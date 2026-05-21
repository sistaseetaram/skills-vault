---
name: n8n-builder
description: Orchestrates end-to-end n8n workflow creation using MCP-first approach (Nate's methodology). Triggers on requests to build, create, or automate workflows. Encodes 6-step build process: clarify → templates → nodes → build → validate → deploy.
triggers:
  - "build a workflow"
  - "create a workflow"
  - "create workflow"
  - "automate this in n8n"
  - "make a workflow"
  - "new workflow"
  - "build me a"
  - "set up automation"
  - "n8n workflow for"
---

# N8N Builder Skill

Encode Nate's 6-step MCP-first workflow building process.

---

## Step 1: Clarify

**Goal:** 95% confidence before touching any MCP tool.

Ask ONE question at a time. Do not dump all questions at once.

**Required clarity on:**
- Trigger type: webhook, cron schedule, event (email/Slack/etc), manual, or another workflow
- Data sources: which services (Gmail, Sheets, Slack, HTTP, database, etc.)
- Authentication: which services need credentials — does user have them configured in n8n?
- Error handling: notify on failure? retry? stop silently?
- Output format: create record, send message, update sheet, return HTTP response, etc.

**Confidence check:** If < 95% confident → ask next clarifying question. Do NOT proceed to Step 2.

---

## Step 2: Search Templates

Before building from scratch, search community templates.

```
search_templates("<primary use case>")
search_templates("<service 1> <service 2>")
search_templates("<trigger type> <service>")
```

- If good template found: use `get_template` → adapt to user's requirements → skip to Step 5
- If no match: proceed to Step 3

---

## Step 3: Research Nodes

For each service/action needed:

```
search_nodes("<service name>")        # e.g. "gmail", "slack", "http request"
search_nodes("<action>")              # e.g. "schedule trigger", "webhook", "set"
```

For each node to use:
1. Note the discriminators in search results (resource, operation, mode)
2. `get_node("<nodeId>", discriminators)` — get exact TypeScript parameter schema
3. Invoke **n8n-node-configuration** skill for configuration guidance

**Critical:** Never guess parameter names. Always call `get_node` first.

---

## Step 4: Build

Use exact parameter names from `get_node` results.

Rules:
- Use `{{ $json.field }}` syntax for data references — invoke **n8n-expression-syntax** skill
- Use `{{ $('NodeName').item.json.field }}` to reference specific upstream nodes
- Invoke **n8n-workflow-patterns** skill for architectural decisions (branching, merging, error flows)
- Invoke **n8n-code-javascript** or **n8n-code-python** for Code node logic

Build checklist:
- [ ] All nodes have correct type + version
- [ ] All connections are wired (no orphan nodes)
- [ ] Expressions reference correct node names (case-sensitive)
- [ ] Credentials are named (not hardcoded values)
- [ ] Error handling path exists (if required)

---

## Step 5: Validate

```
n8n_validate_workflow(<workflow_code>)
```

- Zero errors required before deploy
- If errors: fix → re-validate (do not skip re-validation)
- If stuck on validation error: invoke **n8n-validation-expert** skill
- Common issues: wrong node version, missing required param, broken expression, disconnected node

---

## Step 6: Deploy

```
n8n_create_workflow(<validated_code>, description="<1-2 sentence summary>")
```

**NEVER activate automatically.** Always deploy inactive.

Post-deploy report format:
```
✓ Workflow created: [name]
  ID: <workflow_id>
  Status: INACTIVE (manual activation required)

Credentials needed before activation:
  - <Service>: <n8n credential type> (e.g. "Gmail: Gmail OAuth2")
  - <Service>: <n8n credential type>

To activate: open workflow in n8n → connect credentials → toggle Active
```

---

## Known Issues & Findings

> Self-updating. Add entry after each build with: date | workflow | lesson learned.

<!-- 
Format:
YYYY-MM-DD | Workflow Name | Issue/Finding | Resolution
-->
