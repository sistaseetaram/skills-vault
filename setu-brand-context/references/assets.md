# Setu Locked Assets, Live Surfaces, Stack

## Live Site

- **Production URL:** https://setuagency.com
- **www handling:** `https://www.setuagency.com/*` → `https://setuagency.com/${1}` (301 permanent, Cloudflare Redirect Rules wildcard, path + query preserved)
- **SSL:** active
- **SEO:** `<link rel="canonical">` and `og:url` rendered on every page

## Stack

- **Framework:** Astro
- **Images:** Astro Image optimization → WebP, source PNG/JPG live in `src/assets/` (NOT `public/`)
- **Hosting:** Cloudflare Pages
- **Repo:** github.com/sistaseetaram/MyPersonalBrand
- **Branch policy:** all website work on `main`. No long-lived feature branches. Codex branch is closed/merged — don't reopen.

## LinkedIn — Locked Assets

Base path: `MyPersonalBrand/setu-brand/03-collateral/assets/brand-kit/linkedin/`

| Asset | File | Notes |
|---|---|---|
| **Banner** | `banner/setu-linkedin-banner-selected.svg` (+ `.png`) | "Plain Minimal" variant — chosen by founder. Other variants (terracotta-dark, proof-led, v1-minimal) are archived, not active. |
| **Avatar** | `avatar/setu-linkedin-avatar-recommended.svg` (+ `.png`) | Recommended variant. `*-light` exists but is not the locked choice. |
| **Profile photo (LinkedIn)** | V2 Formal | Stored in collateral; do not swap. |
| **Profile photo (website About)** | Warm Alternate | Different from LinkedIn — intentional. |

## Founder Photo (Site)

- Optimised WebP, served via Astro Image from `src/assets/`
- 98% size reduction vs source PNG
- Do not move back to `public/` — breaks the optimization pipeline

## Planned (not shipped)

- **Setu Library subdomain** — separate scope, likely separate repo. Treat as future work, not current truth.

## Don'ts

- Don't introduce new LinkedIn variants without founder sign-off.
- Don't edit committed banner/avatar SVGs — regenerate cleanly.
- Don't add accent colors to banners. Locked palette only.
