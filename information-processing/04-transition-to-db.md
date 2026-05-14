# 04. Echo Transition To Persistent Objects

Echo should not jump directly from raw evidence to confirmed memory. It moves through reviewable intermediate records.

## Current File-First Path

```text
raw evidence
 -> evidence packet sidecar
 -> candidate item
 -> processing_result
 -> audit_result
 -> proposal_result
 -> domain_event_summary_report
 -> ps_agent_work_log
 -> human review
 -> confirmed object
```

## Candidate Before Confirmation

Automatic extraction can create candidates:

```text
memory_candidate
task_candidate
event_candidate
bill_candidate
receipt_candidate
medical_candidate
person_update_candidate
security_notice_candidate
photo_caption_candidate
duplicate_candidate
```

Candidates are reviewable working records, not confirmed truth.

## Confirmed Objects

After review, Echo can create confirmed objects such as:

```text
memory_observation
entity_relation
task
event
medical_record
finance_record
document_record
photo_event
account_notice
relationship_note
```

Every confirmed object must retain evidence refs. High-risk objects also need citation refs.

## SQLite Later

SQLite should be introduced as an index, not as the only source of truth.

It can index:

```text
evidence packets
candidates
processing/audit/proposal results
PS work logs
review queue status
confirmed object summaries
```

The file layer remains readable and portable even if SQLite is deleted and rebuilt.

## Current Runtime

The current runtime does not create confirmed objects. It stops at:

```text
proposal_result -> domain_event_summary_report -> ps_agent_work_log
```

For financial fake data, `next_spawn_allowed=false` until human review.
