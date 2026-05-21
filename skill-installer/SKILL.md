---
name: "skill-installer"
description: "Use when the user provides a GitHub URL or npx command to install a Claude skill. Handles fetching, security auditing, and installing to the correct scope (project-local vs user/public). Trigger on: 'install this skill', 'pull this skill', 'add this skill', GitHub skill repo links, npx skill install commands."
---

# Skill Installer

Automates: fetch → normalize structure → security audit → scope detection → install (or halt).

## Step 1: Determine install scope

Check context automatically — do NOT ask the user:

- **Inside a project session** (`.claude/` directory exists in cwd, or CLAUDE.md present in project root, or running inside VS Code/IDE with a workspace): → install to **project-local** (`<project>/.claude/skills/`)
- **No project context** (Cloud Desktop app, bare terminal, home directory): → install to **user scope** (`~/.claude/skills/`)

For user-scope installs only: ask the user once before installing:
> "About to install `<skill-name>` to your user skill repository (`~/.claude/skills/`). Confirm?"

Proceed only on explicit yes.

## Step 2: Fetch the skill

### From a GitHub URL

```bash
# Detect the repo root and subdirectory if URL points into a subtree
# e.g. https://github.com/openai/skills/tree/main/skills/.curated/spreadsheet
# → repo: openai/skills, path: skills/.curated/spreadsheet
```

Use Exa web fetch or raw.githubusercontent.com to pull files. Required files:
- `SKILL.md` (mandatory — abort if missing)
- Any files under `agents/`, `references/`, `assets/`, `scripts/` directories

Pull directory listing first, then fetch each file individually. Save to a temp directory: `/tmp/skill-install-<skill-name>/`

### From an npx command

```bash
# Run the npx command in a sandboxed way — capture what it writes, don't execute blindly
# First: fetch the package source from npm registry to inspect before running
# npm pack <package-name> --dry-run  OR  npx --dry-run ...
```

Fetch the package source for audit before executing anything.

## Step 3: Normalize structure

Read `references/skill-structure.md` for the canonical Claude skill layout.

After fetching, inspect the temp directory. If the layout doesn't match, reorganize it before proceeding:

**Detection rules:**

| Observed pattern | Action |
|---|---|
| `SKILL.md` at root, standard subdirs present | Already correct — skip normalization |
| `README.md` instead of `SKILL.md` | Check if it has YAML frontmatter with `name` + `description`. If yes, rename to `SKILL.md`. If no, attempt to generate minimal frontmatter from the README title and description, show user the draft, confirm before continuing. |
| `SKILL.md` nested inside a subdirectory | Hoist it and its siblings up to the temp root |
| Files flat at root (no subdirs) with multiple `.md` files | Move non-SKILL markdown into `references/`. Move `.py`/`.sh`/`.js` files into `scripts/`. Move images/fonts/templates into `assets/`. |
| `prompts/` or `instructions/` directory | Rename to `references/` |
| `tools/` or `bin/` directory | Rename to `scripts/` |
| `examples/` or `templates/` directory | Move into `references/examples/` |
| YAML frontmatter missing `description` field | Abort — cannot install without trigger description. Ask user to provide one. |
| YAML frontmatter missing `name` field | Infer from directory name. Show user, confirm. |

After reorganizing, show the user a summary:
> "Reorganized skill structure: moved X files, renamed Y. Layout now matches Claude's expected format."

Then proceed to audit the normalized structure (not the original).

## Step 4: Security audit

Read `agents/auditor.md` and run a full audit on all fetched files before installing anything.

**Hard stops (abort install, show findings):**
- Shell injection via `eval`, `exec`, `$(...)` on remote/dynamic input
- Network calls that exfiltrate data (POST to external URLs with file contents, env vars, credentials)
- Reading sensitive files: `~/.ssh/`, `~/.aws/`, `.env`, credential files
- Obfuscated code (base64-decoded execution, hex strings run as commands)
- Dependency installation that pulls untrusted packages without pinned versions

**Warnings (show to user, ask to proceed):**
- Broad file system reads outside the skill directory
- Network calls to fetch external resources at runtime
- `npx` install scripts that run arbitrary shell commands

**Pass:** No hard stops found.

If audit fails (hard stop): show exact findings with file:line references. Do not install. Offer to show full file contents.

If warnings only: list them clearly, ask user to confirm before proceeding.

## Step 5: Install

On audit pass (and user confirmation for user-scope):

```bash
# Project-local
cp -r /tmp/skill-install-<name>/ <project-root>/.claude/skills/<name>/

# User scope
cp -r /tmp/skill-install-<name>/ ~/.claude/skills/<name>/
```

Clean up temp directory after install:
```bash
rm -rf /tmp/skill-install-<name>/
```

## Step 5.5: Self-Improvement Check

After install, assess whether the skill benefits from a self-improvement loop.

**Check first:** Does the installed `SKILL.md` already contain `## The Self-Improvement Loop` or `## Applied Learning`? If yes — skip this step entirely.

**Relevance test** — relevant if the skill has any of:
- A multi-step workflow or process that executes and can fail
- Content generation, transformation, or judgment logic
- External tool / API / scheduler usage
- Patterns that compound with repeated use (prompts, searches, frameworks)

**Not relevant** — skip if the skill is purely a static reference file, constants lookup, or read-only knowledge base with no execution logic.

**If relevant and sections missing**, append to the installed `SKILL.md`:

```markdown
## The Self-Improvement Loop

Every failure is a chance to make the system stronger:
1. Identify what broke
2. [Fix the <tool / skill / pattern / approach>]
3. Verify the fix works
4. Update the workflow with the new approach
5. Move on with a more robust system

This loop is how [skill-name] improves over time.

## Applied Learning

When something fails repeatedly, when the user has to re-explain, or when a workaround is found for a platform/tool limitation, add a one line bullet here. Keep each bullet under 15 words. No explanations. Only add things that will save time in future sessions.
```

Step 2 noun guide: tool-based → "Fix the tool"; generation/judgment → "Fix the skill or pattern"; search/research → "Fix the search approach"; scheduler/automation → "Fix the tool or schedule".

Note whether sections were added or skipped — include in the Step 6 confirm message.

## Step 6: Confirm

Tell the user:
- Skill name installed
- Install path (project or user scope)
- Trigger description (from SKILL.md frontmatter) so they know when it activates
- Any warnings that were noted (even if they chose to proceed)

## Step 7: Register in the master registry

An unregistered skill is invisible to the system. After a successful install, append (or update) one row in:

```
/Users/sistaseetaram/Desktop/Claude/claude-datastore/SKILL-REGISTRY.md
```

Schema: `key | scope | project | path | purpose | triggers`

- `key` = `scope:project:skill` — user-scope → `global:-:<name>`, project-local → `local:<project>:<name>` (project = the install project's directory name)
- `path` = absolute path to the installed `SKILL.md`
- `purpose` = one self-sufficient line distilled from the skill's frontmatter `description`
- `triggers` = the trigger phrases from the frontmatter

If a row with that `key` already exists (re-install/overwrite), update it in place — never duplicate. Place the row under the most fitting Layer section, or an "Imported" section if no layer fits. Tell the user the registry row was written/updated.

---

## npx-specific extra caution

npx commands run arbitrary code on install. Always:
1. Inspect the package source BEFORE running
2. Run `npm pack --dry-run` to see what files are included
3. If the package has a `postinstall` script, show it to the user and require explicit confirmation regardless of audit result
4. Never pipe curl output directly to bash

---

## Failure modes

| Situation | Action |
|---|---|
| No SKILL.md and no README.md | Abort. Not a valid skill repo. |
| README.md found, no frontmatter | Attempt to generate frontmatter, confirm with user before continuing. |
| GitHub URL 404 | Abort. Check if repo is private. |
| Audit hard stop | Abort. Show findings. |
| User says no to scope confirmation | Abort cleanly. |
| Install path already exists | Ask: overwrite or cancel? |
