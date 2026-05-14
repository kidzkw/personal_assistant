# 01. Echo Information Inflow

Echo treats every input as evidence first. The system should not jump directly from "new data arrived" to "confirmed memory". It first creates a small evidence packet that can be cited, reviewed, and reprocessed.

## 1. Input Sources

Initial supported source types:

```text
manual_note
local_text_file
pdf
image
screenshot
email_export
chat_export
calendar_export
future_audio
unknown
```

These source labels describe where evidence came from. They do not decide the final memory category.

## 2. Inbox Rule

Everything enters an inbox-like holding area first:

```text
runtime/inbox/          # future local-only real input, git ignored
runtime/truth/raw_evidence/
runtime/truth/sidecars/
```

For the current dry run, the fake raw evidence is committed because it contains no real personal data:

```text
runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
runtime/truth/sidecars/ep_fake_bill_001.meta.json
```

## 3. Evidence Packet

An evidence packet is a small wrapper around one source item or one carefully scoped slice of a source item.

Minimal fields:

```yaml
packet_id: ep_fake_bill_001
source_type: local_text_file
raw_evidence_ref: runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
sensitivity: financial
review_state: inbox
local_only: true
citation_refs:
  - ref_id: bill_text_full
    locator: file
```

## 4. First Processing Landing Point

The first durable output is not a memory. It is a reviewable candidate:

```text
evidence_packet
 -> candidate
 -> processing_result
 -> audit_result
 -> proposal_result
```

This keeps early extraction cheap to change. If the schema is wrong, we can reprocess from raw evidence instead of rewriting confirmed memory.

## 5. Current Dry Run

The current fake flow uses financial data because it forces the review gate:

```text
fake credit card bill
 -> evidence packet sidecar
 -> finance candidate
 -> processing_result
 -> audit_result requiring human review
 -> proposal_result with no confirmed truth write
 -> PS work log with next_spawn_allowed=false
```

## 6. Key Points

- Source type is not the same as semantic category.
- Raw evidence remains durable and citeable.
- High-risk domains default to local-only review.
- Inbox and working outputs are not truth.
- Every confirmed memory must be explainable from evidence refs.
