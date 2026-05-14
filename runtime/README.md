# Echo Runtime

This folder is the first local-first deployment scaffold for the personal memory database.

It is intentionally small:

- `truth/` stores durable source-of-truth artifacts and confirmed objects.
- `working/` stores review queues, agent work logs, and domain reports.
- `cache/` stores rebuildable OCR, FTS, embeddings, thumbnails, and other generated indexes.
- `export/` stores redacted or allowlisted output bundles.

Current deployment mode: local dry run only. No Docker, no cloud sync, no real medical/financial/account data.
The repository also includes a minimal Docker HTTP server for validating this dry run locally.

## Dry Run Flow

The included fake bill packet exercises the current agent chain:

```text
orchestrator -> secretary_agent -> processing_agent -> audit_agent -> proposal_agent -> secretary_agent -> orchestrator
```

Run validation:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Expected result:

```text
DRY_RUN_OK
```

## Docker Server

From the repository root:

```powershell
docker compose up --build
```

Available endpoints:

```text
GET /
GET /api
GET /health
GET /dry-run
GET /inbox
GET /memory/summary
POST /inbox/text
POST /inbox/file
```

Open the browser dashboard:

```text
http://localhost:8080/
```

The dashboard shows quick capture, the last 3 days of inbox records, and past-week highlights.

Check the dry run over HTTP:

```powershell
curl.exe http://localhost:8080/dry-run
```

Send a small local-only item to inbox from the browser dashboard. It supports direct text paste, typed text, file selection, drag/drop, and pasted screenshots/photos. Title/source/sensitivity are filled automatically.

Text API example:

```powershell
$body = @{
  text = "Remember to review this later."
} | ConvertTo-Json -Compress

Invoke-RestMethod `
  -Uri http://localhost:8080/inbox/text `
  -Method Post `
  -ContentType "application/json; charset=utf-8" `
  -Body $body
```

Inbox items are written to:

```text
runtime/inbox/text/
runtime/inbox/files/
```
