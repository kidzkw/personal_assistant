# 04. Echo Transition To Persistent Memory

Echo should transition from evidence to persistent memory in stages. The current repository intentionally stops before automatic confirmed writes.

## 1. Current File-First Structure

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
```

`truth/` stores durable evidence and future confirmed objects. `working/` stores candidates, agent outputs, review queues, and reports. `cache/` is rebuildable.

## 2. Transition Path

```text
raw evidence
 -> evidence packet sidecar
 -> reviewable candidate
 -> processing_result
 -> audit_result
 -> proposal_result
 -> domain_event_summary_report
 -> ps_agent_work_log
 -> human review
 -> confirmed object
```

This shape makes every durable memory answerable:

```text
Why does Echo believe this?
Which evidence supports it?
Which agent processed it?
Which audit result checked it?
Who or what approved it?
```

## 3. Processing Result

The processing agent handles one evidence packet and returns extracted candidate meaning.

Minimal shape:

```json
{
  "result_type": "processing_result",
  "candidate_id": "candidate_bill_fake_001",
  "evidence_packet_id": "ep_fake_bill_001",
  "extracted_summary": "Fake credit card bill requires review.",
  "citation_refs": ["bill_text_full"],
  "recommended_next_step": "audit"
}
```

## 4. Audit Result

The audit agent checks whether the processing result is traceable and safe to use.

Minimal shape:

```json
{
  "result_type": "audit_result",
  "processing_result_id": "processing_result_fake_001",
  "audit_status": "requires_human_review",
  "risk_flags": ["financial_data"],
  "citation_check": "passed"
}
```

## 5. Proposal Result

The proposal agent turns the audited result into one of three outcomes:

```text
review_result
update_proposal
no_action
```

For high-risk data, a proposal may enter the review queue, but it must not write confirmed truth automatically.

## 6. Update Proposal Types

Update proposals should use explicit verbs:

```text
add_detail
correct_detail
reschedule
cancel
complete
split
merge
supersede
retract
```

These proposal types describe how current view may change after review. They do not erase history.

## 7. Future SQLite Index

SQLite can be added later as an index:

```text
evidence packets
candidates
processing/audit/proposal results
PS work logs
review queue status
```

SQLite should not become the only truth source at this stage. Files and citation refs remain inspectable.

## 8. Key Points

- The current runtime validates the shape, not real ingestion.
- Confirmed memory writes are intentionally gated.
- Working records explain the path from evidence to proposal.
- High-risk domains require human review.
- Cache, search, and embeddings are rebuildable.
