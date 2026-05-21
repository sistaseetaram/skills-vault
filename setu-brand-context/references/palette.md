# Setu Palette — LOCKED

The palette is **closed**. No new colors. No derived tints. No "lighten this slightly."
Source of truth: `MyPersonalBrand/CLAUDE.md`. This file mirrors the locked subset.

## Locked Tokens (11)

| Token | Value | Use |
|---|---|---|
| `--setu-light-bg` | `#ffffff` | Light background (default canvas) |
| `--setu-light-fg` | `#111111` | Text on light |
| `--setu-paper-bg` | `#f2f2f0` | Off-white / paper background (LinkedIn, outreach) |
| `--setu-terracotta-bg` | `#1e0f09` | Terracotta dark background (signature hero) |
| `--setu-terracotta-fg` | `#f2ddd3` | Text on terracotta |
| `--setu-forest-bg` | `#0e1810` | Forest dark background (secondary dark) |
| `--setu-forest-fg` | `#ddeadf` | Text on forest |
| `--setu-anthracite-bg` | `#222222` | Neutral dark |
| `--setu-anthracite-fg` | `#f4f4f4` | Text on anthracite |
| `--setu-muted` | `#aaaaaa` | Muted labels |
| `--setu-rule` | `#e8e8e8` | Dividers, borders |

Founder mental model: **terracotta + dark forest + minimalist white. That is it.**

## Required Techniques (use instead of inventing tints)

- **Muted-on-dark text** → locked `*-fg` + `opacity: 0.6–0.8`. Never derive a hex.
- **Lighter / darker shade needed** → don't. Redesign the section to use a different locked surface.
- **Hover state with subtle contrast** → `opacity`, `text-decoration`, or `border` change. Not a new color.
- **Accent color** → there is no accent. Contrast comes from surface (light ↔ terracotta ↔ forest).
- **Higher contrast on a NEW surface** → bump opacity (e.g. `0.85`). Do NOT add a new gray hex.

## Grandfathered Exceptions — CLOSED LIST

These hex values pre-date the lock. Founder kept them after a 2026-05-20 mood-board review
(Option A: locked-fg + opacity equivalent read as visually pale in side-by-side). **This list
is closed. Do not extend. Do not introduce equivalents for other palettes.** Use locked-token +
opacity for anything new.

**Terracotta tints** (inside `.cta-band-terracotta`):
- `#d8c2b6` — terracotta body text
- `#b98e7a` — terracotta eyebrow label

**Neutral grays** (typography hierarchy on light surfaces):
- `#333` — `.lede` body color (big intro paragraph under H1)
- `#555` — `.bridge-line`, `.label` (eyebrow uppercase labels)
- `#666` — `.muted`, `.footer a` (secondary body, footer links, © line)
- `#ccc` — contact form input border

## Self-Check Before Any CSS Edit

Search the diff for any 3- or 6-digit hex not in the locked-tokens table above. If found:
- Is it in the grandfathered list and used on the same selector? → OK, leave.
- Anywhere else? → replace with locked token + opacity.

This rule has been violated once. Don't violate it again.
