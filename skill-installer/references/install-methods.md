# Install Methods Reference

## Method 1: GitHub URL (subtree path)

URL form: `https://github.com/<owner>/<repo>/tree/<branch>/<path>`

Steps:
1. Parse owner, repo, branch, path from URL
2. Fetch directory listing via `https://api.github.com/repos/<owner>/<repo>/contents/<path>?ref=<branch>`
3. For each file, fetch raw content via `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>/<file>`
4. For subdirectories (agents/, references/, assets/, scripts/), recurse one level

If API returns 404: repo may be private. Tell user. Fallback: try Exa web fetch on the GitHub HTML page to list files.

## Method 2: npx command

Form: `npx <package>` or `npx -y <package>` or `npx caveman@caveman install`

Steps:
1. Extract package name from command
2. Fetch package metadata: `https://registry.npmjs.org/<package>`
3. Get tarball URL from `dist.tarball` field
4. Download and extract tarball to `/tmp/skill-install-<name>/`
5. Locate SKILL.md inside the extracted package
6. Run security audit BEFORE executing the npx command

Never run the npx command directly until audit passes and user confirms.

## Method 3: Raw GitHub file URL

Form: `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>/SKILL.md`

Fetch the file directly. If it's a single SKILL.md with no supporting files, that's valid — install as-is.

## Scope detection

```
Project-local install path:  <cwd>/.claude/skills/<skill-name>/
User install path:            ~/.claude/skills/<skill-name>/
```

Detect project context by checking:
- Does `.claude/` directory exist in cwd or any parent up to home?
- Does `CLAUDE.md` exist in cwd?
- Is `CLAUDE_PROJECT` env var set?

If any: project-local. Otherwise: user scope.

## Overwrite handling

If target directory already exists:
- Show current version (read existing SKILL.md name/description)
- Ask: "Skill `<name>` already installed. Overwrite?"
- Only overwrite on explicit yes
