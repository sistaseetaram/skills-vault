---
name: vault
description: >-
  Load a project's API keys and secrets from the central AIOS credential vault
  (~/.config/aios-vault/master.env) into the environment, on demand, in any
  session. Use whenever the user says "get the keys from my vault", "load my
  vault", "load secrets", "load credentials", "vault access", "get my API keys",
  "set up env from vault", "pull my keys", "/vault", or when a project's script
  needs credentials to run. Reports masked status only — never prints secret
  values. This is the single source of truth for every project's secrets ("the
  secrets world").
---

# Vault — central credential access

All project secrets are stored **encrypted in the macOS Keychain** (service
`aios-vault`), NOT in a plaintext file. `~/.config/aios-vault/master.env` is now a
names-only manifest (no values); `project-map.json` defines which keys each project
pulls. The loader `~/Desktop/Claude/SharedInfra/vault/vault_loader.py` reads secrets
from the Keychain non-interactively (login keychain — no password prompt).

**This skill's job:** when the user asks to load keys, or a project script needs
them, load the right project's keys into the environment and confirm with masked
status. Never expose values.

**To ADD / EDIT / DELETE keys** (or when a model needs a key that isn't set yet),
launch the manager dashboard — do NOT hand-edit files:
```bash
python3 ~/Desktop/Claude/SharedInfra/vault/vault_server.py
```
It opens a localhost-only web UI (per-project sections, masked fields, reveal,
secure copy, add/edit/delete). Same key can differ per project via "scoped" add.

## Hard security rules (non-negotiable)

- Secrets live in the Keychain — **never** try to `cat`/`Read` them out (e.g.
  `security find-generic-password -w`) and display in chat.
- `master.env` no longer holds values, but still never paste its contents expecting secrets.
- **Never** print `--shell` output to chat un-`eval`'d. That output contains raw values.
- Confirm success with masked audit ONLY: `KEY=<set>` / `KEY=<not set>`.
- If the user pasted a secret into chat, warn them to rotate it; don't repeat it.

## Step 1 — identify the project

Resolve which project the session is working in:
1. Auto-detect from the working directory (the loader matches a path component
   against a `project-map.json` key):
   ```bash
   python3 /Users/sistaseetaram/Desktop/Claude/SharedInfra/vault/vault_loader.py --auto
   ```
2. If detection fails or is ambiguous, ask the user, or list options:
   ```bash
   python3 /Users/sistaseetaram/Desktop/Claude/SharedInfra/vault/vault_loader.py --projects
   ```

## Step 2 — load the keys (pick the pattern that fits)

**(a) Python project script — the default. Load + use in the SAME process:**
```python
import sys; sys.path.insert(0, "/Users/sistaseetaram/Desktop/Claude/SharedInfra")
from vault.vault_loader import load_for_project
load_for_project("ContentGenerator")     # injects into os.environ for THIS process
# now os.getenv("ANTHROPIC_API_KEY") works
```
This is why persistence across shells never matters here: the keys are used in
the same process that loaded them.

**(b) One-off shell command needing a key — load + use in ONE Bash call:**
```bash
eval "$(python3 /Users/sistaseetaram/Desktop/Claude/SharedInfra/vault/vault_loader.py --shell OutreachAutomation)" \
  && curl -sS -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models
```
The value exists only inside this one shell and is never echoed.

> ⚠ **Never** split load and use across two Bash tool calls. Environment
> variables set in one Bash call do NOT survive to the next (each call is an
> isolated shell). Keep `eval "$(...--shell)"` and the command that needs the
> key in the SAME invocation, or use pattern (a).

## Step 3 — confirm (masked)

```bash
python3 /Users/sistaseetaram/Desktop/Claude/SharedInfra/vault/vault_loader.py --audit OutreachAutomation
```
Report the masked table back. Done.

## Adding / rotating keys

- **Rotate:** edit `~/.config/aios-vault/master.env` directly (never via chat),
  then re-run `--audit`.
- **New project:** add a row to `~/.config/aios-vault/project-map.json`
  (`"ProjectName": ["KEY_A", "KEY_B"]`). If a project needs a differently-named
  credential than another project uses under the same env var, alias it:
  `{"vault": "APMINES_TELEGRAM_BOT_TOKEN", "env": "TELEGRAM_BOT_TOKEN"}`.
- **New key:** add an empty `KEY=` slot to `master.env` and reference it in the
  project's map row.

## What this vault does NOT hold

- Non-secret config (hosts, ports, feature flags, model IDs) → stays in each repo.
- Cloudflare Pages bindings deploy separately, but the vault is still the
  canonical place their values are recorded (copy vault → Cloudflare dashboard).
- OAuth client-secret JSON files (Google/YouTube) stay at their file paths; the
  vault may store the path, not the file contents.
