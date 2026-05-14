# 01. Echo Information Inflow

Echo treats every input as evidence first. It does not assume that one device, one app, or one account is the center of the system.

## Input Sources

Echo should eventually accept controlled local inputs from:

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
future_wearable_stream
future_location_export
```

Early versions should not ingest everything automatically. The first deployable runtime only uses fake data and manually created evidence packets.

## Inbox Rule

All inputs first become inbox items:

```yaml
inbox_item:
  id:
  source_category:
  original_path:
  ingested_at:
  basic_type:
  review_state: inbox
  sensitivity:
  sync_permission:
```

The inbox layer should preserve the source and defer semantic judgment. Echo should not convert a file, email, or screenshot into a long-term memory until there is evidence, citation, and review.

## Evidence Packet

High-value evidence is wrapped in a small packet:

```yaml
evidence_packet:
  packet_id:
  original_ref:
  meta_ref:
  text_or_ocr_ref:
  preview_ref:
  redacted_ref:
  packet_status:
  sensitivity:
```

The packet is not a replacement for the original file. It is a navigation bundle that helps Echo connect candidates, citations, and review results back to the source.

## Current Runtime Example

The current dry run uses one fake financial evidence file:

```text
runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
```

Its packet sidecar is:

```text
runtime/truth/sidecars/ep_fake_bill_001.meta.json
```

This proves the shape of the inflow without touching real personal data.
