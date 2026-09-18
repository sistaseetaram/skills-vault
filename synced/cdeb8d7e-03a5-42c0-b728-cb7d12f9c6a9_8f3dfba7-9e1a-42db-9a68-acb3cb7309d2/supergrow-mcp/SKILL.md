---
name: supergrow-mcp
version: 0.2.0
description: >
  Use this skill whenever a user wants to do anything with Supergrow — creating LinkedIn posts,
  scheduling content, checking their calendar, managing drafts, scoring posts, Content DNA,
  analytics, knowledge base, or managing multiple workspaces as an admin.
  Triggers: "create a post", "draft a post", "schedule content", "what's on my calendar",
  "score this post", "check my drafts", "publish to LinkedIn", "content DNA", "writing style",
  "turn this into a post", "queue this", "my Supergrow workspace", "what's performing",
  "weekly report", "analytics", "knowledge base", "save this to my brain", "all my clients",
  "all workspaces", "aggregated report", "pipeline health", or any LinkedIn content request.
  This skill ensures Claude follows the correct tool call sequence and never guesses the order.
---

# Supergrow MCP Skill

Supergrow is a LinkedIn content creation and scheduling platform for individuals, ghostwriters,
and enterprise teams.

---

## Golden Rules (always apply)

1. **No topic? Go to Workflow 0.** If the user says something vague like "create me a post", "write something", or "help me with LinkedIn" — don't guess. Run Workflow 0 to suggest ideas based on their Content DNA, recent performance, and knowledge base. Let them pick a topic first.
2. **Get Content DNA first.** Call `get_content_dna` before writing or scoring any post.
3. **Fetch weekly reports before creating content.** `get_weekly_reports` tells you what's working — use it to shape format, hook, and angle.
4. **Search the KB before writing.** `kb_search(topic)` pulls the user's real stories, stats, and frameworks. This is what makes posts authentic.
5. **Generate questions before writing.** Use `questions_from_topic` or `questions_from_text` — always. Prefill answers from context; ask the user only for what you don't know. Present all questions at once.
6. **Don't write until you have answers.** Questions → answers → write. Non-negotiable.
7. **workspace_id is always required.** If missing, call `list_workspaces` — never ask the user to find it.
8. **Respect workspace language.** `list_workspaces` returns a `language` field (e.g. "English", "Hindi"). Always write posts in that language unless the user asks otherwise.
9. **Always share both links after saving a post.** `create_public_link` (LinkedIn preview, no signup needed) + `app_url` from the response (opens post in Supergrow editor).
10. **Always include `skill_version: "0.2.0"` in the arguments of every Supergrow tool call.** This literal must match `package.json#skillVersion`; the server uses it to track skill adoption. Clients that omit `skill_version` are treated as the pre-versioning baseline `0.1.0`.

---

## Quick Decision Tree

```
No idea what to post         → Workflow 0
Write a post from a topic    → Workflow 1
Turn a URL/video into a post → Workflow 2
Manage existing posts        → Workflow 3
Content calendar             → Workflow 4
Content DNA                  → Workflow 5
Score a post                 → Workflow 6
Analytics & reports          → Workflow 7
Knowledge base               → Workflow 8
Auto-plug comments           → Workflow 9
Attach media (image/video/PDF) → Workflow 10
Company page publishing      → Company Page Publishing
Admin / multi-workspace      → Admin Workflows A–D
```

---

## Workflow 0: Suggest Ideas (User Has No Topic)

```
1. get_content_dna
2. get_weekly_reports(limit=4)
3. list_posts(status=published)     → avoid repetition
4. list_posts(status=draft)         → avoid duplication
5. kb_list                          → KB items not yet posted = strong idea signals
6. Suggest 5–7 ideas → user picks one → go to Workflow 1
```

**Idea format** — vary formats, each needs a specific *angle* not just a topic:
```
💡 From your expertise
1. [Angle] — Format: Story

📈 Doubling down on what's performing
2. [Angle tied to recent top post] — Format: Question hook

🧠 From your knowledge base
3. [Angle from an unused KB item] — Format: List

🌱 Filling a gap
4. [Something not yet covered] — Format: Personal story
```
"Leadership" is a topic. "Why I stopped giving feedback in 1:1s" is an angle.

---

## Workflow 1: Create a Post from a Topic

```
1. get_content_dna
2. get_weekly_reports
3. kb_search(topic)
4. Brief insight to user: "Your last top posts were [X format]. I'll keep that in mind."
5. questions_from_topic(topic)
6. Prefill answers from KB + context; ask user only for unknowns (all at once)
7. Write post using answers + KB context + Content DNA + performance insights
8. score_post → refine if score < 7
9. create_post
10. create_public_link + share app_url
11. "Here's your preview: [link]. Open in Supergrow: [app_url]. Happy with it?"
12. If changes needed → update_post (preview link auto-updates)
13. Ask: queue_post / schedule_post / leave as draft
```

---

## Workflow 2: Turn a URL or Video into a Post

```
Step 1 — Extract:
  YouTube URL      → extract_youtube       (better transcript accuracy)
  Any other URL    → extract_content       (articles, PDFs, audio — limit: 10/day)

Step 2 — Continue:
2. get_content_dna
3. get_weekly_reports
4. kb_search(topic/theme from content)
5. questions_from_text(extracted content)
6. Prefill from extracted content + KB; ask user for their personal take (all at once)
7. Write post — the article gives facts; the answers give the authentic POV
8. score_post → refine if score < 7
9. create_post
10. create_public_link + share app_url
11. Ask: queue / schedule / leave as draft
```

---

## Workflow 3: Manage Existing Posts

```
Browse:
  get_kanban_board                          → all posts grouped by status
  get_kanban_column(status=...)             → single column (draft/under_review/approved/needs_changes/scheduled/published)
  list_posts(status=...)                    → flat filtered list

View:     get_post(post_id)                 → includes app_url
Edit:     get_post → update_post → score_post (recommended) → create_public_link
Publish:  publish_post                      → async, takes a few seconds
Preview:  create_public_link               → no-signup LinkedIn preview
Remove:   delete_public_link               → removes public access
Delete:   unschedule_post first if scheduled → then delete_post
```

---

## Workflow 4: Content Calendar

```
get_weekly_calendar(offset=0/1/-1)         → current / next / last week
get_monthly_calendar(offset=0)             → current month

Reschedule: unschedule_post → schedule_post or queue_post
```

**schedule_post required fields:** year, month, day_of_the_month, day_of_week (0=Sun), hour (0-23), minute. Provide all six fields together; incomplete schedule requests fail validation.
**Timezone:** Pass `hour` in the workspace's local time — the API uses the workspace timezone, NOT UTC. Never convert to UTC. E.g. for 2 PM IST, pass `hour=14`.
Default recommendation: **Tue–Thu, 8–10am**. For hands-off: use `queue_post` instead.

---

## Workflow 5: Content DNA

```
get_content_dna                            → profile, tone, content patterns, audience
regenerate_content_dna                     → if empty or outdated (warn: takes a moment, needs LinkedIn connected)
```

---

## Workflow 6: Score a Post

```
1. get_content_dna
2. score_post(text)
3. Explain dimensions: Hook Quality · Clarity · Readability · Completeness · CTA · Originality · Grammar · Content DNA Alignment
4. Offer to improve it
```

---

## Workflow 7: Analytics & Performance

```
get_weekly_reports(limit=4)                → structured weekly summaries
get_metrics(metric=IMPRESSION/MEMBERS_REACHED/REACTION/COMMENT/RESHARE, period=last_30_days)
get_followers(period=last_30_days)         → follower count + growth trend
```

**Present as:** what's working → what's not → trend direction → follower insight → one recommendation.

Follower insight: flat growth + high impressions = reaching non-followers but not converting → suggest stronger CTA or profile-driven posts.

---

## Workflow 8: Knowledge Base

```
Add:     kb_ingest(content, title)         → returns status: processing (indexed async)
Browse:  kb_list(status=ready)             → filter by source_type: text/website/pdf/document/youtube/voice
View:    kb_get(item_id)
Search:  kb_search(query)                  → semantic search, returns chunks + insights (stats, quotes, milestones)
Delete:  kb_delete(item_id)               → permanent — confirm with user first
```

Good candidates to ingest: stories, frameworks, stats, past posts, meeting notes, voice transcripts, idea dumps.

**Proactively suggest ingesting** when user shares a compelling insight in chat:
> "That's a great story — want me to save it to your knowledge base for future posts?"

---

## Admin Workflows (Multi-Workspace)

Always start with `list_workspaces` to get all workspace IDs and names.

### A: Aggregated Performance Report
*"How are all my clients doing?"*
```
For each workspace (parallel): get_weekly_reports + get_metrics (all 5) + get_followers
```
Rank into tiers: 🏆 Top performer / ✅ On track / ⚠️ Needs attention / 🚨 Inactive (no posts in 7 days)
Surface: best performing format across accounts, most/least active workspace, recommended actions per workspace.

### B: Pipeline Health Check
*"Which clients have content ready? Who needs new drafts?"*
```
For each workspace: get_kanban_column for draft / under_review / approved / scheduled
```
Present as a table. Flag: 🚨 Empty pipeline / ⚠️ Backlog (drafts not moving) / ⚠️ Nothing scheduled.
Suggested cadence: run Workflow A + B together every Monday morning.

### C: Create Content for a Client
Same as Workflow 1/2, but:
```
list_workspaces → confirm target workspace with admin → proceed
```
**Always confirm the workspace first.** Wrong-account posts are the #1 agency risk.

### D: Follower Growth Comparison
*"Which accounts are growing fastest?"*
```
For each workspace: get_followers(last_30_days) + get_followers(previous_month)
```
Rank by MoM growth rate with absolute gain and trend indicator.

---

## Workflow 9: Auto-Plug Comments

Auto-plug comments are automatically published under a post after it goes live, with a configurable delay.
Cannot add comments to already-published posts.

```
Add:     create_auto_plug_comments(post_id, comments=[{text, post_after_time_unit, post_after_time_unit_count}])
         time units: "minutes", "hours", "days"
         Example: {text: "Link in bio!", post_after_time_unit: "minutes", post_after_time_unit_count: 5}
List:    list_auto_plug_comments(post_id)
Delete:  delete_auto_plug_comment(post_id, comment_id)  → cannot delete on published posts
```

**Suggest proactively** after creating or scheduling a post:
> "Want to add an auto-plug comment? E.g. a link, CTA, or follow-up question that posts automatically after your post goes live."

---

## Company Page Publishing

Posts can be published from a personal profile (default) or a LinkedIn company page.

```
get_company_pages                             → list connected company pages
create_post(..., linked_in_company_page_id)   → publish from company page
queue_post(..., linked_in_company_page_id)    → queue from company page
```

**When to use:** If the user says "post from my company page" or "publish as [Company Name]", call `get_company_pages` first to get the page ID.

---

## Workflow 10: Attach Media (Images / Video / Carousel PDF)

Posts attach media via `media_ids` — an array of confirmed MediaItem IDs. **Direct URLs are no longer accepted.** Every file must travel through the three-step upload flow before its ID can be referenced on a post.

### The three-step upload flow

```
1. create_media(workspace_id, content_type, file_name)
   → returns:
       {
         media_item: { id, ... },
         upload: {
           url,         // MinIO/S3 endpoint to POST to
           fields,      // Object: form fields that MUST all be sent in the multipart body
           key,         // Final object key (informational)
           expires_in,  // Seconds until the presigned URL stops working
           max_size     // Hard upload limit in bytes
         }
       }

2. The user (or their client) performs a multipart/form-data POST to `upload.url`:
   → Body is multipart with EVERY key/value from `upload.fields` as form fields,
     followed by the file binary as the `file` field (must be last).
   → This is the standard S3/MinIO presigned-POST policy — NOT a plain HTTP PUT,
     NOT raw bytes, NOT JSON.
   → A successful response is HTTP 204 (no body).
   → The MCP cannot perform this step; it must happen in the user's environment.

3. confirm_media(workspace_id, media_id)
   → media_id is the `media_item.id` from step 1.
   → Returns 200 once the file has actually landed in storage.
   → Returns 422 if storage has no object at that key (i.e. step 2 never happened or failed).

4. Pass the confirmed ID(s) in `media_ids` when calling create_post / update_post / queue_post.
```

### Reference: a working multipart upload (curl)

```bash
# After step 1 you have $UPLOAD_URL and a JSON object $FIELDS like
# {"key":"...","policy":"...","x-amz-signature":"...","x-amz-algorithm":"...",...}

curl -X POST "$UPLOAD_URL" \
  -F "key=$KEY" \
  -F "policy=$POLICY" \
  -F "x-amz-algorithm=$ALG" \
  -F "x-amz-credential=$CRED" \
  -F "x-amz-date=$DATE" \
  -F "x-amz-signature=$SIG" \
  -F "file=@/path/to/local/file.jpg"   # the file field MUST come last
```

In Node/TS the equivalent is `new FormData()` with each `upload.fields` entry appended, then the file blob appended last as `file`.

### When to use this workflow

- User says "add this image to the post", "attach a video", "make it a carousel", or shares a local file
- Slot in just before the `create_post` / `update_post` step in Workflow 1 / 2 / 3

### Per-type guidance

| Type | media_ids | Extra fields |
|------|-----------|--------------|
| Images | One ID per image, all in the array | — |
| Video | A single video MediaItem ID | optional `video_title` |
| Carousel | A single PDF MediaItem ID | `carousel_title` (required for carousels) |

### Size & format limits

- Images: 10MB · Documents (PDF): 25MB · Audio: 50MB · Video: 100MB
- `content_type` must be a real MIME type (e.g. `image/jpeg`, `image/png`, `application/pdf`, `video/mp4`)
- Honour `upload.max_size` if it is stricter than the type-level limit above

### Reuse existing media

```
list_media(workspace_id, media_type=image|video|audio|document)   → browse confirmed items
get_media(workspace_id, media_id)                                 → presigned read URL
```

If the user has uploaded the file before, reuse the existing `id` instead of creating a new MediaItem.

### Important constraints

- **The MCP cannot upload binary data.** Steps 1, 3, and 4 are MCP tool calls. Step 2 is a multipart HTTP POST that *must* be executed by the user or their client (CLI, browser, app code) — not by Claude. If the user only has a public URL and no local file, ask them to download it first.
- **Multipart, not PUT.** A plain `curl --upload-file` (PUT) or sending raw bytes will be rejected by MinIO. It must be `multipart/form-data` POST with all `upload.fields` plus a `file` part.
- **Always confirm before attaching.** A MediaItem ID returned by `create_media` is *pending* until `confirm_media` succeeds. Attaching an unconfirmed ID to a post will fail.
- **Order matters.** Do not call `create_post` with `media_ids` until every ID has been confirmed.
- **Presigned URLs expire.** Watch `upload.expires_in` (default ~3600s). If it lapses, call `create_media` again for a fresh upload target.

### Example sequence: post with two images and a video

The MCP tool calls (steps 1, 3, 4) are interleaved with binary uploads (step 2) that the user runs themselves:

```
1.  MCP:  create_media(ws, "image/jpeg", "hero.jpg")   → media_item.id=m1, upload={url,fields,...}
2.  USER: multipart POST hero.jpg to upload.url with all fields
3.  MCP:  confirm_media(ws, m1)
4.  MCP:  create_media(ws, "image/png", "chart.png")   → m2, upload=...
5.  USER: multipart POST chart.png
6.  MCP:  confirm_media(ws, m2)
7.  MCP:  create_media(ws, "video/mp4", "demo.mp4")    → m3, upload=...
8.  USER: multipart POST demo.mp4
9.  MCP:  confirm_media(ws, m3)
10. MCP:  create_post(ws, text, media_ids=[m1, m2, m3], video_title="Demo")
```

If the user is operating purely through a chat UI with no terminal, surface a short "here's the curl/JS snippet to run" alongside the `create_media` response so they can do step 2 themselves.
