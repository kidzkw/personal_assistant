# 03. Echo Data Labeling

Echo uses labels to make each memory object explainable: what it is, where it came from, how risky it is, who reviewed it, and whether it can leave the local machine.

## 1. Minimal Label Vector

Each evidence packet, candidate, and proposal should carry a small label vector:

```yaml
domain: finance
source_type: local_text_file
media_type: text
semantic_type: bill
sensitivity: financial
review_state: inbox
sync_permission: local_only
confidence: low
temporal_precision: month
```

The goal is not to make a perfect taxonomy. The goal is to make review and retrieval predictable.

## 2. Source Membership

Source membership records where the item belonged in the original source system.

Examples:

```yaml
source_membership:
  source_system: gmail_export
  source_label: Receipts
```

```yaml
source_membership:
  source_system: apple_photos
  album_name: Medical Receipts
```

Source labels are not the same as Echo semantic labels. A Gmail label, photo album, folder path, or chat thread is evidence context, not confirmed meaning.

## 3. Citation Refs

High-risk objects require citation refs before they can become confirmed memory.

Minimal citation ref:

```yaml
citation_refs:
  - ref_id: bill_line_001
    evidence_packet_id: ep_fake_bill_001
    locator_type: file_line
    locator: ev_fake_credit_card_bill_2026_05.txt#L1-L12
```

For now, locator precision can be coarse. Later it can become page number, bounding box, message id, attachment id, image region, or transcript time range.

## 4. Review Labels

Review labels describe the current decision state:

```text
inbox
candidate
needs_human_review
approved
rejected
archived
confirmed
superseded
```

High-risk domains default to `needs_human_review`:

```text
medical
finance
legal
account_security
relationship
identity
```

## 5. Agent Output Labels

Agent outputs should identify what stage produced them:

```text
processing_result
audit_result
proposal_result
domain_event_summary_report
ps_agent_work_log
```

These are working-layer records. They are not the truth layer.

## 6. Current View And History

Labels should distinguish current view from historical evidence:

```yaml
object_id: event_2026_tax_deadline
current_view:
  status: rescheduled
  date: 2026-05-20
history:
  - proposal_type: reschedule
    previous_date: 2026-05-15
    citation_refs:
      - calendar_export_001
```

An update proposal changes the current view only after review. It does not erase history.

## 7. Key Points

- Labels support review, safety, and retrieval.
- Source membership does not equal semantic meaning.
- Citation refs are required for high-risk confirmed memory.
- Agent outputs are working records, not truth.
- Current view is separate from object history.
