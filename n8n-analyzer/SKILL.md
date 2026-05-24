---
name: n8n-analyzer
description: Fetches workflows from any n8n instance (Railway, cloud, local) via Python REST API client. Lists available workflows, lets user select which to analyze, generates a named summary report with expert AI automation review, saves locally and uploads to Google Drive.
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

Fetch workflows from any n8n instance → let user select which to analyze → produce named summary report with expert review → save locally + upload to Google Drive.

**Tool used:** Python scripts in `tools/analyzer/` via n8n REST API.

---

## Step 1: Instance Selection

Check if current project `.env` has credentials:

```bash
cat /Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills/.env 2>/dev/null | grep -E "N8N_BASE_URL|N8N_API_KEY" | sed 's/=.*/=<set>/'
```

Present to user:
> "Instance found: `<N8N_BASE_URL value>`. Use this instance, or provide a different URL + API key?"

Also ask:
> "What should I call this instance? (used in filename — e.g. `railway`, `cloud_nation`, `rapid_api`)"

If user provides a different URL + API key for this session:
- Set `N8N_BASE_URL` and `N8N_API_KEY` as env vars inline for the Python commands — do NOT write them to `.env` or display them in chat
- Use instance name as provided by user

**Security:** Never echo API key values in chat. Confirm only with `KEY=<set>`.

---

## Step 2: Fetch Workflow List

```bash
# CLI-first (preferred)
n8n-cli workflow list --format=json > /tmp/workflows.json
```

Fallback (if n8n-cli unavailable or different instance):
```bash
cd /Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills
python3 tools/analyzer/fetch_all_workflows.py
```

Then display a numbered selection menu from `/tmp/workflows.json` (or `.tmp/workflows.json`):

```
Workflows on <instance_name>:
  1. [Workflow Name] — ACTIVE
  2. [Workflow Name] — INACTIVE
  3. [Workflow Name] — INACTIVE
  ... (all workflows)

Which would you like to analyze?
→ Enter numbers (e.g. 1,3,5), a range (1-4), or "all"
```

Wait for user selection before proceeding. Only analyze the selected workflows.

---

## Step 3: Fetch Full Details (selected only)

Fetch full node+parameter JSON only for selected workflows:

```bash
# CLI-first (preferred) — one command per selected ID
for id in <selected_ids>; do
  n8n-cli workflow get "$id" --format=json
done
```

Or fetch into a combined file:
```bash
python3 -c "
import subprocess, json, sys
ids = sys.argv[1:]
details = [json.loads(subprocess.check_output(['n8n-cli','workflow','get',i,'--format=json'])) for i in ids]
json.dump(details, open('/tmp/workflows_selected.json','w'), indent=2)
print(f'Fetched {len(details)} workflows')
" <id1> <id2> ...
```

Fallback (if n8n-cli unavailable):
```bash
cd /Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills
python3 -c "
import json, sys, warnings, os
warnings.filterwarnings('ignore')
sys.path.insert(0, 'tools')
from shared.n8n_client import N8nClient

client = N8nClient()
workflows = json.load(open('.tmp/workflows.json'))
selected_ids = <ids from user selection>
selected = [wf for wf in workflows if wf['id'] in selected_ids]
details = [client.get_workflow(wf['id']) for wf in selected]
os.makedirs('.tmp', exist_ok=True)
json.dump(details, open('.tmp/workflows_selected.json','w'), indent=2)
print(f'Fetched {len(details)} workflows')
"
```

Then extract key fields via Python (do not read raw JSON — file can exceed 256KB):

```bash
python3 -c "
import json, warnings
warnings.filterwarnings('ignore')

details = json.load(open('.tmp/workflows_selected.json'))
for wf in details:
    nodes = wf.get('nodes', [])
    node_types = list(set(
        n.get('type','').replace('n8n-nodes-base.','').replace('@n8n/n8n-nodes-langchain.','AI:').replace('@n8n/','')
        for n in nodes if n.get('type')
    ))
    connected_targets = set()
    for src, conns in (wf.get('connections') or {}).items():
        for output_key, output_list in (conns or {}).items():
            for targets in (output_list or []):
                for t in (targets or []):
                    if isinstance(t, dict):
                        connected_targets.add(t.get('node',''))
    trigger_nodes = [n for n in nodes if n.get('name') and n['name'] not in connected_targets]
    trigger_type = trigger_nodes[0].get('type','unknown').split('.')[-1] if trigger_nodes else 'unknown'
    print(f'=== {wf.get(\"name\")} ===')
    print(f'  Active: {wf.get(\"active\",False)}')
    print(f'  Nodes: {len(nodes)}')
    print(f'  Trigger: {trigger_type}')
    print(f'  Types: {chr(44).join(sorted(node_types))}')
    for n in nodes:
        ntype = n.get('type','').split('.')[-1]
        name = n.get('name','')
        params = n.get('parameters',{})
        key_params = {k:v for k,v in params.items() if k in ('prompt','text','subject','operation','resource','url','method','chatId','message','fromEmail','toEmail','query','systemMessage') and isinstance(v,str) and len(str(v))<120}
        print(f'  [{ntype}] {name}' + (f' -> {key_params}' if key_params else ''))
    print()
"
```

---

## Step 4: Analyze Each Selected Workflow

For each workflow, extract:
- Name + active status
- Trigger type (`webhook`, `schedule/cron`, `manual`, `event`, `sub-workflow`)
- Node count + unique node types (strip prefixes)
- Data flow: trigger → transformations → output

Understand from node names + types + parameters:
- What triggers it
- What data it reads/fetches
- What transformations happen
- Where output goes
- Whether error handling exists

---

## Step 5: Generate & Save Report

**Local output path:** `/Users/sistaseetaram/Desktop/n8n_resources/MyCloudWorkflows/Railway_workflow_analysis/`

**Filename format:** `<instance_name>_summary_report_YYYY-MM-DD.md`
Examples:
- `railway_summary_report_2026-05-21.md`
- `cloud_nation_summary_report_2026-05-21.md`
- `rapid_api_summary_report_2026-05-21.md`

If same filename exists, append `_v2`, `_v3`.

```bash
mkdir -p /Users/sistaseetaram/Desktop/n8n_resources/MyCloudWorkflows/Railway_workflow_analysis
```

Write report to file using the Write tool. Also display inline.

**Report format:**

```markdown
# N8N Instance Report — <Instance Name>
Generated: YYYY-MM-DD
Instance URL: <masked — show domain only, not full URL with tokens>
Workflows analyzed: X of Y total

---

## [Workflow Name] — [ACTIVE/INACTIVE]

**Trigger:** <type + details>
**Nodes:** X total | Services: <node type list>

**Summary**
<Full description — what it does, how it flows, what integrations it uses. No word limit. Write for a technical colleague who hasn't seen this workflow.>

**Expert AI Automation Review**
<As an AI automation expert with deep n8n experience:
- What was done well
- What could be improved (error handling gaps, fragile patterns, hardcoded values, missing retries)
- Opportunities to add AI/intelligence
- Best practice gaps
- One concrete next-step recommendation>

---
```

Repeat for each selected workflow. Then append:

```markdown
## Cross-Workflow Observations
<Only if 2+ workflows analyzed:
- Shared patterns or anti-patterns
- Inter-workflow dependencies
- Top 3 recommendations>
```

---

## Step 6: Upload to Google Drive

After local save, upload the report to Google Drive.

**Config:**
- OAuth client secret: `/Users/sistaseetaram/Documents/credentials/Gemini_API_OAuth/client_secret_web_client_2.json`
- Token cache: `/Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills/.tmp/gdrive_token.json`
- Drive folder ID: `10dWjCnfUkoFjznxQCzLLQkNwxCuVZiLO`

```bash
pip3 install --quiet google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

```bash
python3 -c "
import os, sys
sys.path.insert(0, 'tools')

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDS_FILE = '/Users/sistaseetaram/Documents/credentials/Gemini_API_OAuth/client_secret_web_client_2.json'
TOKEN_FILE = '/Users/sistaseetaram/Desktop/Claude/claude_projects/n8nAutomationAndSkills/.tmp/gdrive_token.json'
FOLDER_ID = '10dWjCnfUkoFjznxQCzLLQkNwxCuVZiLO'
REPORT_PATH = sys.argv[1]

creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, 'w') as t:
        t.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)
file_metadata = {'name': os.path.basename(REPORT_PATH), 'parents': [FOLDER_ID]}
media = MediaFileUpload(REPORT_PATH, mimetype='text/markdown')
result = service.files().create(body=file_metadata, media_body=media, fields='id,name,webViewLink').execute()
print(f'Uploaded: {result[\"name\"]}')
print(f'Drive link: {result[\"webViewLink\"]}')
" /Users/sistaseetaram/Desktop/n8n_resources/MyCloudWorkflows/Railway_workflow_analysis/<filename>.md
```

First run: browser OAuth flow opens once → token cached → all future runs silent.

Confirm to user:
> "Report saved locally and uploaded to Drive: <webViewLink>"

---

## Step 7: Self-Update

Append findings to **Applied Learning** below:
```
YYYY-MM-DD | <instance name> | <pattern/finding> | <future watch>
```

---

## Applied Learning

> Self-updating. Appended after each analysis run.

2026-05-21 | Railway instance (9 workflows) | 8 of 9 workflows inactive — project in prototype stage with high build investment but near-zero deployment | Check active/inactive ratio as project health signal
2026-05-21 | Railway instance | Duplicate workflows (Email Digest saved twice) — happens when workflow cloned without intent | Flag name collisions before reporting
2026-05-21 | Railway instance | Hardcoded placeholder values (user@example.com, YOUR_TELEGRAM_CHAT_ID) survive into deployed workflows — silent failures on activation | Grep for common placeholder strings in node parameters
2026-05-21 | Railway instance | Telegram is universal output channel (7/9 workflows) — mobile-first Telegram-centric UX is a strong consistent design choice
2026-05-21 | Railway instance | workflows_full.json was 2.4MB — too large to Read directly; always use Python extraction script, never raw file read
2026-05-23 | Railway instance | Workflow updates via PUT API fail with 400 Bad Request if read-only properties (id, meta, isArchived, etc.) or custom settings (availableInMCP) are present; payload must be sanitized to name, nodes, connections, settings (standard-only), staticData, pinData | Sanitize updates before calling API
