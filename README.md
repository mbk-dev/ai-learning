# AI Learning

Portable skills for AI coding agents, agent-assisted development courses,
and personal projects.

A skill is a reusable workflow instruction. It does not install Git, an
orchestrator, MCP servers, or accounts, and it does not grant additional authority.

## Native Codex subagents — milestone 1

Use the [student setup prompt](docs/codex-native-subagents-setup-prompt.md)
to install the course's native Codex roles globally with your ChatGPT sign-in.
The prompt preserves existing settings and asks before resolving conflicts.
See the [setup guide](docs/codex-native-subagents.md) and
[ready-to-copy TOML files](codex/native-subagents/agents/).
No API keys or third-party model providers are required.

## Keep instructions and task knowledge up to date

Use the [update-instructions setup prompt](docs/update-instructions-setup-prompt.md)
to create a portable personal workflow in Codex or Claude Code. It includes the
skill content, so a local checkout is not required. The prompt preserves existing
settings and provides backup, rollback, and fresh-session verification steps.

Invoke `$update-instructions` in Codex or `/update_instructions` in Claude Code.
Use `--no-delivery` to update verified knowledge without publishing, or
`--checkpoint` to save task state for continuation. Full delivery follows the
project's permissions and review process; automatic knowledge updates do not
grant permission to publish.

## Available skills

| Skill | Purpose |
| --- | --- |
| [commit](skills/commit/SKILL.md) | Review changes, create coherent commits, preserve unrelated work, and handle push/PR permissions |
| [tracker-task-hygiene](skills/tracker-task-hygiene/SKILL.md) | Write clear tasks and acceptance criteria, maintain accurate status, and report verified completion |
| [agent-behavior-graph](skills/agent-behavior-graph/SKILL.md) | Design and review agent workflows with branches, bounded retries, waits, handoffs, and escalation |
| [course-run-epic-waves](skills/course-run-epic-waves/SKILL.md) | Coordinate course tasks through dependency graphs, independent agent waves, acceptance, integration, and recovery |

These are self-contained educational adaptations of the author's working skills.
They do not depend on the author's private servers, memory, paths, or scripts.
The skill instructions and course examples are currently written in Russian.

## Installation

New to Node.js or missing `npx`? Follow the [macOS, Windows, and Linux setup guide](docs/install-node.md) first.

Use [Skills CLI](https://github.com/vercel-labs/skills) with a supported Node.js
version. The following commands install one skill globally for Codex:

```bash
npx skills add mbk-dev/ai-learning --skill commit -g -a codex
npx skills add mbk-dev/ai-learning --skill tracker-task-hygiene -g -a codex
npx skills add mbk-dev/ai-learning --skill agent-behavior-graph -g -a codex
npx skills add mbk-dev/ai-learning --skill course-run-epic-waves -g -a codex
```

For Claude Code, replace `-a codex` with `-a claude-code`. For OpenCode, use
`-a opencode`. To install only in a project, run the command from that project
and omit `-g`.

Check for an existing skill with the same name before installing. Do not overwrite
a different implementation without reviewing it. Use a separate training profile
or a supported rename when both versions are needed. Start a fresh agent session
and verify that the intended skill is available.

Codex users can also ask the built-in `skill-installer` to install a selected
folder, such as `skills/agent-behavior-graph`, from `mbk-dev/ai-learning`.

List available skills without installing them:

```bash
npx skills add mbk-dev/ai-learning --list
```

## Usage and exercises

**Commit**

> Use the commit skill. Inspect the changes and create only a local commit for
> the fix. Do not push.

[Commit exercise](docs/commit-exercise.md).

**Tracker task hygiene**

> Use tracker-task-hygiene to draft a task for this problem: intended outcome,
> scope, and verifiable acceptance criteria. Do not publish it yet.

[Task examples and exercise](skills/tracker-task-hygiene/references/examples.md).

**Agent behavior graph**

> Use agent-behavior-graph to describe this process, including failure branches,
> bounded retries, and escalation. Separate confirmed requirements from unknowns.

[Workflow example and exercise](skills/agent-behavior-graph/references/example.md).

**Task waves — milestone 1**

> Use course-run-epic-waves to execute this training task through a dependency
> graph and independent agent waves. Verify each result and deliver each wave
> before starting the next. Preserve permissions and pending operations on resume.

[Exercise, expected artifacts, and failure scenarios](docs/run-epic-waves-exercise.md).
The course uses native Codex roles through ChatGPT sign-in; the skill does not
require external CLI workers or paid API keys.

Project instructions and existing permissions continue to apply. A diagram is a
workflow contract, not an execution engine.

## Graph checker

The graph skill includes a Python 3.10+ checker using only the standard library.
From a checkout of this repository:

```bash
python3 skills/agent-behavior-graph/scripts/graph_check.py skills/agent-behavior-graph/references/example.md
python3 -m unittest discover -s skills/agent-behavior-graph/tests -v
```

It checks flat Mermaid state diagrams for structural problems, including missing
entry/exit paths, unreachable states, incomplete fallbacks, and apparently
unbounded cycles. Nested/concurrent state diagrams are outside its supported
subset. It is a heuristic: it cannot prove that a counter changes, that guards
are correct, or that an agent will follow the process. Render diagrams separately
and inspect them visually.

For Python lint and formatting checks:

```bash
uvx ruff check skills/agent-behavior-graph
uvx ruff format --check skills/agent-behavior-graph
```

## Validation status

The skill instructions passed compatibility checks in the author's environment.
The graph checker passed 15 CLI regression tests, and the included example passed
structural checks and rendering with Mermaid CLI 11.17.0. These checks do not
constitute a behavioral evaluation of an autonomous agent or a clean classroom VM.

The task-wave skill passed format and instruction-compatibility checks; both
example graphs were rendered and visually inspected with Mermaid CLI 11.17.1,
and its state diagram passed the included graph checker. Skills CLI discovers
all four skills. Agent execution and clean-VM validation remain unperformed; see
the [exercise validation notes](docs/run-epic-waves-exercise.md#статус-проверки-материала).

## License

[MIT](LICENSE).
