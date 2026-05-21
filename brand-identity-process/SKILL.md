---
name: brand-identity-process
description: "End-to-end brand building orchestrator — routes to the correct phase sub-skill based on project state or explicit argument"
argument-hint: "[setup | foundation | visual-identity | collateral]"
allowed-tools:
  - Read
  - Bash
  - Agent
---

<objective>
Lightweight orchestrator for building a personal or studio brand from scratch.

Phases (each is a separate sub-skill loaded on demand):
  Phase 0 — setup           : create project repo structure + git init
  Phase 1 — foundation      : brand brief discovery (name, audience, values, tone)
  Phase 2 — visual-identity : wordmark, palette, typography, guidelines HTML + PNG
  Phase 3 — collateral      : website, LinkedIn, pitch deck, or print/digital assets

Invocation:
  /brand-identity-process                  — auto-detect phase from repo state and continue
  /brand-identity-process setup            — force Phase 0 (new project)
  /brand-identity-process foundation       — force Phase 1
  /brand-identity-process visual-identity  — force Phase 2
  /brand-identity-process collateral       — force Phase 3
</objective>

<process>

## 1. Parse argument

If $ARGUMENTS is one of: setup, foundation, visual-identity, collateral
  → PHASE = that value, skip detection
Else
  → detect phase (step 2)

## 2. Auto-detect phase from repo state

Run: `ls -d *-brand/ 2>/dev/null | head -1`

If no `*-brand/` directory found:
  → PHASE = setup

Else read `<brand>-brand/README.md` and check the "Current Phase" line:
  - "Phase 0 complete" or foundation section empty → PHASE = foundation
  - Foundation locked, visual-identity section empty → PHASE = visual-identity
  - Visual identity locked → PHASE = collateral

## 3. Route to sub-skill

Announce: "Routing to [PHASE] sub-skill."

Invoke the matching skill:
  - setup           → Skill(skill="brand-setup")
  - foundation      → Skill(skill="brand-foundation")
  - visual-identity → Skill(skill="brand-visual-identity")
  - collateral      → Skill(skill="brand-collateral")

Do NOT attempt to run phase logic inline. The sub-skill handles everything.

</process>

<self-improvement>
Every failure is a chance to make the system stronger:
1. Identify what broke (which sub-skill, which step, which tool)
2. Fix the sub-skill file that failed
3. Verify the fix works before continuing
4. Move on with a more robust system

This loop is how the skill improves over time.
</self-improvement>

<applied-learning>
When something fails repeatedly, when the user has to re-explain, or when a workaround is
found for a platform/tool limitation, add a one-line bullet here. Keep each bullet under
15 words. No explanations. Only add things that will save time in future sessions.

(empty — will grow as sessions surface real-world friction)
</applied-learning>
