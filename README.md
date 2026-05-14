# Personal Assistant / Personal Memory Database

This repository contains the first local-first scaffold for a personal assistant memory system.

The current goal is not to deploy a cloud service or a full multi-agent platform. The goal is to make a small, inspectable personal database workflow that can preserve evidence, produce reviewable candidates, and keep every memory update traceable back to source material.

## Current Status

This is a documentation-first and dry-run-first repository.

Implemented so far:

- information architecture docs under `information-processing/`
- Omi information-processing analysis under `docs/`
- a local dry-run runtime under `runtime/`
- a fake finance evidence packet that exercises the current agent chain
- a PowerShell validation script that checks the dry-run references

Not implemented yet:

- real inbox ingestion
- OCR pipeline
- database migrations
- real agent runner
- Telegram / Google / email sync
- medical, financial, legal, or account-security automation
- Docker deployment

## Core Design

The system is local-first:

```text
inbox
 -> raw evidence / asset
 -> sidecar metadata
 -> evidence packet
 -> candidate extraction
 -> review gate
 -> confirmed memory object
 -> search / timeline / reminders
 -> evidence pullback
```

Sensitive domains such as medical, financial, legal, account security, and relationship data default to:

```text
sync_permission = local_only
review_required = true
```

## Agent Workflow

The current agent workflow is intentionally serial and lightweight.

```text
orchestrator / 总管
  -> assigns work item to secretary agent / 小秘

secretary agent / 小秘
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

secretary agent / 小秘
  -> creates domain_event_summary_report
  -> reports back to orchestrator / 总管

orchestrator / 总管
  -> updates ps_agent_work_log
  -> decides next_spawn_allowed
```

Short-lived agents never write confirmed memory or the truth layer directly. They only produce structured intermediate results. The secretary agent summarizes the domain event, and the orchestrator owns the global work log.

## Repository Layout

```text
docs/
  Omi and external information-processing analysis

information-processing/
  Current workflow docs, candidate proposals, and research notes

runtime/
  Local dry-run scaffold
```

Runtime layout:

```text
runtime/
  truth/
    raw_evidence/
    sidecars/
    confirmed_objects/
  working/
    review_queue/
    agent_work_log/
    domain_reports/
  cache/
    ocr/
    fts/
  export/
  scripts/
```

## Run The Dry Run

From the repository root:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Expected output:

```text
DRY_RUN_OK
```

The dry run uses fake financial data only:

```text
runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
```

The chain validates that:

- the fake evidence packet exists
- the candidate remains reviewable
- the processing result points to the candidate
- the audit result requires human review for financial data
- the proposal result does not write confirmed truth
- the PS work log keeps `next_spawn_allowed=false` until review

## Why No Docker Yet?

Docker is useful later, once the project has a real backend, worker, OCR stack, or local service dependencies.

For now the safest deployment path is:

```text
local files + JSON sidecars + dry-run validation
```

This keeps the early system easy to inspect and avoids hiding privacy-sensitive file permissions behind containers too early.

## Next Milestones

1. Add a tiny CLI for creating new fake packets.
2. Add a SQLite index for packet/work-log lookup.
3. Add a local review queue command.
4. Add real ingestion only after the fake chain is boringly reliable.
5. Add Docker Compose only after there is a backend or worker worth packaging.

## Safety Notes

Do not commit real personal evidence, medical records, financial records, credentials, account-security notices, or private relationship data to this repository.

The included runtime data is fake and exists only to test the workflow shape.
