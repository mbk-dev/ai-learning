# AI Learning

Portable skills by Sergey Kikevich for AI coding agents, agent-assisted development
courses, and personal projects.

A skill is a reusable workflow instruction. It does not install Git, an
orchestrator, MCP servers, or accounts, and it does not grant additional authority.

## Available skills

| Skill | Purpose |
| --- | --- |
| [commit](skills/commit/SKILL.md) | Review changes, create coherent commits, preserve unrelated work, and handle push/PR permissions |
| [tracker-task-hygiene](skills/tracker-task-hygiene/SKILL.md) | Write clear tasks and acceptance criteria, maintain accurate status, and report verified completion |
| [agent-behavior-graph](skills/agent-behavior-graph/SKILL.md) | Design and review agent workflows with branches, bounded retries, waits, handoffs, and escalation |

These are self-contained educational adaptations of the author's working skills.
They do not depend on the author's private servers, memory, paths, or scripts.
The skill instructions and course examples are currently written in Russian.

## Installation

Use [Skills CLI](https://github.com/vercel-labs/skills) with a supported Node.js
version. The following commands install one skill globally for Codex:

```bash
npx skills add mbk-dev/ai-learning --skill commit -g -a codex
npx skills add mbk-dev/ai-learning --skill tracker-task-hygiene -g -a codex
npx skills add mbk-dev/ai-learning --skill agent-behavior-graph -g -a codex
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

## License

[MIT](LICENSE). Copyright © 2026 Sergey Kikevich.
