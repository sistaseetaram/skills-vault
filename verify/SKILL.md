---
name: verify
description: Use when a project or feature is near completion or before publishing, shipping, deploying, or activating anything — or when the user says "I think we're done", "ready to ship", "before we publish", "final check", "is it done", "test it before it goes live". Detects what was actually built, generates product-SPECIFIC tests for that thing, runs them, and only green-lights release when clean. Stops work that only LOOKS done from shipping.
argument-hint: "[optional: what to verify]"
---

## What this does

Step 2 of the trust stack. Claude (any model) will hand you something that *looks* finished but isn't — a dashboard that breaks on mobile, a workflow with a dead node, a script that crashes on empty input. `verify` is the gate that catches that BEFORE it ships.

This is **not a fixed test suite.** There is no canned "Playwright test." The whole idea: look at what was actually built, derive the *right* tests for *that* product, run them, report honestly. A dashboard, an n8n workflow, and a Python tool need totally different tests — so build them per product, every time, before publishing.

## Step 0: The gate (when this fires)

Fire this skill when the project is near its finish line — either the user signals it, OR you detect it (deliverable built, user winding down, about to deploy/activate/hand off). Ask once, plainly:

> Project looks near done. Want me to build + run a verification pass before we publish?
> I'll create tests specific to **[detected product]** and only green-light when clean. **[yes / no / not yet]**

If no/not yet → stop, note it, continue. If "just ship it" override → respect it but state the risk in one line. If yes → proceed.

## Step 1: Detect project type + finish line

Look at what was built. Map it to its real "done" line (this is what "publish" means for this project):

| Type | "Done / publish" means | 
|---|---|
| Web app / dashboard / artifact | deployed or viewable in browser |
| n8n workflow | activated on the instance |
| Python tool / script / report | runs clean + output file generated |
| API / service | endpoints live + contract honored |
| Skill | installed + trigger fires + registered |
| Content / ad / report doc | published / sent to client |

## Step 2: Derive the test plan for THAT product

Pick the relevant column. These are starting checklists — adapt to the actual build, add product-specific cases:

- **Web / dashboard / artifact** → start the local server; use Playwright CLI (`npx playwright`) as computer-use; screenshot **every section** at **desktop AND mobile** viewports; check console for errors; test responsive/dark mode; **stress-test every form** with valid + malformed inputs (leading spaces, bad emails, duplicate submit, empty required, oversized); check broken links.
- **n8n workflow** → validate every node config; execute with a realistic test payload; inspect each node's output; trigger the error/failure path; confirm credentials are present; check it's activation-ready (no test-only nodes left).
- **Python tool / script** → run on real input; hit edge inputs (empty, malformed, huge, unicode, missing file); check exit codes; confirm output file exists, is non-empty, and is well-formed; force an exception path and confirm it's handled.
- **API / service** → hit each endpoint; assert status codes + response schema; test auth (valid + missing + expired); test error responses; check rate-limit / timeout behavior.
- **Skill** → confirm it installs; test that its trigger phrases actually invoke it; dry-run an invocation end-to-end; confirm the registry row exists and is correct.
- **Content / ad / report** → are factual claims grounded (no hallucinated stats)? do all links/numbers resolve? on-brand voice? required disclaimers present?

Write the chosen test list down first (definition of done) so "done" is objective, not a vibe.

## Step 3: Build + run the tests

Generate the actual tests/commands for this product and run them. Prefer deterministic scripts/CLIs over manual clicking (efficiency hierarchy). Watch real behavior — headed browser when you need to see it, headless when you don't. Capture proof (screenshots, output files, logs).

## Step 4: Report (honest, skimmable)

```
## VERIFY REPORT — <product>
Tests: <N>  (pass <P> / fail <F>)
- <test name> — PASS/FAIL — <one-line detail / proof>
...
Gaps found: <real holes, e.g. "no duplicate-email guard">
VERDICT: SHIP  /  FIX-FIRST
```

If FIX-FIRST: list the smallest fixes that flip it to SHIP. Never report SHIP while a test is red. Don't soften failures.

## Step 5 (optional): Cross-model second opinion

For high-stakes ships, pass the report to a different model to break correlated blind spots:

```bash
codex exec "Review this verification report. What did it fail to test? Any gap that should block ship? REPORT: <report>"
# or
gemini -p "Review this verification report for missing test coverage before we ship. REPORT: <report>"
```

Surface any disagreement to the user.

## Rules

- Tests are **built per product, every time.** No reusing yesterday's test plan blindly — derive from what's actually in front of you.
- "Looks done" is not done. Only SHIP on green tests with proof.
- The gate question fires before the irreversible go-live step, not after.
- Respect an explicit "just ship it" override, but state the risk in one line first.
- This catches broken builds; it does not cure bias — pair with `roast` at project start.
