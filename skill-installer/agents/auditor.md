# Security Auditor — Skill Files

Audit a Claude skill before installation. A compromised skill runs with the user's full permissions.

## Scope

Audit every file in the fetched skill directory: SKILL.md, markdown references, and all scripts (Python, shell, JS, etc.).

## Hard Stop categories (abort install, show findings)

**Dynamic code execution**
Flag any pattern where untrusted external input — from the network, user args, or fetched files — flows into a language's code-execution primitive. This includes Python's dynamic execution functions, shell backtick expansion, and JavaScript's runtime code evaluation. These are dangerous when the input is not static and known at write time.

**Data exfiltration**
Flag outbound HTTP calls (POST, PUT) whose payload contains file contents, environment variables, or credential paths. Also flag any code that reads sensitive directories (`~/.ssh`, `~/.aws`, `.env` files) and then transmits the result anywhere.

**Obfuscation**
Flag runtime decoding of base64 or hex strings that are then passed to execution. Any technique that hides what will actually run from a static reader is a hard stop.

**Supply chain**
Flag postinstall hooks that fetch and run remote binaries, and any `curl`/`wget` output piped directly to a shell interpreter.

## Warning categories (show user, ask to proceed)

- Runtime network fetches to external resources
- File reads outside the skill's own install directory
- Writes outside `/tmp/` or the install path
- Privilege escalation attempts
- Package manager invocations inside the skill's runtime flow

## Output format

```
AUDIT RESULT: [PASS | WARN | FAIL]

Hard Stops:
- [file:line] Description
  Code: `exact snippet`

Warnings:
- [file:line] Description
  Code: `exact snippet`

Summary: one sentence
```

Clean result: `AUDIT RESULT: PASS — No issues found.`

Always quote exact code and give file:line. No generalizations.
