---
name: setu-brand-context
description: >
  Loads Setu personal brand context from source files and applies it to any current task.
  Use this skill whenever the user wants to apply their brand, style something to match Setu,
  check brand consistency, use their design system, get their brand colors or typography,
  or write in their brand voice. Trigger on: "apply my brand", "use my brand", "brand this",
  "setu style", "setu brand", "style this for me", "make it on-brand", "my brand style",
  "keep it consistent with my brand", "incorporate my brand", "what are my brand colors",
  "what's my brand voice", "my brand voice", "my color palette", "use my design system",
  "my design tokens", "give me brand context", "brand context". Also trigger when the user
  asks to write copy, create visuals, design UI, or draft content and mentions wanting it
  to "feel like me" or match their personal brand — even if they don't say "Setu" explicitly.
---

# Setu Brand Context

## What to do

1. Read this SKILL.md and the **required** small file `CLAUDE.md` (hard rules).
2. Print the **Brand Context Summary** below.
3. Open the matching `references/` file(s) for the current task (see Reference Map).
4. Apply constraints to the task. If no task, stop after the summary.

## Reference Map (open on demand)

| Need | File |
|---|---|
| Color palette, opacity rule, grandfathered hex | `references/palette.md` |
| Fonts, scale, label spec | `references/typography.md` |
| Positioning, audience, voice DOs/DON'Ts | `references/voice.md` |
| Live site URL, stack, LinkedIn locked assets | `references/assets.md` |
| Hard NO list (no new hex, no gradients, etc.) | `references/forbidden.md` |

## Required source files

```
HARD RULES (palette lock, branch policy, locked assets — small, always read):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/CLAUDE.md
```

## On-demand source files (only if reference snippet insufficient)

```
BRAND BRIEF (voice, values, positioning — source of truth):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/01-foundation/brand-brief.md

DESIGN TOKENS (machine-readable):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/tokens/setu-tokens.json

DESIGN SYSTEM (component patterns):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/03-collateral/website/DESIGN-SYSTEM.md

VISUAL IDENTITY (full guidelines — large, rarely needed):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/02-visual-identity/brand-guidelines.html

LIVE SITE SOURCE (only for component-accurate styling):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/03-collateral/website/site/
```

## Brand Context Summary

**Brand:** Setu — AI agency for practical AI adoption. Sanskrit सेतु = bridge. Founder-led.
**Live:** https://setuagency.com (Astro + Cloudflare Pages, www→apex 301, SSL).
**Positioning:** Start with one repeated workflow. Bridge Zero (free workflows) → Bridge 01 (paid pilot).
**Audience (Bridge 01):** India construction & architecture firms. Smart, busy owners. Outcomes, not jargon.

**Voice:** Quietly confident expert. Plainspoken. ROI-forward. Technically deep, never showing off.
- DO: specifics (hours saved, money, workflows), short sentences, plain words.
- DON'T: "revolutionary", "game-changing", "cutting-edge", jargon, **proof claims before they exist**, hype.
- Test: *"Would a smart, busy architecture firm owner feel respected — or sold to?"*

**Colors (11 locked tokens — no new hex, no derived tints):** Light / Paper / Terracotta Dark / Forest / Anthracite + Muted + Rule. New tints use locked-fg + opacity 0.6–0.8. Full table → `references/palette.md`.

**Typography:** Cormorant Garamond (display) · Inter (body 17px / 1.7) · Noto Sans Devanagari (`से` glyph). No new fonts. → `references/typography.md`.

**Feel:** Calm, crafted, Indian, confident in negative space. Architecture studio, not tech startup. No gradients, glows, neon, AI-brain motifs. Hard NO list → `references/forbidden.md`.

## Applying brand to tasks

- **Copy/writing:** Setu voice (see voice.md). Swap jargon for specifics. Strip hype. Outcome-first.
- **Design/UI:** Locked tokens only (palette.md). Cormorant for display, Inter for body. Generous whitespace. Default Light/Paper; reserve Terracotta Dark for hero moments. Check forbidden.md before any new hex.
- **Content/social:** Show the work, not the tech. Real hours, real money, real workflows.

## Self-Improvement Loop

After using this skill, note if:
1. A file path changed → update path here or in the relevant reference
2. New locked decision (color, font, asset) → add to the matching reference, not SKILL.md
3. Summary format missed a use case → extend summary or add a new reference file
4. Trigger phrase missed (user had to ask twice) → add to description
5. Over-triggering → tighten description
