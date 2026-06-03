---
version: 0.3.0
name: higgsfield-marketplace-cards
description: |
  Generate marketplace product image cards through Higgsfield: compliant
  main image, secondary product images, and A+ style content modules. Use when
  the user asks for marketplace listing images, product detail cards,
  secondary product images, product infographics, lifestyle listing shots,
  A+ style content, marketplace image sets, or sales-ready product visuals.
  Backend owns marketplace compliance references and prompt templates; this skill
  only routes user intent to the CLI.
  NOT for generic brand product photography without marketplace/listing context
  (use higgsfield-product-photoshoot), video generation or UGC ads (use
  higgsfield-generate), or Soul Character training (use higgsfield-soul-id).
argument-hint: "[--scope main|product-images|aplus|full-set] [prompt]"
allowed-tools: Bash
---

# Marketplace Cards

Create marketplace-ready product visuals with `higgsfield marketplace-cards create`.
The CLI first calls the backend enhancer, where marketplace rules and templates are kept private, then creates `nano_banana_2` jobs and prints result URLs.

## Bootstrap

1. If `higgsfield` is not on `$PATH`, install it by running the official installer with Bash: `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`.
2. If `higgsfield account status` fails with authentication errors, ask the user to run `higgsfield auth login`.

## UX Rules

1. Respond in the user's language.
2. Ask at most one concise confirmation question before running.
3. Prefer a product image. If the user provides only text or a URL, proceed only when the product details are clear.
4. Do not write final image-generation prompts yourself. Backend enhancement owns that.
5. Final answer should contain only the ready image URLs and short labels.

## Scope Selection

Use `--scope` when the user asks for a common bundle:

| Scope | Creates |
|---|---|
| `main` | 1 marketplace main image |
| `product-images` | main image + 5 secondary images |
| `aplus` | main image + 7 A+ modules |
| `full-set` | main image + 5 secondary images + 7 A+ modules |

Use repeated `--asset` only for custom subsets:

- `main_image`
- `infographic`
- `multi_angle`
- `detail_shot`
- `lifestyle`
- `whats_in_box`
- `aplus_hero_banner`
- `aplus_pain_points`
- `aplus_features`
- `aplus_ingredients`
- `aplus_efficacy`
- `aplus_how_to_use`
- `aplus_endorsement`

## Command

Build and run one `higgsfield marketplace-cards create` command from the user's request.

For common bundles, use `--scope <main|product-images|aplus|full-set>`, `--prompt "<short product and listing intent>"`, optional repeated `--image <path-or-upload-id>`, and optional context flags: `--product_context`, `--brand_context`, `--category`, `--visual_style`.

Examples to mirror when choosing arguments:

- Product images: `higgsfield marketplace-cards create --scope product-images --prompt "sparkling peach lemonade can for marketplace listing" --image ./can.png --category "beverage"`
- Full set: `higgsfield marketplace-cards create --scope full-set --prompt "premium skincare serum, clean clinical marketplace visual system" --image ./serum.jpg --brand_context "minimal white and sage palette"`
- Custom subset: repeat `--asset`, for example `--asset main_image --asset infographic --asset lifestyle`.
- Existing completed main image job: use `--main-job <completed_main_job_id>` with the requested secondary or A+ `--asset` values.

## Delivery

Print URLs with labels:

```text
Marketplace cards ready:
- Main image: https://...
- Infographic: https://...
- Lifestyle: https://...
```

Avoid JSON, job IDs, internal model names, or enhanced prompt text unless the user explicitly asks.

## The Self-Improvement Loop

Every failure is a chance to make the system stronger:
1. Identify what broke
2. Fix the tool or skill pattern
3. Verify the fix works
4. Update the workflow with the new approach
5. Move on with a more robust system

This loop is how higgsfield-marketplace-cards improves over time.

## Applied Learning

When something fails repeatedly, when the user has to re-explain, or when a workaround is found for a platform/tool limitation, add a one line bullet here. Keep each bullet under 15 words. No explanations. Only add things that will save time in future sessions.
