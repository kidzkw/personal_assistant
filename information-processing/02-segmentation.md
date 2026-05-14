# 02. Echo Segmentation

Echo should split inputs only as much as needed to preserve evidence and make review practical.

## Segmentation Units

Recommended units:

```text
raw_evidence
evidence_packet
content_chunk
email_message
attachment_asset
image_asset
transcript_segment_later
stream_event_later
candidate_item
confirmed_object
timeline_entry_projection
```

The first runtime does not implement automatic segmentation. It uses one fake evidence packet and hand-written JSON to validate the chain.

## Chunking Rules

When segmentation is added later:

- text and Markdown should split by heading or paragraph
- PDF should split by page and section
- email should preserve message and attachment boundaries
- screenshots and photos should preserve asset-level metadata first
- audio should split into transcript segments only after the text layer is reliable
- continuous streams should keep raw events separate from merged projections

## Scope And Aggregation

Every derived record should declare what level it belongs to:

```yaml
scope: asset | message | attachment | chunk | observation | relation | schedule | transaction | event | task
aggregation_level: atomic | thread | session | event_cluster | duplicate_cluster | daily_view
```

This prevents thread summaries, daily views, or duplicate clusters from overwriting atomic facts.

## Projection Boundary

Daily logs, timelines, map views, galleries, and summaries are projections. They are useful, but they are not the truth layer.

```text
raw evidence / confirmed objects
 -> projection entry
 -> daily timeline / domain timeline / export summary
```

If a projection cannot explain which evidence or object produced it, it is not valid.
