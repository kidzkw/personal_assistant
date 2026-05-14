# 03. Echo Data Labeling

Echo uses labels as routing and review aids. Labels are not truth by themselves.

## Minimal Label Vector

```yaml
domain: daily | photo | health | finance | email | relationship | admin | travel | account | other
media_type: text | pdf | image | screenshot | email | json | audio_later
semantic_type: note | bill | receipt | lab_result | visit | task | event | memory | contact | security_notice
sensitivity: normal | private | health | financial | legal | account_security | relationship
review_state: inbox | candidate | needs_review | confirmed | archived | rejected
sync_permission: local_only | summary_ok | task_calendar_ok
interpretation_level: raw | source_semantic | derived_candidate | reviewed_fact | projection
```

## Source Membership

Source folders, albums, labels, mailbox folders, and export batches should not be mixed with personal semantic labels.

Use `source_membership`:

```yaml
source_membership:
  canonical_ref:
  source_category:
  source_account_ref:
  source_label_or_folder:
  membership_type: source_folder | source_label | album | mailbox_folder | thread | collection | export_batch
  first_seen_at:
  last_seen_at:
  sensitivity:
  publish_policy:
```

This lets one asset appear in multiple source containers without duplicating the long-term semantic object.

## Review Labels

High-risk domains default to review:

```text
health
financial
legal
account_security
relationship
identity
```

Low-risk OCR, file previews, and fake dry-run data can remain automated as long as they do not become confirmed memory.

## Citation Labels

Candidates in high-risk domains require citation refs:

```yaml
citation_ref:
  evidence_ref:
  artifact_ref:
  locator:
  excerpt:
  extraction_method:
  confidence:
```

No citation means no confirmed memory.
