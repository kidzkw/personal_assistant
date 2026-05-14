# Echo Information Processing Design

This document describes Echo's current information-processing target. It is written as Echo's own design, not as a reference to another assistant product.

## Design Goal

Echo is a local-first personal assistant and memory database. Its job is to help preserve personal evidence, produce reviewable candidates, and keep every long-term memory traceable back to source material.

Echo should feel small, inspectable, and personally maintainable before it becomes automated.

## Core Loop

```text
inbox
 -> raw evidence / asset
 -> sidecar metadata
 -> evidence packet
 -> candidate extraction
 -> processing_result
 -> audit_result
 -> proposal_result
 -> human review
 -> confirmed memory object
 -> search / timeline / reminders
 -> evidence pullback
```

## Storage Layers

Echo separates durable truth from generated working material:

```text
truth   = original evidence, sidecars, confirmed memory objects
working = candidates, review queue, domain reports, agent work logs
cache   = OCR, FTS, embeddings, thumbnails, rebuildable indexes
export  = allowlisted and redacted output bundles
```

The file layer remains the source of truth. SQLite, FTS, vector indexes, and dashboards are projections or caches.

## Agent Roles

Echo uses information-processing roles, not unrestricted autonomous agents.

```text
orchestrator / æ€»ç®¡
  -> owns global classification, dispatch, work log, conflicts, next-step queue

secretary_agent / å°ç§˜
  -> long-lived domain steward, such as finance_secretary or health_secretary

processing_agent
  -> short-lived packet processor
  -> reads one evidence packet
  -> returns processing_result

audit_agent
  -> short-lived checker
  -> validates citations, scope boundary, contradictions, and risk flags
  -> returns audit_result

proposal_agent
  -> short-lived proposal writer
  -> returns review_result / update_proposal / no_action
  -> never writes confirmed truth directly
```

Only the orchestrator updates `ps_agent_work_log` and decides `next_spawn_allowed`.

## High-Risk Defaults

Medical, financial, legal, account-security, identity, and relationship data default to:

```text
sync_permission = local_only
review_required = true
```

Short-lived agents never directly write confirmed memory. High-risk candidates require citation refs and human review.

## First Runtime

The current runtime is intentionally simple:

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

Run the current validation from the repository root:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Expected output:

```text
DRY_RUN_OK
```

