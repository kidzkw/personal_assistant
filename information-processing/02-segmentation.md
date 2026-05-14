# 02. Echo Segmentation

Echo segmentation is about turning raw input into small, reviewable units. The unit should be small enough for a processing agent to handle without carrying a large private context.

## 1. Segmentation Layers

```text
raw evidence / asset
 -> evidence packet
 -> reviewable candidate
 -> object brief
 -> proposal / projection
```

## 2. Raw Evidence Or Asset

Raw evidence is the original file, text, export, screenshot, image, or future audio chunk. It should be preserved and referenced rather than rewritten.

Examples:

```text
credit card bill text
medical PDF
email export
chat transcript slice
screenshot
photo metadata
calendar export item
```

## 3. Evidence Packet

An evidence packet is the smallest useful processing unit.

Good packet boundaries:

- one bill
- one medical document
- one email or one email attachment
- one screenshot
- one calendar event export item
- one chat thread slice

Avoid giving a one-shot agent an entire mailbox, a full photo library, or a broad life summary.

## 4. Candidate

A candidate is a possible memory object or update waiting for review.

Candidate examples:

```text
possible_transaction
possible_subscription
possible_medical_visit
possible_relationship_interaction
possible_event_update
possible_account_security_notice
```

Candidates can be wrong. They are allowed to be incomplete as long as they carry citation refs and review state.

## 5. Object Brief

When new evidence may update an old object, the long-lived secretary agent should provide a small object brief, not the full object history.

Minimal object brief:

```yaml
object_id: subscription_netflix
current_view:
  status: active
  amount: 19.99
  billing_cycle: monthly
known_uncertainties:
  - amount changed recently but not confirmed
recent_citation_refs:
  - ref_id: bill_2026_04_line_12
```

The processing agent compares the new evidence packet to this brief and returns a scoped result.

## 6. Projection Boundary

Daily logs, timelines, dashboards, summaries, search indexes, OCR cache, FTS, and embeddings are projections or caches. They are not segmentation truth.

```text
confirmed objects + evidence refs
 -> timeline projection
 -> daily working summary
 -> export bundle
```

## 7. Key Points

- One processing agent gets one small packet.
- Segmentation favors reviewability over completeness.
- Object history is preserved; current view is generated from reviewed state.
- Projections are rebuildable and do not replace evidence.
