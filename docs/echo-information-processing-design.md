# Echo Information Processing Design

This document describes Echo's current information-processing target. It is written as Echo's own design, not as a reference to another assistant product.

## Design Goal

Echo is a local-first personal assistant and personal memory database. Its first deployment target is intentionally small: local files, JSON sidecars, fake evidence, and a validation script.

The system should make this question easy to answer:

```text
Why was this memory written or updated?
```

## Core Chain

```text
raw evidence
 -> evidence packet
 -> candidate
 -> processing_result
 -> audit_result
 -> proposal_result
 -> domain_event_summary_report
 -> ps_agent_work_log
 -> human review
 -> confirmed memory object
```

## Agent Roles

```text
orchestrator / 总管
  Owns global classification, work assignment, PS work log, and next_spawn_allowed.

secretary_agent / 小秘
  Owns one domain queue and may run only one active child chain at a time.

processing_agent
  Handles one small evidence packet and returns processing_result.

audit_agent
  Reviews the processing result for citations, scope, safety, and risk.

proposal_agent
  Converts the audited result into review_result, update_proposal, or no_action.
```

## Safety Boundary

Short-lived agents do not write confirmed truth. Medical, financial, legal, account-security, identity, and relationship data defaults to `local_only` and `review_required`.

## Current Runtime

The current runtime validates one fake financial packet:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Expected output:

```text
DRY_RUN_OK
```
