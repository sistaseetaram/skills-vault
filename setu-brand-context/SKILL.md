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

This skill loads Setu's brand identity from its canonical source: the **personal-brand-wiki**.

Personal-brand-wiki is the single source of truth. This skill is a reader of it, not a second copy. Brand facts here → stale. Brand facts in the wiki → live.

## Load procedure

1. Read `personal-brand-wiki/wiki/index.md` — the map.
2. Read ALL files in `personal-brand-wiki/wiki/syntheses/` — the bets (small, high-value).
3. Read the specific concept page(s) needed for the task:
   - Voice + tone → `personal-brand-wiki/wiki/concepts/setu-voice.md`
   - Positioning + bridge → `personal-brand-wiki/wiki/concepts/setu-positioning.md`
   - Values + filter checklist → `personal-brand-wiki/wiki/concepts/setu-values.md`
   - Visual system → `personal-brand-wiki/wiki/concepts/setu-visual-identity.md`
   - Audience / ICP → `personal-brand-wiki/wiki/concepts/target-audience.md`
4. For design tokens + visual system details: also read `personal-brand-wiki/AGENTS.md` and the on-demand files below.
5. Apply constraints to the task.

## On-demand files (raw source details — rarely needed)

```
BRAND BRIEF (voice, values, positioning — full source):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/01-foundation/brand-brief.md

DESIGN TOKENS (machine-readable):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/tokens/setu-tokens.json

DESIGN SYSTEM (component patterns):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/03-collateral/website/DESIGN-SYSTEM.md

VISUAL IDENTITY (full guidelines — large, rarely needed):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/setu-brand/02-visual-identity/brand-guidelines.html

HARD RULES (palette lock, branch policy):
/Users/sistaseetaram/Desktop/Claude/claude_projects/MyPersonalBrand/CLAUDE.md
```

The wiki concept pages (`setu-visual-identity`, `setu-voice`, etc.) are the distillations. The on-demand files above are the raw originals — read them only when the distillation doesn't have enough detail.

## Reference map (design tasks)

| Need | Read |
|---|---|
| Color palette, opacity rule | `references/palette.md` (this skill) OR `setu-visual-identity` wiki concept |
| Fonts, scale, label spec | `references/typography.md` (this skill) |
| Positioning, audience, voice | `personal-brand-wiki/wiki/concepts/setu-voice.md` + `setu-positioning.md` |
| Hard NO list | `references/forbidden.md` (this skill) |

## Self-Improvement Loop

After using this skill:
1. If a wiki concept page is stale or wrong → update the wiki page. Do NOT update this SKILL.md with brand facts.
2. If a file path changed → update the on-demand file list above.
3. If a trigger phrase missed → add to description.
4. If a new locked decision (color, font, asset) → add to `personal-brand-wiki/wiki/concepts/setu-visual-identity.md`, then also to `references/palette.md` if design-token-level.
