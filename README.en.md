# Echo Personal Assistant / Personal Memory Database

Echo is a local-first personal assistant and personal memory database experiment. The current goal is not to launch a cloud service or a complex multi-agent platform. The goal is to make the smallest inspectable loop work first:

```text
evidence -> sidecar -> candidate -> audit -> proposal -> review -> work log
```

The repository currently contains:

- design docs in `information-processing/` and `docs/`
- a runnable dry-run scaffold in `runtime/`

All included runtime data is fake. Do not commit real medical, financial, account-security, relationship, identity, or private files to this repository.

## Quick Start

Clone the repository and enter the root directory:

```powershell
git clone https://github.com/kidzkw/personal_assistant.git
cd personal_assistant
```

Run the dry run:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Expected output:

```text
DRY_RUN_OK
```

This means the fake packet chain is internally consistent:

- the evidence packet can find the original fake evidence
- the candidate remains reviewable
- the processing result points to the candidate
- the audit result requires human review for financial data
- the proposal result does not write confirmed truth
- `ps_agent_work_log.next_spawn_allowed=false` until review is complete

## Local Docker Server

The repository now includes a minimal Docker server for local validation. It does not ingest real personal data and does not run autonomous agents. It exposes the current dry-run workflow over HTTP.

Start it from the repository root:

```powershell
docker compose up --build
```

Then check:

```powershell
curl.exe http://localhost:8080/health
curl.exe http://localhost:8080/dry-run
```

Or open the browser dashboard:

```text
http://localhost:8080/
```

To send a small local-only note into Echo, use the dashboard's "Send Text To Inbox" form. The item is saved under `runtime/inbox/text/` and remains `review_state=inbox`; it is not confirmed memory.

API example:

```powershell
$body = @{
  title = "Test note"
  text = "Remember to review the fake bill workflow."
  sensitivity = "personal"
} | ConvertTo-Json -Compress

Invoke-RestMethod `
  -Uri http://localhost:8080/inbox/text `
  -Method Post `
  -ContentType "application/json; charset=utf-8" `
  -Body $body
```

List received inbox items:

```powershell
curl.exe http://localhost:8080/inbox
```

Expected `/dry-run` response includes:

```json
{
  "status": "ok",
  "message": "DRY_RUN_OK"
}
```

Stop it:

```powershell
docker compose down
```

Without Docker Compose:

```powershell
docker build -t echo-personal-assistant:local .
docker run --rm -p 8080:8080 echo-personal-assistant:local
```

## How To Use The Current Runtime

The current runtime is not a full application. It is a file-based dry-run scaffold that uses plain text and JSON to model one personal-memory processing chain.

Main entry points:

```text
runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
runtime/truth/sidecars/ep_fake_bill_001.meta.json
runtime/working/review_queue/candidate_bill_fake_001.json
runtime/working/agent_work_log/pswl_fake_finance_001.json
runtime/scripts/validate-dry-run.ps1
```

Read the chain in this order:

```text
1. Raw evidence
   runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt

2. Evidence packet sidecar
   runtime/truth/sidecars/ep_fake_bill_001.meta.json

3. Reviewable candidate
   runtime/working/review_queue/candidate_bill_fake_001.json

4. Processing result
   runtime/working/agent_work_log/processing_result_fake_001.json

5. Audit result
   runtime/working/agent_work_log/audit_result_fake_001.json

6. Proposal result
   runtime/working/agent_work_log/proposal_result_fake_001.json

7. Domain event summary report
   runtime/working/domain_reports/domain_event_summary_report_fake_001.json

8. PS work log
   runtime/working/agent_work_log/pswl_fake_finance_001.json
```

For now, creating another fake packet means manually copying the JSON shape. The next milestone is a tiny CLI that creates these packet chains for us.

## Agent Chain

The current agent flow is serial. Short-lived agents do not run independently or write durable truth.

```text
orchestrator / 总管
  -> assigns work item to secretary agent / 小秘

secretary_agent / 小秘
  -> starts one active processing/audit/proposal chain

processing_agent
  -> handles one small evidence packet
  -> returns processing_result

audit_agent
  -> checks processing_result, citations, scope boundary, and risk flags
  -> returns audit_result

proposal_agent
  -> generates review_result / update_proposal / no_action
  -> returns proposal_result

secretary_agent / 小秘
  -> creates domain_event_summary_report
  -> reports back to orchestrator / 总管

orchestrator / 总管
  -> updates ps_agent_work_log
  -> decides next_spawn_allowed
```

Important boundaries:

- `processing_agent` does not write the truth layer
- `audit_agent` does not make the final domain decision
- `proposal_agent` does not directly write confirmed memory
- the secretary agent summarizes the domain event
- the orchestrator owns the global work log and unlocks the next step
- medical, financial, legal, account-security, and relationship information defaults to `local_only` and `review_required`

## Repository Layout

```text
docs/
  Echo information-processing design notes and reference material

information-processing/
  personal memory workflow, candidate proposals, and research notes

runtime/
  current runnable dry-run scaffold
```

Runtime layout:

```text
runtime/
  truth/
    raw_evidence/        # original evidence or fake evidence
    sidecars/            # evidence packet metadata
    confirmed_objects/   # future confirmed memory objects
  working/
    review_queue/        # candidates waiting for review
    agent_work_log/      # processing/audit/proposal/work log
    domain_reports/      # secretary-to-orchestrator reports
  cache/
    ocr/                 # rebuildable OCR cache
    fts/                 # rebuildable search cache
  export/                # future export layer
  scripts/               # local commands
```

## Current Commands

Validate the dry run:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Check repository status:

```powershell
git status -sb
```

No install step is required yet.

## Current Status

Done:

- documentation scaffold
- local runtime folder layout
- fake financial evidence packet
- evidence packet sidecar
- candidate item
- processing/audit/proposal result examples
- domain event summary report
- PS agent work log example
- dry-run validation script
- minimal Docker server with `/health` and `/dry-run`
- local text inbox endpoint with `POST /inbox/text`

Not done:

- real inbox ingestion
- CLI for creating packets
- SQLite index
- OCR
- web UI
- real agent runner
- sync with Gmail, Google Calendar, Telegram, Hermes, or cloud storage
- production Docker packaging with real workers or OCR dependencies

## Roadmap

### Phase 0: Static Dry Run

Status: current.

Goal: make the memory workflow inspectable with fake data only.

Milestones:

- keep the fake evidence packet chain valid
- keep `validate-dry-run.ps1` passing
- refine JSON schemas while they are still cheap to change

### Phase 1: Tiny CLI

Goal: stop hand-writing every fake packet.

Planned commands:

```powershell
personal-db new-fake-packet --type bill
personal-db validate
personal-db show-work-log
personal-db list-review-queue
```

The first version can be PowerShell or Python. It should still write plain files, not a database-first system.

### Phase 2: SQLite Index

Goal: make lookup and review queue navigation easier without making SQLite the truth layer.

SQLite should index:

- evidence packets
- candidates
- processing/audit/proposal results
- PS work logs
- review queue status

Truth remains the file layer.

### Phase 3: Review Queue

Goal: make human review practical.

Needed behavior:

- list candidates
- show citation refs
- approve / correct / reject / archive
- keep review results traceable
- do not auto-confirm high-risk domains

### Phase 4: Real Ingestion

Goal: import controlled local files after the fake flow is boringly reliable.

Possible first ingesters:

- local text file
- local PDF metadata-only packet
- screenshot or image metadata packet
- email export packet

Still no automatic medical, financial, legal, or account-security decisions.

### Phase 5: Local App Or Backend

Goal: add a small local UI or API only after the file workflow is stable.

Possible stack:

- Python FastAPI
- Next.js local dashboard
- SQLite + FTS5
- local filesystem storage

### Phase 6: Docker Compose

Status: minimal local server scaffold exists.

Goal: package heavier dependencies only when there is something worth packaging.

Docker becomes more useful when we have:

- backend service
- worker process
- OCR dependency
- local search service
- repeatable development environment

Until then, Docker would mostly hide simple file behavior behind container volume permissions.

## Safety Rules

Do not commit real personal data.

Never commit:

- medical records
- financial statements
- legal documents
- credentials
- account-security notices
- private relationship notes
- identity documents
- real email exports
- real chat exports
- real photos with GPS/person metadata

Recommended local-only folders are ignored by git:

```text
runtime/local/
runtime/private/
runtime/inbox/
```

Use those folders later for real local experiments, but keep them out of GitHub.
