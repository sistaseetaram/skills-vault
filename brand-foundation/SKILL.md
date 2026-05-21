---
name: brand-foundation
description: "Brand Phase 1 — discover brand essence through structured questions and produce a locked brand brief"
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
---

<objective>
Captures the brand's core identity through batched, structured questions and writes a locked brand brief.

The brief is the foundation every subsequent phase reads before producing any visual artifact.
Text output is acceptable here — this phase is conceptual, not visual.

Invoked by: brand-identity-process (Phase 1)
Followed by: brand-visual-identity (Phase 2)
</objective>

<process>

## 1. Find the repo

Run: `ls -d *-brand/ 2>/dev/null | head -1`
Set REPO to the result. If not found, stop and say: "No brand repo found. Run /brand-identity-process setup first."

## 2. Check for existing brief

Read `<REPO>/01-foundation/brand-brief.md` if it exists.
If it exists and is populated, ask: "A brand brief already exists. Resume and update it, or start fresh?"

## 3. Collect brand information (batch 1)

Ask all of the following in a single AskUserQuestion call:
- Brand name — what is it, and what does it do in one sentence?
- Target audience — who are they, and what do they care about?
- 3–5 core values — words or short phrases that define the brand's character
- Tone of voice — where does it sit on these spectrums: formal↔casual, bold↔understated, warm↔sharp?

## 4. Collect visual direction (batch 2, optional)

Ask:
- Any visual references, moods, or aesthetics that feel right? (designers, brands, colors, textures — anything)
- Any visual directions to explicitly avoid?

If the user has no references, mark as "open exploration" — do not block on this.

## 5. Write brand-brief.md

Write `<REPO>/01-foundation/brand-brief.md`:

```markdown
# Brand Brief — <Brand Name>

## Identity
**Name:** <name>
**What it does:** <one-sentence description>

## Audience
<description of target audience and what they care about>

## Core Values
- <value 1>
- <value 2>
- <value 3>
(etc.)

## Tone of Voice
- Formal / Casual: <position>
- Bold / Understated: <position>
- Warm / Sharp: <position>

## Visual Direction
**References:** <anything provided, or "open exploration">
**Avoid:** <anything provided, or "none specified">

## Status
Phase 1 locked — <date>
```

## 6. Update README and commit

Update `<REPO>/README.md` — replace the Foundation section under "Locked Decisions" with a one-line summary of name, audience, and tone.

```bash
cd <REPO>
git add 01-foundation/brand-brief.md README.md
git commit -m "Lock Phase 1 — brand foundation brief"
```

## 7. Hand off

Print:
  "Brand brief locked and committed.
   Run /brand-identity-process visual-identity to begin Phase 2."

</process>
