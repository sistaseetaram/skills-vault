---
name: n8n-analyzer
description: Fetches all workflow JSON from a remote n8n instance (Railway or any hosted) via existing Python REST API client, analyzes what each workflow does, and generates a project summary report with expert AI automation review. Produces both a plain-English summary and an expert opinion on architecture quality, improvement opportunities, and best practice gaps.
triggers:
  - "analyze my workflows"
  - "what workflows do I have"
  - "give me a project summary"
  - "summarize my n8n project"
  - "what does my n8n do"
  - "analyze n8n"
  - "workflow report"
  - "n8n project overview"
  - "review my automations"
---

# N8N Analyzer Skill

Fetch all workflows from the remote n8n instance (Railway) → analyze what each does → produce a project summary with expert AI automation review.

**Tool used:** Python scripts in `tools/analyzer/` via n8n REST API. Connects to any hosted instance — Railway, self-hosted, cloud.

---

## Step 1: Verify Environment

Check credentials are set:

```bash
cd /Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills
cat .env 2>/dev/null | grep -E "N8N_BASE_URL|N8N_API_KEY" | sed 's/=.*/=<set>/'
```

Required env vars in `.env`:
- `N8N_BASE_URL` — Railway URL (e.g. `https://your-app.railway.app`)
- `N8N_API_KEY` — from n8n Settings → API Keys

If missing, stop and ask user to set them in `.env` before continuing.

---

## Step 2: Fetch All Workflows

```bash
cd /Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills
python3 tools/analyzer/fetch_all_workflows.py
```

This calls the Railway n8n REST API (`GET /api/v1/workflows`) and saves results to `.tmp/workflows.json`.

If the fetch fails (auth error, connection refused, etc.) — report the exact error and stop. Do not proceed with stale/missing data.

---

## Step 3: Fetch Individual Workflow Details

The summary fetch may not include full node parameters. For complete analysis, fetch each workflow individually:

```python
# Run inline or as a quick script
import json, sys, os
sys.path.insert(0, 'tools')
from shared.n8n_client import N8nClient

client = N8nClient()
workflows = json.load(open('.tmp/workflows.json'))
details = []
for wf in workflows:
    full = client.get_workflow(wf['id'])
    details.append(full)

with open('.tmp/workflows_full.json', 'w') as f:
    json.dump(details, f, indent=2)
print(f"Fetched full details for {len(details)} workflows")
```

Run via:
```bash
cd /Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills
python3 -c "
import json, sys
sys.path.insert(0, 'tools')
from shared.n8n_client import N8nClient
client = N8nClient()
workflows = json.load(open('.tmp/workflows.json'))
details = [client.get_workflow(wf['id']) for wf in workflows]
import os; os.makedirs('.tmp', exist_ok=True)
json.dump(details, open('.tmp/workflows_full.json','w'), indent=2)
print(f'Fetched {len(details)} workflows')
"
```

Read `.tmp/workflows_full.json` — this is the full analysis input.

---

## Step 4: Analyze Each Workflow

For each workflow object in the full JSON:

**Extract:**
- `name` and `active` (true/false)
- **Trigger node** — node with no incoming connections, or type containing `Trigger`, `Webhook`, `Schedule`, `Cron`, `ManualTrigger`
- **Trigger type** — `webhook`, `schedule/cron`, `manual`, `event`, `sub-workflow`
- **Node count** and **unique node types** (strip `n8n-nodes-base.` prefix)
- **Data flow** — trace connection path from trigger → final output node(s)

**Understand the workflow** from node names + types + parameters:
- What triggers it
- What data it reads/fetches
- What transformations happen
- Where output goes
- Whether error handling exists

---

## Step 5: Generate Report

**Output path:** `/Users/sistaseetaram/Desktop/n8n_resources/MyCloudWorkflows/`

Filename format: `YYYY-MM-DD_n8n-railway-analysis.md` (e.g. `2026-05-21_n8n-railway-analysis.md`)

Create directory if missing:
```bash
mkdir -p /Users/sistaseetaram/Desktop/n8n_resources/MyCloudWorkflows
```

Write the full report to that file AND display it inline. After writing:
```bash
echo "Report saved to /Users/sistaseetaram/Desktop/n8n_resources/MyCloudWorkflows/$(date +%Y-%m-%d)_n8n-railway-analysis.md"
```

**Report format:**

```markdown
# N8N Project Analysis Report
Generated: <date>
Instance: <N8N_BASE_URL value> (Railway)

## Project Overview
- Total workflows: X
- Active: X / Inactive: X
- Trigger types: webhook (X), schedule (X), manual (X), event (X)

---

## Workflows

### [Workflow Name] — [ACTIVE/INACTIVE]

**Trigger:** <type + details>
**Nodes:** X total | Services: <node type list>

**Summary**
<Full description — what it does, how it flows, what integrations it uses. No word limit. Write for a technical colleague who hasn't seen this workflow.>

**Expert AI Automation Review**
<As an AI automation expert with deep n8n experience:
- What was done well (architecture, node choices, flow design)
- What could be improved (error handling gaps, fragile patterns, hardcoded values, missing retries)
- Opportunities to add AI/intelligence (LLM nodes, classification, summarization, dynamic routing)
- Best practice gaps (naming, missing documentation nodes, no monitoring, etc.)
- One concrete next-step recommendation>

---
```

Repeat for every workflow. Then append:

```markdown
## Cross-Workflow Observations

<Patterns across all workflows:
- Common node types used
- Shared architectural patterns or anti-patterns
- Workflows that depend on each other
- Overall project maturity
- Top 3 recommendations to improve the automation stack>
```

---

## Step 6: Self-Update

After generating the report, append findings to **Applied Learning** below:

```
YYYY-MM-DD | <project context> | <pattern/finding> | <future watch>
```

---

## Applied Learning

> Self-updating. Appended after each analysis run.

<!--
Format:
YYYY-MM-DD | Project context | Pattern or finding | Future watch
-->
