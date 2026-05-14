# 06. Global Workflowï¼ˆå¤šè½®è¿­ä»£åŽçš„ä¸ªäººæ•°æ®åº“æ€»æµç¨‹ï¼‰

è¿™ä»½æ–‡æ¡£è®°å½•å½“å‰ personal database / personal assistant information architecture çš„æœ€æ–°å…¨å±€ workflowã€‚å®ƒä¸æ˜¯ Echo åŽŸå§‹æµç¨‹çš„å¤è¿°ï¼Œè€Œæ˜¯åœ¨å¤šè½®ç ”ç©¶åŽï¼ŒæŠŠ Echoã€Paperless-ngxã€Immich/PhotoPrismã€Notmuch/afewã€FHIR/PHRã€Actual/Fireflyã€Monicaã€Basic Memory ç­‰æ¨¡å¼åˆå¹¶åŽçš„å½“å‰æ–¹å‘ã€‚

ä¸€å¥è¯ç‰ˆæœ¬ï¼š

```text
file-first inbox
 -> immutable evidence/assets
 -> sidecar metadata + provenance
 -> parse / OCR / chunk / segment
 -> contextualize chunks + build routing index
 -> scope-aware candidate extraction
 -> candidate verification
 -> review gate
 -> confirmed domain objects
 -> entity graph + timelines + indexes
 -> permission-aware retrieval
 -> controlled sync/actions/export
```

## 0. å½“å‰è®¾è®¡åŽŸåˆ™

å½“å‰ç³»ç»Ÿä¸æ˜¯ todo appï¼Œä¹Ÿä¸æ˜¯å•çº¯ PKMï¼Œè€Œæ˜¯ä¸€ä¸ª whole-life personal databaseã€‚

å®ƒè¦é•¿æœŸè¦†ç›–ï¼š

- ç…§ç‰‡ã€æˆªå›¾ã€PDFã€Markdownã€JSONã€é‚®ä»¶ã€é™„ä»¶ã€èŠå¤©å¯¼å‡ºã€‚
- å¥åº·è®°å½•ã€å°±è¯Šã€åŒ–éªŒã€å¤„æ–¹ã€ç—‡çŠ¶ã€ä¿é™©ã€åŒ»ç–—è´¦å•ã€‚
- è´¢åŠ¡è®°å½•ã€è´¦å•ã€è®¢é˜…ã€ç¨ŽåŠ¡ã€ä¿é™©ã€æ”¶æ®ã€ä»˜æ¬¾æé†’ã€‚
- äººé™…å…³ç³»ã€ç”Ÿæ—¥ã€å®¶åº­åŽ†å²ã€æœ‹å‹äº’åŠ¨ã€å…±åŒäº‹ä»¶ã€‚
- è´¦æˆ·ã€è®¾å¤‡ã€æˆ¿äº§ã€è½¦è¾†ã€æ—…è¡Œã€ç”Ÿæ´»è¡Œæ”¿æ–‡ä»¶ã€‚
- æœªæ¥éŸ³é¢‘ã€wearable streamsã€Telegram/Hermesã€Google syncã€‚

å› æ­¤åº•å±‚åŽŸåˆ™æ˜¯ï¼š

1. åŽŸå§‹è¯æ®ä¼˜å…ˆï¼Œä¸æŠŠ AI æ‘˜è¦å½“æˆçœŸç›¸ã€‚
2. æ–‡ä»¶ä¼˜å…ˆï¼Œæ•°æ®åº“å’Œç´¢å¼•æ˜¯è§†å›¾ï¼Œä¸æ˜¯å”¯ä¸€çœŸç›¸ã€‚
3. æ‰€æœ‰æ´¾ç”Ÿå¯¹è±¡å¿…é¡»èƒ½å›žæ‹‰ evidenceã€‚
4. é«˜é£Žé™©ä¿¡æ¯é»˜è®¤ candidateï¼Œä¸è‡ªåŠ¨ç¡®è®¤ã€‚
5. æ£€ç´¢å’ŒåŒæ­¥å¿…é¡» permission-awareã€‚
6. æ ‡ç­¾å¿…é¡»å£°æ˜Žä½œç”¨åŸŸï¼Œé¿å… threadã€assetã€chunkã€observation æ··åœ¨ä¸€èµ·ã€‚

## 1. File-first Inbox

æ‰€æœ‰è¾“å…¥å…ˆè¿›å…¥æ–‡ä»¶å¼ inboxï¼Œä¸æ€¥ç€è¿›å…¥æœ€ç»ˆ schemaã€‚

è¾“å…¥åŒ…æ‹¬ï¼š

- `photo`
- `screenshot`
- `pdf`
- `markdown`
- `json_export`
- `email_message`
- `email_attachment`
- `chat_export`
- `manual_note`
- `future_audio`
- `future_stream_event`

Inbox çš„èŒè´£ï¼š

- ä¿å­˜åŽŸå§‹æ–‡ä»¶æˆ–åŽŸå§‹ payloadã€‚
- è®°å½• `ingested_at`ã€`source_category`ã€`source_account_id`ã€`original_path`ã€‚
- æ‰“ä¸Šæœ€ä½Žé™åº¦æ ‡ç­¾ï¼š`review_state=inbox`ã€`processing_state=received`ã€‚
- ä¸åœ¨æ­¤é˜¶æ®µåšæ°¸ä¹…äº‹å®žç¡®è®¤ã€‚

## 2. Immutable Raw Evidence / Assets

è¿›å…¥ç³»ç»ŸåŽçš„åŽŸå§‹è¯æ®å°½é‡ä¸å¯å˜ã€‚

æ ¸å¿ƒå¯¹è±¡ï¼š

```text
raw_evidence
media_asset
email_raw_message
attachment_asset
document_asset
stream_raw_event
```

æœ€å°å­—æ®µï¼š

```yaml
id:
kind:
content_hash:
original_filename:
original_path:
mime_type:
size_bytes:
source_category:
source_account_id:
ingested_at:
occurred_at:
timezone:
retention_class:
sensitivity:
sync_permission:
```

è¦ç‚¹ï¼š

- `occurred_at` å’Œ `ingested_at` å¿…é¡»åˆ†å¼€ã€‚
- åŽŸä»¶ä¸ç›´æŽ¥å†™æ ‡ç­¾ï¼›æ ‡ç­¾ã€OCRã€captionã€ä¿®æ­£è®°å½•å†™ sidecarã€‚
- å¤§æ–‡ä»¶è¯æ®ä¸æ”¾è¿› Gitï¼›æ–‡æœ¬è§„èŒƒã€sidecarã€ç´¢å¼•æè¿°å¯ä»¥ Git åŒ–ã€‚

## 3. Sidecar Metadata + Provenance

sidecar æ˜¯è¯æ®å±‚å’Œç»“æž„å±‚ä¹‹é—´çš„æ¡¥ã€‚

ç…§ç‰‡ä¼˜å…ˆå…¼å®¹ XMPï¼›å…¶ä»–æ–‡ä»¶å¯ä½¿ç”¨ `*.meta.json` æˆ– Markdown frontmatterã€‚

sidecar éœ€è¦è®°å½•ï¼š

```yaml
id:
evidence_id:
labels:
provenance:
  document:
  record:
field_origin:
field_authority:
field_merge_policy:
processing_history:
review_state:
claim_state:
confidence:
evidence_refs:
```

å…³é”®æ¦‚å¿µï¼š

- `provenance.document`ï¼šåŽŸå§‹æ–‡ä»¶ä»Žå“ªé‡Œæ¥ã€‚
- `provenance.record`ï¼šå½“å‰æ ‡ç­¾ã€OCRã€æ‘˜è¦ã€å€™é€‰å¯¹è±¡æ˜¯è°ç”Ÿæˆçš„ã€‚
- `field_origin`ï¼šå­—æ®µæ¥è‡ª EXIFã€XMPã€OCRã€LLMã€æ‰‹å·¥è¾“å…¥ã€è§„åˆ™ç­‰ã€‚
- `field_authority`ï¼šå†²çªæ—¶è°æ›´å¯ä¿¡ã€‚
- `field_merge_policy`ï¼šè¦†ç›–ã€åˆå¹¶ã€å–æœ€é«˜æ•æ„Ÿåº¦ã€äººå·¥ç¡®è®¤ç­‰ã€‚

## 4. Parse / OCR / Chunk / Segment

ä¸åŒè¾“å…¥ç±»åž‹è¿›å…¥ä¸åŒåˆ‡åˆ†ç®¡çº¿ã€‚

```text
Markdown/text -> chunks
PDF -> pages + OCR regions + text chunks
photo/screenshot -> EXIF + OCR + visual labels + thumbnails
email -> message + thread + attachment
chat -> message + thread/session
audio later -> transcript segments + conversation/session
continuous streams later -> stream + event(timestamp, duration, payload)
```

åˆ‡åˆ†åŽçš„å¯¹è±¡å¿…é¡»å¸¦ï¼š

```yaml
parent_evidence_id:
chunk_id:
scope:
aggregation_level:
position:
timestamp:
text_or_payload_ref:
confidence:
```

`scope` æ˜¯å½“å‰è¿­ä»£åŽçš„å…³é”®å­—æ®µï¼š

```text
asset
message
thread
attachment
chunk
observation
relation
schedule
transaction
event
task
```

`aggregation_level` ç”¨æ¥è¯´æ˜Žè¿™ä¸ªå¯¹è±¡æ˜¯åŽŸå­å¯¹è±¡è¿˜æ˜¯èšåˆè§†å›¾ï¼š

```text
atomic
thread
session
event_cluster
duplicate_cluster
daily_view
```

## 5. Scope-aware Candidate Extraction

åœ¨ candidate extraction å‰ï¼Œç³»ç»Ÿåº”å…ˆä¸ºå¯æ£€ç´¢å†…å®¹ç”Ÿæˆè½»é‡æŠ½è±¡å±‚ï¼š

```text
chunks / messages / pages / sessions
 -> contextual_prefix
 -> context_routing_index
 -> sparse keys
```

è¿™å±‚å€Ÿé‰´ Claude/Anthropic çš„ contextual retrieval ä¸Ž layered memoryï¼šå¸¸é©»ä¸Šä¸‹æ–‡åªä¿ç•™è·¯ç”±ç´¢å¼•ï¼Œç»†èŠ‚æŒ‰éœ€åŠ è½½ï¼›chunk ä¸åªä»¥å­¤ç«‹æ–‡æœ¬è¿›å…¥ç´¢å¼•ï¼Œè€Œæ˜¯å¸¦ä¸Šå®ƒåœ¨æ•´ç¯‡æ–‡æ¡£ã€é‚®ä»¶ threadã€åŒ»ç–—æŠ¥å‘Šã€è´¦å•å‘¨æœŸæˆ–ç…§ç‰‡äº‹ä»¶ä¸­çš„ä½ç½®è¯´æ˜Žã€‚

æ–°å¢žå¯¹è±¡ï¼š

```yaml
context_routing_index:
  id:
  topic:
  domain:
  keywords:
  active_entities:
  status:
  sensitivity:
  sync_permission:
  detail_refs:
  last_touched_at:
  priority:

content_chunk:
  id:
  parent_evidence_id:
  raw_text_ref:
  contextual_prefix:
  document_outline_ref:
  section_path:
  entity_refs:
  date_refs:
  page_or_region:
  embedding_policy:
  bm25_text:
```

`contextual_prefix` æ˜¯æ£€ç´¢è¾…åŠ©æ–‡æœ¬ï¼Œä¸æ˜¯äº‹å®žçœŸç›¸ã€‚å®ƒå¿…é¡»å¯é‡æ–°ç”Ÿæˆï¼Œå¹¶ä¿ç•™ `generated_by`ã€`generated_at`ã€`source_prompt_version`ã€‚

AIã€OCRã€è§„åˆ™ã€æ–‡ä»¶åè§£æžã€é‚®ä»¶ header è§£æžéƒ½åªèƒ½å…ˆç”Ÿæˆå€™é€‰å¯¹è±¡ã€‚

å€™é€‰ç±»åž‹ï¼š

```text
memory_observation_candidate
entity_relation_candidate
task_candidate
event_candidate
finance_item_candidate
medical_item_candidate
relationship_edge_candidate
person_update_candidate
account_notice_candidate
security_notice_candidate
duplicate_group_candidate
photo_caption_candidate
```

å€™é€‰å¯¹è±¡å¿…é¡»æœ‰ï¼š

```yaml
id:
candidate_type:
scope:
aggregation_level:
claim_state: candidate
confidence:
evidence_refs:
created_by:
created_at:
review_state:
sensitivity:
sync_permission:
```

é‡è¦è§„åˆ™ï¼š

- AI ä¸ç›´æŽ¥åˆ›é€  confirmed memoryã€‚
- OCR ä¸ç›´æŽ¥åˆ›é€  confirmed transactionã€‚
- é‚®ä»¶ thread æ ‡ç­¾ä¸è¦†ç›–å•å° message çš„äº‹å®žã€‚
- duplicate cluster ä¸è‡ªåŠ¨åˆ é™¤ä»»ä½•åŽŸä»¶ã€‚
- åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€å…³ç³»ã€è´¦æˆ·å®‰å…¨é»˜è®¤éœ€è¦ reviewã€‚

## 6. Review Gate

åœ¨è¿›å…¥ review gate ä¹‹å‰ï¼Œé«˜é£Žé™©å€™é€‰å¯ä»¥å…ˆèµ°ä¸€å±‚ç»“æž„åŒ– verification passã€‚

```yaml
candidate_verification:
  candidate_id:
  verifier:
  checked_against_evidence_refs:
  contradiction_found:
  missing_evidence:
  confidence_delta:
  recommended_review_state:
  notes:
```

è¿™å±‚å€Ÿé‰´ DeepSeek-R1 çš„ self-verification / reflection å’Œ Claude long-running agent çš„ fresh-context evaluator æ€è·¯ã€‚å®ƒä¸èƒ½æ›¿ä»£äººå·¥ç¡®è®¤ï¼Œåªè´Ÿè´£æå‰æ ‡å‡ºè¯æ®ä¸è¶³ã€å†²çªã€ä½Žç½®ä¿¡ã€éœ€è¦ä¼˜å…ˆ review çš„å€™é€‰ã€‚

Review gate æ˜¯å½“å‰å…¨å±€ workflow çš„æ ¸å¿ƒæŽ§åˆ¶ç‚¹ã€‚

é»˜è®¤è¿›å…¥ review çš„å†…å®¹ï¼š

- åŒ»ç–—ã€å¥åº·ã€ç—‡çŠ¶ã€åŒ–éªŒã€å¤„æ–¹ã€‚
- è´¢åŠ¡ã€ç¨ŽåŠ¡ã€ä¿é™©ã€è´·æ¬¾ã€æŠ•èµ„ã€‚
- æ³•å¾‹ã€èº«ä»½ã€è´¦æˆ·ã€å®‰å…¨é€šçŸ¥ã€‚
- äººé™…å…³ç³»ã€å®¶åº­å…³ç³»ã€ç¬¬ä¸‰æ–¹éšç§ã€‚
- è‡ªåŠ¨ç”Ÿæˆçš„é•¿æœŸ memoryã€‚
- è‡ªåŠ¨ç”Ÿæˆçš„ entity relationã€‚
- é‡å¤æ–‡ä»¶åˆ é™¤å»ºè®®ã€‚

é€šç”¨çŠ¶æ€ï¼š

```text
review_state:
  inbox
  needs_review
  approved
  rejected
  corrected
  archived

claim_state:
  candidate
  confirmed
  disputed
  superseded
  retracted
```

æ‰€æœ‰ confirmed å¯¹è±¡éƒ½åº”è¯¥ä¿ç•™ï¼š

```yaml
reviewed_by:
reviewed_at:
review_reason:
evidence_refs:
validity:
  valid_from:
  valid_to:
  last_confirmed_at:
```

## 7. Confirmed Domain Objects

å®¡é˜…åŽè¿›å…¥é•¿æœŸæ ¸å¿ƒå±‚ã€‚è¿™é‡Œæ‰æ˜¯ assistant æ—¥åŽç¨³å®šä½¿ç”¨çš„ä¸»å¯¹è±¡ã€‚

### 7.1 Memory / Knowledge

é•¿æœŸè®°å¿†ä¸å†ç­‰äºŽ summaryï¼Œè€Œæ˜¯ï¼š

```text
memory_observation
entity_relation
memory_version
```

ç¤ºä¾‹ï¼š

```yaml
memory_observation:
  id:
  entity_refs:
  observation_type:
  content:
  claim_state:
  confidence:
  validity:
  evidence_refs:
  supersedes:
  conflicts_with:
  version_history_ref:
```

### 7.2 Email / Life Admin

é‚®ä»¶é‡‡ç”¨åŒå±‚ç»“æž„ï¼š

```text
email_message
 -> email_thread
 -> email_attachment
 -> derived_item
```

æ´¾ç”Ÿå¯¹è±¡åŒ…æ‹¬ï¼š

```text
bill_notice
receipt_notice
account_notice
security_notice
appointment_notice
deadline
contact_update
task
event
archive_only_evidence
```

thread sensitivity é‡‡ç”¨ `max(child.sensitivity)`ï¼Œä½†æ£€ç´¢æ—¶ä»æŒ‰ message/attachment è£å‰ªæƒé™ã€‚

### 7.3 Finance

è´¢åŠ¡ä¸ç›´æŽ¥ä»Ž OCR è¿›å…¥ transactionã€‚

æŽ¨èç»“æž„ï¼š

```text
financial_evidence
finance_item_candidate
transaction
subscription_or_bill_schedule
payment_deadline
reconciliation_link
```

`reconciliation_link` è¿žæŽ¥è¯æ®ã€å€™é€‰é¡¹ã€çœŸå®žäº¤æ˜“å’Œå‘¨æœŸä¹‰åŠ¡ï¼š

```yaml
finance_reconciliation_link:
  id:
  evidence_refs:
  candidate_item_id:
  transaction_id:
  schedule_id:
  match_confidence:
  amount_confidence:
  date_confidence:
  review_state:
```

### 7.4 Health / Medical

åŒ»ç–—é‡‡ç”¨ FHIR-inspired æœ€å°è§†å›¾ï¼Œä¸å®žçŽ°å®Œæ•´ EHRã€‚

æœ€å°å¯¹è±¡ï¼š

```text
medical_document
encounter
appointment
condition
observation.lab_result
observation.vital
observation.symptom
medication_statement
diagnostic_report
procedure
immunization
allergy_intolerance
claim
coverage
practitioner
organization
```

é»˜è®¤ç­–ç•¥ï¼š

```text
review_required = true
sync_permission = local_only
embedding_policy = none æˆ– summary_only_local
evidence_refs = required
```

ç³»ç»Ÿåªåšå½’æ¡£ã€æ—¶é—´çº¿ã€æ£€ç´¢ã€å°±è¯Šå‡†å¤‡ï¼Œä¸åšè¯Šæ–­ã€ç”¨è¯æˆ–ç†èµ”å†³ç­–ã€‚

### 7.5 People / Relationships

å…³ç³»åŸŸç‹¬ç«‹äºŽæ™®é€š memoryã€‚

æ ¸å¿ƒå¯¹è±¡ï¼š

```text
person_profile
relationship_edge
interaction
relationship_memory
relationship_reminder
```

å…³ç³»è¾¹ç¤ºä¾‹ï¼š

```yaml
relationship_edge:
  id:
  from_person_id:
  to_person_id:
  relationship_type:
  direction:
  confidence:
  claim_state:
  validity:
  evidence_refs:
  sensitivity:
  sync_permission: local_only
```

### 7.6 Photo / Media / Documents

ç…§ç‰‡å’Œæ–‡æ¡£ pipelineï¼š

```text
original asset
 -> EXIF/GPS/device/source folder
 -> thumbnail/preview
 -> OCR/caption/visual labels
 -> content hash + perceptual hash
 -> duplicate cluster
 -> event/date/place/person clustering
```

åŽ»é‡å¯¹è±¡ï¼š

```text
duplicate_group
representative_asset
stack_member
```

é‡è¦è§„åˆ™ï¼š

- ä¸è‡ªåŠ¨åˆ é™¤åŽŸä»¶ã€‚
- é«˜æ•æ„Ÿ metadataï¼ˆGPSã€äººè„¸ã€åŒ»ç–—/è´¢åŠ¡æ–‡æ¡£ç±»åž‹ï¼‰é»˜è®¤ä¸è‡ªåŠ¨åˆå¹¶ã€‚
- `original_path`ã€`display_folder`ã€`logical_collection` åˆ†ç¦»ã€‚

## 8. Entity Graph + Timeline + Indexes

confirmed objects è¿›å…¥å›¾è°±å’Œè§†å›¾å±‚ã€‚

Entity graph åŒ…æ‹¬ï¼š

```text
person
place
organization
account
device
project
vehicle
property
document
event
medical_provider
financial_institution
```

Timeline åŒ…æ‹¬ï¼š

```text
daily_timeline
medical_timeline
finance_timeline
relationship_timeline
travel_timeline
household_timeline
account_security_timeline
```

Indexes åŒ…æ‹¬ï¼š

```text
exact search
date search
metadata filters
FTS / BM25
vector search later
graph lookup
domain-specific indexes
```

Embedding ä¸æ˜¯é»˜è®¤å…¨é‡å¼€å¯ã€‚é«˜æ•æ„Ÿå†…å®¹ä¼˜å…ˆä¸ embedï¼Œæˆ–åªåšæœ¬åœ° summary embeddingã€‚

## 9. Permission-aware Retrieval

Assistant æ£€ç´¢æ—¶æŒ‰å±‚çº§é€æ­¥å±•å¼€ï¼š

```text
1. context_routing_index
2. confirmed objects
3. summaries / metadata / graph
4. contextualized chunks / OCR / thread
5. raw evidence pullback
```

æ£€ç´¢è¡¨ç¤ºæ‹†æˆä¸‰ç±»ï¼š

```text
latent_summary è´Ÿè´£å¬å›ž
sparse_keys è´Ÿè´£è¿‡æ»¤
exact_ref è´Ÿè´£è¯æ®å›žæ‹‰
```

è¿™æ˜¯ä»Ž DeepSeek-V3 MLA / sparse attention å¾—åˆ°çš„ç»“æž„å¯å‘ï¼šåŽ‹ç¼©è¡¨ç¤ºä¸æ›¿ä»£åŽŸå§‹è¯æ®ï¼Œç¨€ç–é€‰æ‹©åŽä»è¦èƒ½å›žæ‹‰ç²¾ç¡®åŽŸæ–‡ã€‚

æ¯ä¸€æ­¥éƒ½æ£€æŸ¥ï¼š

```text
sensitivity
sync_permission
embedding_policy
review_state
claim_state
retention_class
source evidence availability
```

å›žç­”é«˜é£Žé™©é—®é¢˜æ—¶ï¼Œå¿…é¡»èƒ½å›žæ‹‰è¯æ®ï¼š

- PDF é¡µç ã€‚
- OCR regionã€‚
- é‚®ä»¶ message idã€‚
- é™„ä»¶ hashã€‚
- ç…§ç‰‡ asset idã€‚
- åŒ»ç–— document referenceã€‚
- è´¢åŠ¡ reconciliation linkã€‚

## 10. Controlled Sync / Actions / Export

Googleã€Telegram/Hermesã€æœªæ¥ç§»åŠ¨ç«¯éƒ½ä¸æ˜¯åº•å±‚çœŸç›¸ï¼Œè€Œæ˜¯å±•ç¤ºå±‚æˆ–è¡ŒåŠ¨å±‚ã€‚

åŒæ­¥å‰æ£€æŸ¥ï¼š

```text
sync_permission
sensitivity
review_state
claim_state
target_system
field_allowlist
```

å…¸åž‹ç­–ç•¥ï¼š

```text
task -> å¯åŒæ­¥åˆ°ä»»åŠ¡ç³»ç»Ÿ
calendar event -> å¯åŒæ­¥åˆ°æ—¥åŽ†
daily readable summary -> å¯é€‰æ‹©åŒæ­¥
medical raw evidence -> é»˜è®¤ local_only
relationship graph -> é»˜è®¤ local_only
finance/tax/insurance -> é»˜è®¤ restricted
```

æ‰€æœ‰å†™å…¥ã€åŒæ­¥ã€ä¿®æ­£ã€åˆ é™¤å»ºè®®éƒ½åº”è¯¥è¿›å…¥ append-only audit/change logã€‚

## 11. å’Œ Echo åŽŸå§‹æµç¨‹çš„å…³ç³»

Echo çš„æ ¸å¿ƒæµç¨‹æ˜¯ï¼š

```text
conversation
 -> structured
 -> memories / action_items / events
 -> vector index
```

å½“å‰ personal database çš„æµç¨‹å‡çº§ä¸ºï¼š

```text
evidence/assets
 -> scoped records/chunks/messages/threads/streams
 -> candidate observations/items/relations
 -> reviewed domain objects
 -> entity graph + timelines + retrieval indexes
 -> assistant actions with privacy gates
```

Echo ä»ç„¶æœ‰ä»·å€¼ï¼Œå› ä¸ºå®ƒæä¾›äº†â€œè¯æ® -> ç†è§£ -> è¡ŒåŠ¨/æ£€ç´¢â€çš„åŸºæœ¬éª¨æž¶ã€‚ä½†å½“å‰ç³»ç»Ÿå·²ç»æ‰©å±•ä¸ºå¤šæºã€å¤šé¢†åŸŸã€é•¿æœŸå¯è¿ç§»çš„ whole-life databaseã€‚

## 12. å½“å‰æœ€é«˜ä¼˜å…ˆçº§

ä¸‹ä¸€æ­¥å¦‚æžœè¦æŠŠè®¾è®¡ç»§ç»­å›ºåŒ–ï¼Œä¼˜å…ˆå†™è¿™å‡ å¼ è¡¨ï¼š

1. `field_cardinality / field_merge_semantics` è·¨åŸŸè¡¨ã€‚
2. åŒ»ç–—æœ€å°è§†å›¾å­—æ®µè¡¨ï¼šEncounter / Observation / MedicationStatement / DiagnosticReport / Claimã€‚
3. é‚®ä»¶ thread ingest è§„åˆ™ï¼šMessage-ID / In-Reply-To / References / attachment / derived itemã€‚
4. å…³ç³»å›¾è°±å®‰å…¨ç­–ç•¥ï¼šå“ªäº›å…³ç³»å¯è‡ªåŠ¨æŠ½å–ï¼Œå“ªäº›å¿…é¡»äººå·¥ç¡®è®¤ï¼Œå“ªäº›æ°¸ä¸å¤–éƒ¨åŒæ­¥ã€‚
5. sidecar æœ€å° schemaï¼š`id/kind/provenance/labels/evidence_refs/field_origin/field_authority/field_merge_policy`ã€‚



