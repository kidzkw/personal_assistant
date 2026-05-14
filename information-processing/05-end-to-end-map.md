# 05. Echo End-To-End Map

This is the current end-to-end map for Echo's local-first personal memory workflow.

```mermaid
flowchart TD
  A["Inbox item"] --> B["Raw evidence / asset"]
  B --> C["Sidecar metadata"]
  C --> D["Evidence packet"]
  D --> E["Candidate item"]
  E --> F["Processing agent"]
  F --> G["processing_result"]
  G --> H["Audit agent"]
  H --> I["audit_result"]
  I --> J["Proposal agent"]
  J --> K["proposal_result"]
  K --> L["Secretary agent / 小秘"]
  L --> M["domain_event_summary_report"]
  M --> N["Orchestrator / 总管"]
  N --> O["ps_agent_work_log"]
  O --> P{"Human review needed?"}
  P -->|yes| Q["Review queue"]
  P -->|no, low risk only| R["Confirmed object"]
  Q --> S["confirm / correct / reject / archive"]
  S --> R
  R --> T["Search / timeline / reminders"]
  T --> U["Evidence pullback"]
```

## Serial Agent Rule

Each secretary agent can only run one active processing/audit/proposal chain at a time.

```text
active_chain_id != null
  -> no new chain

active_chain_id == null and next_spawn_allowed == true
  -> next chain may start
```

## Review Gate

The review gate is mandatory for:

```text
medical
financial
legal
account_security
identity
relationship
delete_or_merge_proposal
```

Low-risk generated artifacts can be automated only when they remain in working/cache layers.

## Evidence Pullback

Every important answer should be able to pull back to:

```text
file path
content hash
packet id
page / line / message / timestamp locator
citation ref
review result
work log entry
```

If Echo cannot explain why a memory was written or updated, the write is not valid.
