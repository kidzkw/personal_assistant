# 2026-05-13 12:21 EDT - Field Cardinality / Medical Views / Email Rules / Relationship Safety

本轮目标：沿着上次 memory 中留下的 TODO，补齐四个薄弱点：跨域字段的 `cardinality / merge_semantics`，医疗最小视图字段，邮件 thread ingest 规则，以及关系图谱的安全边界。仍然只做 information architecture 研究，不实现代码、不写数据库迁移、不做同步集成。

## Sources checked

- LinkML slots / cardinality: https://linkml.io/linkml/schemas/slots.html
- Logseq DB version properties: https://github.com/logseq/docs/blob/master/db-version.md
- HL7 FHIR R4 Observation: https://hl7.org/fhir/R4/observation.html
- HL7 FHIR R4 DiagnosticReport: https://hl7.org/fhir/R4/diagnosticreport.html
- HL7 FHIR R4 DocumentReference: https://hl7.org/fhir/R4/documentreference.html
- HL7 FHIR R4 Encounter: https://hl7.org/fhir/R4/encounter.html
- HL7 FHIR R4 MedicationStatement: https://www.hl7.org/fhir/R4/medicationstatement.html
- Notmuch initial tagging: https://notmuchmail.org/initial_tagging/
- Notmuch special tags: https://notmuchmail.org/special-tags/
- Monica personal CRM: https://github.com/monicahq/monica
- Reddit: Meerkat personal CRM: https://www.reddit.com/r/selfhosted/comments/1s5di3t/i_built_meerkat_a_crm_for_the_personal_life/
- Reddit: graph-based personal CRM request: https://www.reddit.com/r/selfhosted/comments/1sxa5qo/selfhosted_personal_crm_with_graphbased/
- Relaticle CRM for dynamic custom fields / per-field encryption pattern: https://github.com/relaticle/relaticle

## Pattern 1 - Field cardinality should be explicit, not implied by field name

**Found pattern**

LinkML makes field cardinality explicit with `required`, `multivalued`, `minimum_cardinality`, `maximum_cardinality`, and UML-style `0..1 / 1 / 0..* / 1..*`. Logseq's DB documentation points in the same direction from the PKM side: typed properties can be single-value or multi-value, and tags can behave like flexible types with inherited properties.

**Why it matters**

The current proposal already has `field_origin`, `field_authority`, and `field_merge_policy`, but it does not yet force each field to declare whether it is single-valued, multi-valued, ordered, append-only, or derived. Without this, a future rule engine cannot reliably decide whether to overwrite `occurred_at`, merge `tags`, take max sensitivity, or preserve multiple conflicting addresses.

**Recommended structural change**

Add a lightweight `field_contract` table/spec for important fields:

```yaml
field_contract:
  field_name:
  scope:
  cardinality: "1 | 0..1 | 0..* | 1..* | 0..n | 1..n"
  value_type:
  ordered: false
  merge_semantics:
  conflict_policy:
  default_review_state:
  sensitivity_floor:
  sync_floor:
  provenance_required: true
```

Suggested merge semantics vocabulary:

```text
replace_by_authority
append_unique
append_versioned
max_sensitivity
min_sync_permission
union_tags
intersect_permissions
manual_only
derive_only
no_merge_cluster_only
```

**Should it change current structure?**

Yes. This should be promoted to P0 because it stabilizes every later pipeline: photos, health, email, finance, relationships, and future streams all need the same answer to "can this field have more than one value and how do conflicts resolve?"

**Risk / tradeoff**

The risk is schema bloat. Keep it limited to cross-domain and high-risk fields first: identity, timestamps, sensitivity, sync permission, review state, entity refs, evidence refs, medical values, finance amounts, contact fields, and relationship edges.

## Pattern 2 - Medical minimum view should distinguish report, atomic observation, encounter, and document evidence

**Found pattern**

FHIR separates `DocumentReference` from clinical objects. `DiagnosticReport` groups observations and carries report-level timing / performer / conclusion. `Observation` is the atomic result/value layer. `Encounter` provides visit context. `MedicationStatement` is explicitly a statement about medication use and can be derived from supporting information, rather than being the same thing as a prescription/order/dispense event.

**Why it matters**

For personal DB use, scanned PDFs and portal screenshots should not be treated as medical facts by themselves. They are evidence. The system needs a minimum view that can answer "what happened during this visit?", "what were the lab values?", "which medication was reported active?", and "which document supports this?" without attempting full EHR implementation.

**Recommended structural change**

Promote P1-9 into a more concrete minimum field set:

```yaml
medical_document:
  evidence_id:
  document_type:
  subject_person_id:
  author_or_facility:
  service_period:
  document_date:
  security_label:
  presented_form_ref:
  review_state:

medical_encounter:
  occurred_at_or_period:
  facility:
  practitioner_refs:
  reason_refs:
  diagnosis_candidate_refs:
  document_refs:

diagnostic_report:
  status:
  code:
  subject_person_id:
  encounter_ref:
  effective_at_or_period:
  issued_at:
  performer:
  result_observation_refs:
  presented_form_ref:

medical_observation:
  observation_kind: "lab_result | vital | symptom | wearable | patient_reported"
  status:
  code:
  value:
  unit:
  reference_range:
  effective_at_or_period:
  encounter_ref:
  performer_or_source:
  derived_from_refs:

medication_statement:
  medication:
  status:
  effective_at_or_period:
  date_asserted:
  information_source:
  dosage_text:
  reason_refs:
  derived_from_refs:
```

**Should it change current structure?**

Yes, but as documentation/schema proposal only. The key change is not "use FHIR wholesale"; it is "use FHIR names to keep the minimum views aligned with the outside world."

**Risk / tradeoff**

Medical data is high-risk. All medical objects should default to `sensitivity=medical_high`, `sync_permission=local_only`, `review_state=review_required`, and `claim_state=candidate` unless manually confirmed or imported from a trusted structured source. This system must not do diagnosis, medication advice, insurance decisioning, or automatic deletion of medical evidence.

## Pattern 3 - Email ingest needs a two-stage new-message tag plus thread-level rollup

**Found pattern**

Notmuch recommends tagging new messages first, then running post-processing only over the new set. It also distinguishes special tags synchronized with Maildir flags (`unread`, `replied`, `flagged`, etc.) and automatic tags such as `attachment`, `signed`, and `encrypted`. This suggests a clean separation between ingest state, mail-client state, and personal-DB semantic labels.

**Why it matters**

Old inbox imports can contain years of noisy, sensitive, or stale data. A one-pass classifier that writes bills, contacts, tasks, and memories directly from email would create long-term contamination. The architecture should preserve raw messages and attachments while allowing staged review and rollups.

**Recommended structural change**

Add an `email_ingest_rule` convention:

```yaml
email_raw_message:
  message_id:
  thread_key:
  mailbox_account:
  folder_or_label_snapshot:
  header_hash:
  body_hash:
  mime_structure_ref:
  attachment_refs:
  mail_client_flags:
  ingest_tags: ["new"]
  semantic_candidates:

email_thread:
  thread_key:
  message_refs:
  participants:
  subject_normalized:
  occurred_range:
  rollup_labels:
  max_child_sensitivity:
  min_child_sync_permission:
  thread_review_state:
```

Rules:

- `ingest_tags` track pipeline state: `new`, `parsed`, `classified`, `reviewed`, `archived_only`.
- `mail_client_flags` mirror source mailbox state and should not be confused with semantic truth.
- `rollup_labels` are derived from child messages and attachments.
- Thread labels never overwrite message-level facts.
- Attachments become independent evidence assets, linked back to message and thread.

**Should it change current structure?**

Yes. This deepens P1-6 and should be paired with P0-6 `scope/aggregation_level`.

**Risk / tradeoff**

Thread rollups can over-broaden sensitivity. Use `max(child.sensitivity)` and `min(child.sync_permission)` at thread level. Encrypted/signed messages should preserve cryptographic status as metadata, but the system should avoid silently downgrading them into ordinary text chunks.

## Pattern 4 - Relationship graph should be consent-aware and field-level private

**Found pattern**

Monica and recent self-hosted personal CRM discussions converge on contacts, relationships, reminders, activities/interactions, notes, documents/photos, and custom fields. Reddit users asking for graph-based personal CRM want flexible long-term relationship accumulation, but existing tools are either too rigid, too CRM-like, or lack graph semantics. Relaticle adds a useful enterprise pattern for dynamic fields and per-field encryption, but its business CRM orientation is too broad for a personal DB.

**Why it matters**

Relationships are not just "people tags." They include third-party private facts, inferred ties, sensitive life context, and time-varying edges. If this graph later feeds an assistant, it can easily leak or overstate facts about other people.

**Recommended structural change**

Add relation-level safety fields:

```yaml
relationship_edge:
  from_person_id:
  to_person_id:
  relation_type:
  directionality: "directed | symmetric"
  claim_state: "candidate | confirmed | disputed | retracted"
  confidence:
  valid_from:
  valid_to:
  evidence_refs:
  visibility_scope: "self_only | household | explicit_share | never_share"
  consent_state: "unknown | self_asserted | shared_by_person | public | do_not_store"
  sensitivity:
  sync_permission:

person_profile_field:
  person_id:
  field_name:
  value:
  cardinality:
  source:
  field_sensitivity:
  field_sync_permission:
  review_state:
```

**Should it change current structure?**

Yes. P1-8 should explicitly include `consent_state`, `visibility_scope`, and per-field sensitivity/sync overrides. A person's birthday reminder and a private family conflict are both "relationship data," but they need very different retrieval and sync behavior.

**Risk / tradeoff**

More privacy fields mean more review overhead. The compromise is a simple default: relationship graph objects are `local_only`, `review_required`, and excluded from external sync/search unless explicitly allowed.

## Recommended category / label changes

- Add `field_contract.cardinality` and `field_contract.merge_semantics` as cross-domain IA terms.
- Add `medical_document`, `medical_encounter`, `diagnostic_report`, `medical_observation`, and `medication_statement` as medical semantic categories.
- Add email ingest labels: `new`, `parsed`, `classified`, `reviewed`, `archived_only`.
- Add relationship/privacy labels: `visibility_scope`, `consent_state`, `field_sensitivity`, `field_sync_permission`.
- Add default rollup policies: `max_child_sensitivity`, `min_child_sync_permission`.

## Proposed schema impact

Proposal-level only:

- New P0 item: `field_contract` for cardinality and merge semantics.
- Deepen P1-9 into a concrete FHIR-inspired medical minimum view.
- Deepen P1-6 with `email_ingest_rule`, separated `ingest_tags`, `mail_client_flags`, and `rollup_labels`.
- Deepen P1-8 with consent-aware relationship edges and field-level privacy.

## Confidence

Medium-high. LinkML, FHIR, Notmuch, and Monica are mature references. The exact field names should still be treated as IA proposals, not implementation-ready migrations.

## Privacy / safety considerations

- Medical, financial, legal, account-security, and relationship data should default to `local_only`, `review_required`, and evidence-backed candidates.
- Relationship facts can harm third parties if over-shared or over-inferred; use consent and visibility fields even in a local-first system.
- Email thread rollups must inherit the strictest child sensitivity/sync policy.
- Field contracts should include redaction behavior for routing indexes and exported views.

## Investigate next

- Turn `field_contract` into a one-page table for the highest-value fields.
- Draft a medical minimum-view field matrix with source evidence and review defaults.
- Write example email ingest rules for bills, receipts, account security notices, travel bookings, and archive-only newsletters.
- Research privacy-preserving graph retrieval: how to answer relationship questions while hiding third-party sensitive details by default.
