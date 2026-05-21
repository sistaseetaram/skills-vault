# Claude Skill — Canonical Structure

```
<skill-name>/
├── SKILL.md           (required)
├── agents/            (optional) — subagent instruction files (.md)
├── references/        (optional) — docs, schemas, examples loaded into context
│   └── examples/      (optional) — runnable example files
├── scripts/           (optional) — executable code (.py, .sh, .js)
└── assets/            (optional) — static files (templates, fonts, images)
```

## SKILL.md frontmatter (required fields)

```yaml
---
name: "skill-name"           # kebab-case, matches directory name
description: "..."           # trigger description — must explain WHEN to use this skill
---
```

Optional frontmatter fields:
```yaml
compatibility:               # tools or env this skill requires
  tools: [Read, Write, Bash]
  requires: [python3, node]
```

## Rules

- `SKILL.md` must be at the directory root — not nested
- `name` must match the directory name exactly
- `description` is the sole trigger mechanism — must be present and descriptive
- `agents/` files: each is a standalone instruction set for a subagent, named descriptively (e.g. `auditor.md`, `grader.md`)
- `scripts/` files: executable, should be invokable directly; no hardcoded absolute paths
- `references/` files: read-only context; use a table of contents comment at top if >300 lines
- `assets/` files: binary or static; referenced by path from SKILL.md or scripts

## Size guidelines

- `SKILL.md` body: under 500 lines ideal
- If approaching limit: split into `references/` files and add clear pointers in SKILL.md

## Common non-standard layouts and their mappings

| Foreign pattern | Maps to |
|---|---|
| `README.md` with frontmatter | → `SKILL.md` |
| `prompts/`, `instructions/` | → `references/` |
| `tools/`, `bin/`, `src/` | → `scripts/` |
| `examples/`, `templates/` | → `references/examples/` |
| `img/`, `static/`, `public/` | → `assets/` |
| Flat `.py`/`.sh` files at root | → `scripts/<file>` |
| Flat `.md` files at root (not SKILL.md) | → `references/<file>` |
