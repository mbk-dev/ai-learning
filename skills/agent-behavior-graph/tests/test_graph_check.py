"""Exercise the public CLI against valid and deliberately broken process graphs."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "graph_check.py"
VALID = """stateDiagram-v2
    [*] --> Work
    Work --> result
    state result <<choice>>
    result --> Done_ok : [verified]
    result --> Escalate_failure : [else]
    Done_ok --> [*]
    Escalate_failure --> [*]
"""


class GraphCheckTests(unittest.TestCase):
    def check_cli(self, graph, expected_code, finding=None):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temporary:
            source = Path(temporary) / "process.md"
            source.write_text(graph, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(source)],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        self.assertEqual(
            result.returncode, expected_code, result.stdout + result.stderr
        )
        if finding:
            self.assertIn(finding, result.stdout)

    def test_valid_process(self):
        self.check_cli(VALID, 0)

    def test_no_graph(self):
        self.check_cli("A process without a graph.", 1)

    def test_empty_diagram_is_not_success(self):
        self.check_cli("stateDiagram-v2\n", 1, "empty_graph")

    def test_declared_but_unused_state_is_reported(self):
        self.check_cli(VALID + 'state "Forgotten work" as Forgotten\n', 1, "dead_ends")

    def test_missing_entry_is_reported(self):
        self.check_cli("stateDiagram-v2\nDone_ok --> [*]\n", 1, "missing_start")

    def test_disconnected_process_is_reported(self):
        self.check_cli(
            VALID + "Other --> Done_other\nDone_other --> [*]\n",
            1,
            "unreachable_states",
        )

    def test_missing_fallback_is_reported(self):
        self.check_cli(VALID.replace("[else]", "[failed]"), 1, "choices_without_else")

    def test_multiple_fallbacks_are_reported(self):
        self.check_cli(VALID.replace("[verified]", "[else]"), 1, "multiple_else")

    def test_bounded_retry_is_accepted(self):
        graph = """stateDiagram-v2
[*] --> Work
Work --> Retry
state Retry <<choice>>
Retry --> Work : [attempts < N] / increment attempts
Retry --> Escalate_limit : [else]
Escalate_limit --> [*]
"""
        self.check_cli(graph, 0)

    def test_word_deadline_does_not_bound_a_loop(self):
        graph = """stateDiagram-v2
[*] --> Waiting
Waiting --> Waiting : [срок не задан]
Waiting --> Escalate_limit : [else]
Escalate_limit --> [*]
"""
        self.check_cli(graph, 1, "unbounded_loops")

    def test_unbounded_alternative_path_is_reported(self):
        graph = """stateDiagram-v2
[*] --> Work
Work --> Bounded : [attempts < N]
Work --> Bypass : [else]
Bounded --> Work
Bypass --> Work : [again]
Bypass --> Escalate_limit : [else]
Escalate_limit --> [*]
"""
        self.check_cli(graph, 1, "unbounded_loops")

    def test_escalation_cannot_resume_implicitly(self):
        self.check_cli(
            VALID.replace("Escalate_failure --> [*]", "Escalate_failure --> Work"),
            1,
            "escalation_not_final",
        )

    def test_bounded_cycle_without_final_path_is_reported(self):
        graph = """stateDiagram-v2
[*] --> Work
[*] --> Done_ok
Work --> Work : [attempts < N]
Done_ok --> [*]
"""
        self.check_cli(graph, 1, "no_final_path")

    def test_nested_diagram_is_not_silently_accepted(self):
        graph = """stateDiagram-v2
[*] --> Group
state Group {
    [*] --> Work
    Work --> [*]
}
Group --> [*]
"""
        self.check_cli(graph, 1, "unsupported_syntax")

    def test_each_markdown_graph_is_checked(self):
        self.check_cli(
            "```mermaid\n"
            + VALID
            + "```\n\n```mermaid\n"
            + VALID.replace("[else]", "[failed]")
            + "```\n",
            1,
            "choices_without_else",
        )


if __name__ == "__main__":
    unittest.main()
