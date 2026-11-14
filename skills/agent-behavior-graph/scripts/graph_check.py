"""Check structural defects in flat Mermaid state diagrams (Python 3.10+).

This is a heuristic checker, not a Mermaid parser or a proof of termination.
Use a Mermaid renderer separately and review guards and counter updates manually.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

BOUND = re.compile(
    r"(?<![\w/])(?:<=|<|≤)\s*(?:\d+|[A-Za-z_]\w*|[а-яё]+)\b"
    r"|меньше\s+(?:\d+|[A-Za-z_]\w*)\b"
)
STATE_EDGE = re.compile(r"(\[\*\]|\w+)\s*-->\s*(\[\*\]|\w+)\s*(?::\s*(.*))?$")
STATE_CHOICE = re.compile(r"state\s+(\w+)\s+<<choice>>")
STATE_DECL = re.compile(r'state\s+(?:"[^"\n]+"\s+as\s+)?(\w+)')
ELSE = re.compile(r"\b(?:иначе|else)\b", re.IGNORECASE)


def reachable(starts, adjacency):
    """Return nodes reachable without crossing the start/end pseudostate."""
    seen = set(starts) - {"[*]"}
    pending = list(seen)
    while pending:
        for node in adjacency.get(pending.pop(), []):
            if node != "[*]" and node not in seen:
                seen.add(node)
                pending.append(node)
    return seen


def unbounded_loops(out: dict[str, list[tuple[str, str]]]) -> list[str]:
    """Циклы, на которых ни одно ребро не несёт предела, — по циклу-примеру на компоненту.

    Рёбра с пределом убираются; любой цикл в остатке ничто не останавливает. Обход только по
    обратным рёбрам тут не годится: в узел, уже пройденный путём с пределом, второй путь без
    предела заходит незамеченным.
    """
    rest = {
        v: [w for w, lab in edges if w != "[*]" and not BOUND.search(lab)]
        for v, edges in out.items()
    }
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[set[str]] = []

    def strong(v: str) -> None:
        """Тарьян: компоненты сильной связности остатка."""
        index[v] = low[v] = len(index)
        stack.append(v)
        on_stack.add(v)
        for w in rest.get(v, []):
            if w not in index:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            component: set[str] = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                component.add(w)
                if w == v:
                    break
            components.append(component)

    for v in sorted(rest):
        if v not in index:
            strong(v)

    loops: list[str] = []
    for component in components:
        start = min(component)
        if len(component) == 1 and start not in rest.get(start, []):
            continue
        # Кратчайший путь из start обратно в start внутри компоненты — пример цикла.
        parent: dict[str, str] = {}
        queue = [start]
        while queue:
            v = queue.pop(0)
            if start in rest.get(v, []):
                path = [v]
                while path[-1] != start:
                    path.append(parent[path[-1]])
                loops.append(" -> ".join(reversed(path)) + f" -> {start}")
                break
            for w in rest.get(v, []):
                if w in component and w not in parent and w != start:
                    parent[w] = v
                    queue.append(w)
    return loops


def check_block(body: str, number: int) -> bool | None:
    lines = [line.strip() for line in body.strip().splitlines()]
    while lines and (not lines[0] or lines[0].startswith("%%")):
        lines.pop(0)
    if not lines or lines[0] not in {"stateDiagram-v2", "stateDiagram"}:
        print(f"[{number}] skipped: not a state diagram")
        return None
    edges = []
    nodes = set()
    choices = set()
    for line in lines[1:]:
        if match := STATE_DECL.match(line):
            nodes.add(match.group(1))
        if match := STATE_CHOICE.match(line):
            choices.add(match.group(1))
        if match := STATE_EDGE.fullmatch(line):
            a, b, label = match.groups()
            edges.append((a, b, label or ""))
            nodes.update((a, b))
    nodes.discard("[*]")
    out = defaultdict(list)
    forward = defaultdict(list)
    reverse = defaultdict(list)
    for a, b, label in edges:
        out[a].append((b, label))
        forward[a].append(b)
        reverse[b].append(a)
    starts = {b for a, b, _ in edges if a == "[*]" and b != "[*]"}
    finals = {a for a, b, _ in edges if b == "[*]" and a != "[*]"}
    branching = choices | {node for node in nodes if len(out[node]) > 1}
    unsupported = [
        line
        for line in lines[1:]
        if (line.startswith("state ") and line.endswith("{"))
        or line in {"}", "--"}
        or "<<fork>>" in line
        or "<<join>>" in line
    ]
    findings = {
        "unsupported_syntax": unsupported,
        "empty_graph": not edges or not nodes,
        "missing_start": not starts,
        "missing_finish": not finals,
        "dead_ends": sorted(node for node in nodes if not out[node]),
        "unreachable_states": sorted(nodes - reachable(starts, forward)),
        "no_final_path": sorted(nodes - reachable(finals, reverse)),
        "choices_without_else": sorted(
            node
            for node in branching
            if not any(ELSE.search(label) for _, label in out[node])
        ),
        "multiple_else": sorted(
            node
            for node in nodes
            if sum(bool(ELSE.search(label)) for _, label in out[node]) > 1
        ),
        "unbounded_loops": unbounded_loops(out),
        "escalation_not_final": sorted(
            {a for a, b, _ in edges if a.startswith("Escalate_") and b != "[*]"}
        ),
    }
    print(f"[{number}] states={len(nodes)} edges={len(edges)}")
    for name, finding in findings.items():
        print(f"[{number}] {name}={finding}")
    return not any(findings.values())


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python3 graph_check.py FILE.md|FILE.mmd")
        return 2
    try:
        text = Path(argv[0]).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Cannot read input: {error}")
        return 2
    blocks = re.findall(r"^```mermaid[ \t]*\n(.*?)^```", text, re.DOTALL | re.MULTILINE)
    results = [check_block(body, i) for i, body in enumerate(blocks or [text], 1)]
    checked = [result for result in results if result is not None]
    if not checked:
        print("FAIL: no state diagram found")
        return 1
    ok = all(checked)
    print("OK" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
