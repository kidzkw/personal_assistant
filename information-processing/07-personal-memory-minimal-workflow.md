# 07. Personal Memory Minimal Workflowï¼ˆä¸ªäººè®°å¿†åº“ç²¾ç®€ä¸»å¹²ï¼‰

è¿™ä»½æ–‡æ¡£æŠŠå‰é¢å¤šè½® research é‡Œçš„å¤æ‚æž¶æž„åŽ‹ç¼©æˆâ€œä¸ªäººå¯ç»´æŠ¤â€çš„ç‰ˆæœ¬ã€‚

ç›®æ ‡ä¸æ˜¯åšä¼ä¸šçº§ EHRã€è´¢åŠ¡ç³»ç»Ÿã€CRMã€æ•°æ®ä»“åº“æˆ–é€šç”¨ AI å¹³å°ï¼Œè€Œæ˜¯åšä¸€ä¸ªé•¿æœŸå¥½ç”¨çš„ä¸ªäººè®°å¿†åº“ï¼šèƒ½ä¿å­˜è¯æ®ï¼Œèƒ½å¸®æˆ‘æ‰¾å›žäº‹æƒ…ï¼Œèƒ½æé†’æˆ‘è¯¥å¤„ç†ä»€ä¹ˆï¼Œèƒ½åœ¨éœ€è¦æ—¶å›žåˆ°åŽŸå§‹æ¥æºã€‚

## 1. å½“å‰æ ¸å¿ƒåˆ¤æ–­

ä¸ªäººè®°å¿†åº“æœ€é‡è¦çš„ä¸æ˜¯ schema å¤šå®Œæ•´ï¼Œè€Œæ˜¯è¿™å‡ ä»¶äº‹ç¨³å®šï¼š

1. åŽŸå§‹èµ„æ–™åˆ«ä¸¢ã€‚
2. æ¯æ¡é‡è¦ä¿¡æ¯çŸ¥é“ä»Žå“ªé‡Œæ¥ã€‚
3. è‡ªåŠ¨æå–çš„ä¸œè¥¿å…ˆå½“å€™é€‰ï¼Œä¸è¦ç›´æŽ¥å½“äº‹å®žã€‚
4. æœç´¢æ—¶å…ˆæ‰¾æ‘˜è¦å’Œæ ‡ç­¾ï¼Œä¸å¤Ÿå†å›žåˆ°åŽŸæ–‡/åŽŸå›¾/åŽŸé‚®ä»¶ã€‚
5. åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€å…³ç³»ã€è´¦å·å®‰å…¨é»˜è®¤æ›´è°¨æ…Žã€‚
6. å¤æ‚æ ‡å‡†åªå€Ÿé‰´ï¼Œä¸ç…§æ¬ã€‚

å½“å‰ä¸»å¹²ï¼š

```text
inbox
 -> raw evidence / asset
 -> light metadata / labels
 -> text/OCR/chunks if needed
 -> extracted candidates
 -> review / confirm
 -> personal memory objects
 -> search / timeline / reminders
 -> evidence pullback
```

## 2. è¦è®°çš„ä¿¡æ¯ç‚¹

### 2.1 æ—¥å¸¸è®°å¿†

åŒ…æ‹¬æ¯æ—¥é‡è¦äº‹æƒ…ã€å†³å®šã€æƒ³æ³•ã€åå¥½ã€ä¹ æƒ¯å˜åŒ–ã€é¡¹ç›®è¿›å±•ã€ä»¥åŽå€¼å¾—é—® assistant çš„äº‹å®žã€‚

æœ€ä½Žå­—æ®µï¼š

```yaml
type: memory
title:
summary:
occurred_at:
source_ref:
sensitivity:
review_state:
```

### 2.2 æ–‡ä»¶å’Œè¯æ®

åŒ…æ‹¬ PDFã€Markdownã€JSON å¯¼å‡ºã€æˆªå›¾ã€ç…§ç‰‡ã€æ‰«æä»¶ã€åŒ»ç–—æ–‡ä»¶ã€è´¦å•ã€ä¿é™©ã€ç¨ŽåŠ¡ã€åˆåŒã€æ—…è¡Œæ–‡ä»¶ã€æ—§ç¡¬ç›˜/æ—§é‚®ç®±/æ—§èŠå¤©å¯¼å‡ºçš„åŽŸå§‹ææ–™ã€‚

æœ€ä½Žå­—æ®µï¼š

```yaml
type: evidence
file_path:
content_hash:
source_category:
ingested_at:
occurred_at:
mime_type:
sensitivity:
```

åŽŸåˆ™ï¼šåŽŸä»¶ä¼˜å…ˆä¿å­˜ï¼›AI æ‘˜è¦ä¸æ˜¯åŽŸä»¶ã€‚

### 2.3 ç…§ç‰‡ / æˆªå›¾ / åª’ä½“

åŒ…æ‹¬æ‰€æœ‰ç…§ç‰‡ã€æˆªå›¾ã€æ–‡æ¡£ç…§ç‰‡ã€EXIF æ—¶é—´ã€GPSã€è®¾å¤‡ã€åŽŸå§‹æ–‡ä»¶å¤¹ã€OCR æ–‡æœ¬ã€ç®€å• captionã€é‡å¤å€™é€‰ã€äº‹ä»¶èšç±»ã€‚

ç¬¬ä¸€ç‰ˆæœ€ä½Žå¤„ç†ï¼š

```yaml
asset_id:
original_path:
content_hash:
captured_at:
source_folder:
media_type:
ocr_text_ref:
caption_candidate:
sensitivity:
```

æš‚ä¸å¤æ‚åŒ–ï¼š

- ä¸æ€¥ç€åšäººè„¸åº“ã€‚
- ä¸è‡ªåŠ¨åˆå¹¶/åˆ é™¤é‡å¤ç…§ç‰‡ã€‚
- GPS å’Œäººè„¸é»˜è®¤æ•æ„Ÿï¼Œä¸éšä¾¿åŒæ­¥ã€‚

### 2.4 åŒ»ç–— / å¥åº·

åŒ…æ‹¬åŒ»ç”Ÿå°±è¯Šã€åŒ–éªŒå•ã€å¤„æ–¹ã€è¯ç‰©ã€ç—‡çŠ¶ã€ä½“æ£€ã€ä¿é™©ç†èµ”ã€åŒ»ç–—è´¦å•ã€‚

ä¸ªäººç‰ˆåªéœ€è¦äº”ç±»ï¼š

```text
medical_document
doctor_visit
lab_result
medication
symptom_note
```

æœ€ä½Žå­—æ®µï¼š

```yaml
type:
date:
provider:
summary:
key_values:
evidence_refs:
review_state: needs_review
sensitivity: medical
sync_permission: local_only
```

æš‚ä¸å¤æ‚åŒ–ï¼š

- ä¸å®žçŽ°å®Œæ•´ FHIRã€‚
- ä¸è‡ªåŠ¨è¯Šæ–­ã€‚
- ä¸è‡ªåŠ¨ç»™ç”¨è¯å»ºè®®ã€‚
- åŒ–éªŒå€¼å¯ä»¥ç»“æž„åŒ–ï¼Œä½†å¿…é¡»èƒ½å›žåˆ°åŽŸ PDF/æˆªå›¾ã€‚

### 2.5 è´¢åŠ¡ / è´¦å• / ç”Ÿæ´»è¡Œæ”¿

åŒ…æ‹¬è´¦å•ã€æ”¶æ®ã€è®¢é˜…ã€ç¨ŽåŠ¡ã€ä¿é™©ã€è´·æ¬¾ã€ä»˜æ¬¾æé†’ã€æŠ¥é”€ã€é“¶è¡Œ/ä¿¡ç”¨å¡è®°å½•ã€‚

ä¸ªäººç‰ˆå¯¹è±¡ï¼š

```text
financial_document
bill_or_subscription
receipt
payment_deadline
finance_candidate
```

æœ€ä½Žå­—æ®µï¼š

```yaml
type:
merchant_or_org:
amount:
currency:
due_at:
paid_state:
evidence_refs:
review_state:
sensitivity: financial
```

æš‚ä¸å¤æ‚åŒ–ï¼š

- ä¸åšå®Œæ•´å¤å¼è®°è´¦ã€‚
- OCR é‡‘é¢é»˜è®¤ candidateã€‚
- ä¸è‡ªåŠ¨åšè´¢åŠ¡å†³ç­–æˆ–æŠ•èµ„å»ºè®®ã€‚

### 2.6 é‚®ä»¶ / è´¦å· / å®‰å…¨é€šçŸ¥

åŒ…æ‹¬æ—§é‚®ç®±å’Œæ–°é‚®ç®±ã€é™„ä»¶ã€è´¦å•ã€æ”¶æ®ã€éªŒè¯ç ã€å®‰å…¨æé†’ã€è´¦å·å˜æ›´ã€æ—…è¡Œé¢„è®¢ã€é¢„çº¦æé†’ã€‚

ä¸ªäººç‰ˆå¤„ç†ï¼š

```text
email_message
email_thread_summary
attachment_asset
derived_notice
```

æœ€ä½Žå­—æ®µï¼š

```yaml
message_id:
from:
to:
subject:
sent_at:
thread_id:
attachment_refs:
summary:
derived_candidates:
sensitivity:
```

æ³¨æ„ï¼š

- thread åªæ˜¯è§†å›¾ï¼Œä¸èƒ½è¦†ç›–å•å°é‚®ä»¶çš„äº‹å®žã€‚
- é™„ä»¶è¦å˜æˆç‹¬ç«‹ evidenceã€‚
- å®‰å…¨é€šçŸ¥ã€è´¦å•ã€åŒ»ç–—é‚®ä»¶é»˜è®¤éœ€è¦ reviewã€‚

### 2.7 äºº / å…³ç³» / ç”Ÿæ—¥ / å…±åŒç»åŽ†

åŒ…æ‹¬æœ‹å‹ã€å®¶äººã€åŒ»ç”Ÿã€åŒäº‹ã€æœåŠ¡å•†ã€ç”Ÿæ—¥ã€è”ç³»æ–¹å¼ã€é‡è¦å…³ç³»ã€æœ€è¿‘äº’åŠ¨ã€å…±åŒäº‹ä»¶ã€è¦è·Ÿè¿›çš„æ‰¿è¯ºã€‚

ä¸ªäººç‰ˆå¯¹è±¡ï¼š

```text
person
interaction
relationship_note
reminder
```

æœ€ä½Žå­—æ®µï¼š

```yaml
person_id:
name:
aliases:
birthday:
contact_methods:
relationship_summary:
last_interaction_at:
evidence_refs:
sensitivity:
sync_permission: local_only
```

æš‚ä¸å¤æ‚åŒ–ï¼š

- ä¸æ€¥ç€åšå®Œæ•´å…³ç³»å›¾è°±ã€‚
- ä¸è‡ªåŠ¨ç¡®è®¤æ•æ„Ÿå…³ç³»ã€‚
- ç¬¬ä¸‰æ–¹éšç§é»˜è®¤ local_onlyã€‚

### 2.8 ä»»åŠ¡ / äº‹ä»¶ / æé†’

åŒ…æ‹¬å¾…åŠžã€æ‰¿è¯ºã€æˆªæ­¢æ—¥æœŸã€é¢„çº¦ã€è´¦å• due dateã€ç”Ÿæ—¥ã€æ—…è¡Œå®‰æŽ’ã€‚

ä¸ªäººç‰ˆå¯¹è±¡ï¼š

```text
task
event
reminder
```

æœ€ä½Žå­—æ®µï¼š

```yaml
title:
kind:
due_at:
status:
source_ref:
sync_permission:
review_state:
```

å¯ä»¥åŒæ­¥æ™®é€šä»»åŠ¡å’Œæ™®é€šæ—¥ç¨‹ã€‚é»˜è®¤ä¸åŒæ­¥åŒ»ç–—ç»†èŠ‚ã€è´¢åŠ¡ç»†èŠ‚ã€å…³ç³»å›¾è°±å’ŒåŽŸå§‹æ•æ„Ÿæ–‡ä»¶ã€‚

## 3. ä¿¡æ¯å¤„ç†ä¸»æµç¨‹

### Step 1: æ”¶è¿› inbox

æ‰€æœ‰ä¸œè¥¿å…ˆè¿›å…¥ inboxï¼Œä¸è¦æ±‚ä¸€å¼€å§‹åˆ†ç±»å®Œç¾Žã€‚

```text
photo / screenshot / pdf / markdown / json / email / attachment / chat export / note
 -> inbox
```

inbox æœ€å°‘è®°å½•ï¼š

```yaml
id:
source_category:
original_path:
ingested_at:
basic_type:
review_state: inbox
```

### Step 2: ä¿å­˜åŽŸå§‹è¯æ®

è¿›å…¥ç³»ç»ŸåŽï¼ŒåŽŸå§‹æ–‡ä»¶å°½é‡ä¸æ”¹ã€‚

```text
inbox item
 -> raw_evidence / media_asset / email_message / attachment_asset
```

æœ€é‡è¦çš„æ˜¯æœ‰ hashã€è·¯å¾„ã€æ¥æºã€æ—¶é—´ã€æ•æ„Ÿçº§åˆ«ã€‚

åŒæ—¶è¦åŒºåˆ†å››å±‚ï¼š

```text
truth   = åŽŸå§‹æ–‡ä»¶ã€sidecarã€confirmed memory objects
working = å¯è¯»æ•´ç†é¡µã€wiki briefã€å°±è¯Šå‡†å¤‡æ‘˜è¦ã€äººå·¥ä¿®æ­£è¯´æ˜Ž
cache   = OCRã€thumbnailã€FTS/BM25ã€embeddingã€graph view
export  = Markdown/HTML/CSV/JSON å¯¼å‡ºåŒ…
```

ä¸ªäººç‰ˆåŽŸåˆ™ï¼š

- `truth` æ‰æ˜¯çœŸç›¸å±‚ã€‚
- `working` æ˜¯å¸®åŠ©äººç†è§£å’Œ review çš„æ•´ç†å±‚ï¼Œä¸æ›¿ä»£åŽŸä»¶ã€‚
- `cache` å¯ä»¥åˆ é™¤é‡å»ºï¼Œå¿…é¡»çŸ¥é“ä»Žå“ªäº›æ–‡ä»¶/å¯¹è±¡ç”Ÿæˆã€‚
- `export` é»˜è®¤å­—æ®µç™½åå•å’Œè„±æ•ï¼Œä¸ç›´æŽ¥å¸¦å‡ºåŒ»ç–—ã€è´¢åŠ¡ã€å…³ç³»ã€è´¦å·å®‰å…¨åŽŸä»¶ã€‚

ç¬¬ä¸€ç‰ˆæœ€ä½Žå­—æ®µï¼š

```yaml
storage_layer: truth | working | cache | export
artifact_role: original | sidecar | extracted_text | ocr | preview | redacted | wiki_brief | index_record | embedding
built_from_refs:
generated_at:
review_state:
```

### Step 3: è½»é‡æ‰“æ ‡ç­¾

ä¸ªäººç‰ˆå…ˆä¿ç•™è¿™äº›ï¼š

```yaml
domain: daily | photo | health | finance | email | relationship | admin | travel | account | other
media_type: text | pdf | image | screenshot | email | json | audio_later
semantic_type: note | bill | receipt | lab_result | visit | task | event | memory | contact | security_notice
sensitivity: normal | private | health | financial | legal | account_security | relationship
review_state: inbox | candidate | confirmed | archived | rejected
sync_permission: local_only | summary_ok | task_calendar_ok
occurred_at:
ingested_at:
```

è¿™æ˜¯å½“å‰æŽ¨èçš„â€œä¸ªäººç‰ˆæ ‡ç­¾å‘é‡â€ã€‚å¤Ÿç”¨äº†ï¼Œåˆ«å†å¾€é‡Œé¢å¡žå¤ªå¤šèŠ±æ´»ã€‚

æ¥æºç³»ç»Ÿè‡ªå·±çš„æ–‡ä»¶å¤¹ã€æ ‡ç­¾ã€ç›¸å†Œã€threadã€æ”¶è—å¤¹ä¸è¦æ··è¿›ä¸ªäººè¯­ä¹‰æ ‡ç­¾ã€‚å®ƒä»¬å•ç‹¬ä½œä¸º `source_membership`ï¼š

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
  publish_policy: local_only | private_export_ok | redacted_export_ok | share_ok
```

è¿™æ ·åŒä¸€å¼ ç…§ç‰‡ã€åŒä¸€å°é‚®ä»¶ã€åŒä¸€ä»½ PDF å¯ä»¥å±žäºŽå¤šä¸ªæ¥æºå®¹å™¨ï¼Œä½†é•¿æœŸè¯­ä¹‰åªç¡®è®¤ä¸€æ¬¡ã€‚

### Step 4: è§£æž / OCR / åˆ‡å—

åªåœ¨éœ€è¦æ—¶åšè§£æžã€‚

```text
PDF -> text + pages
photo/screenshot -> EXIF + OCR + thumbnail
email -> message + attachments
markdown/text -> chunks
json export -> source-specific records
audio later -> transcript segments
```

åˆ‡å—åŽŸåˆ™ï¼š

- æ–‡æœ¬æŒ‰æ®µè½/æ ‡é¢˜åˆ‡ã€‚
- PDF æŒ‰é¡µå’Œç« èŠ‚åˆ‡ã€‚
- é‚®ä»¶æŒ‰ message å’Œ attachment åˆ‡ã€‚
- ç…§ç‰‡ä¸å¼ºè¡Œåˆ‡ï¼Œåªä¿ç•™ metadata/OCR/captionã€‚
- æœªæ¥éŸ³é¢‘æŒ‰ transcript segment + sessionã€‚

### Step 5: æå–å€™é€‰

AI/OCR/è§„åˆ™åªç”Ÿæˆå€™é€‰ï¼Œä¸ç›´æŽ¥ç”ŸæˆçœŸç›¸ã€‚

å€™é€‰ç±»åž‹ï¼š

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

å€™é€‰æœ€ä½Žå­—æ®µï¼š

```yaml
candidate_type:
summary:
extracted_values:
confidence:
evidence_refs:
review_state: candidate
sensitivity:
```

é«˜é£Žé™©å€™é€‰è¿˜éœ€è¦ `citation_refs`ï¼Œè‡³å°‘èƒ½å›žåˆ°æ–‡ä»¶ã€é¡µç ã€message id æˆ–æˆªå›¾/OCR ç‰‡æ®µï¼š

```yaml
citation_refs:
  evidence_ref:
  artifact_ref:
  locator:
  excerpt:
  extraction_method:
  confidence:
```

åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€è´¦å·å®‰å…¨ã€å…³ç³»ç±»å€™é€‰å¦‚æžœæ²¡æœ‰ citationï¼Œåªèƒ½ç•™åœ¨ candidateï¼Œä¸èƒ½ confirmedã€‚

### Step 6: Review

ä¸ªäººç‰ˆ review ä¸éœ€è¦å¤æ‚å·¥ä½œæµï¼Œåªè¦åˆ†æ¸…ï¼š

```text
confirm
correct
ignore
archive
```

é»˜è®¤éœ€è¦ reviewï¼š

- åŒ»ç–—ã€‚
- è´¢åŠ¡ã€‚
- æ³•å¾‹ã€‚
- è´¦å·å®‰å…¨ã€‚
- äººé™…å…³ç³»ã€‚
- è‡ªåŠ¨ç”Ÿæˆçš„é•¿æœŸè®°å¿†ã€‚
- åˆ é™¤/åˆå¹¶å»ºè®®ã€‚

å¯ä»¥ä½Ž review æˆ–è‡ªåŠ¨å½’æ¡£ï¼š

- æ™®é€šç…§ç‰‡ captionã€‚
- æ™®é€šæ–‡ä»¶ OCRã€‚
- æ— è¡ŒåŠ¨é¡¹çš„è¥é”€é‚®ä»¶ã€‚
- æ˜Žç¡®ä½Žä»·å€¼å™ªå£°ã€‚

### Step 6.5: PS æ€»ç®¡å’Œ agent ä¸²è¡ŒæŽ¥åŠ›

agent workflow åªä½œä¸ºä¿¡æ¯å¤„ç†è§’è‰²ï¼Œä¸æ˜¯æ— é™è‡ªæ²»ç³»ç»Ÿã€‚

ä¸ªäººç‰ˆæœ€å°åˆ†å·¥ï¼š

```text
æ€»ç®¡ = å”¯ä¸€æ€»è°ƒåº¦å±‚ï¼Œè´Ÿè´£åˆ†ç±»ã€åˆ†æ´¾ã€å…¨å±€ work logã€å†²çªè®°å½•ã€ä¸‹ä¸€æ­¥æŽ’é˜Ÿ
å°ç§˜ = é•¿æœŸé¢†åŸŸ stewardï¼Œä¾‹å¦‚ health_secretary / finance_secretary / email_admin_secretary / relationship_secretary
processing_agent = çŸ­ç”Ÿå‘½å‘¨æœŸå¤„ç†è€…ï¼Œåªå¤„ç†ä¸€ä¸ª evidence packet / object brief / update check
audit_agent = çŸ­ç”Ÿå‘½å‘¨æœŸå®¡è®¡è€…ï¼Œåªæ£€æŸ¥ processing_result çš„è¯æ®ã€å¼•ç”¨ã€è¾¹ç•Œå’Œé£Žé™©
proposal_agent = çŸ­ç”Ÿå‘½å‘¨æœŸææ¡ˆè€…ï¼Œåªç”Ÿæˆ review_result / update_proposal / no_action
```

æ ¸å¿ƒçº¦æŸï¼šæ¯ä¸ªå°ç§˜åŒä¸€æ—¶é—´åªèƒ½æœ‰ä¸€æ¡ active child chainã€‚ä¸Šä¸€æ¡ processing/audit/proposal chain æ²¡æœ‰è¢«å°ç§˜æ±‡æ€»ã€å†™å…¥ work logã€report ç»™æ€»ç®¡ä¹‹å‰ï¼Œä¸å…è®¸å¼€å§‹ä¸‹ä¸€æ¡ chainã€‚

ä¸ªäººç‰ˆæœ€å°å­—æ®µï¼š

```yaml
ps_agent_work_log:
  log_id:
  secretary_agent:
  work_item_ref:
  evidence_packet_refs:
  object_refs:
  current_status: queued | assigned | processing_running | processing_returned | audit_running | audit_returned | proposal_running | secretary_reported | closed | blocked
  active_chain_id:
  next_spawn_allowed:
  processing_result_ref:
  audit_result_ref:
  proposal_ref:
  baton_ref:
  domain_event_summary_report_ref:
  recommended_next_step:
  sensitivity:
```

çŸ­ç”Ÿå‘½å‘¨æœŸ agent çš„è¾“å‡ºåªèƒ½æ˜¯ç»“æž„åŒ–ä¸­é—´ç»“æžœï¼š

```yaml
processing_result:
  processing_run_id:
  evidence_packet_ref:
  output_type: extracted_candidate | object_brief | update_check | no_signal
  structured_output_ref:
  citation_refs:
  confidence:
  recommended_next_step:

audit_result:
  audit_run_id:
  processing_run_id:
  evidence_sufficient:
  citation_valid:
  contradiction_found:
  scope_violation:
  audit_decision: pass | retry | human_review | reject
  risk_flags:

proposal_result:
  proposal_run_id:
  final_output_type: review_result | update_proposal | no_action
  final_output_ref:
  recommended_next_step:
```

æ³¨æ„ï¼š

- processing/audit/proposal agent éƒ½ä¸ç›´æŽ¥å†™ confirmed memory æˆ– truth layerã€‚
- ä¸ä¿å­˜çŸ­ç”Ÿå‘½å‘¨æœŸ agent çš„é•¿ä¸Šä¸‹æ–‡ï¼Œåªä¿å­˜ç»“æž„åŒ–ç»“æžœã€citationã€baton å’Œ work log çŠ¶æ€ã€‚
- å°ç§˜è´Ÿè´£ç”Ÿæˆ `domain_event_summary_report` ç»™æ€»ç®¡ï¼›æ€»ç®¡åªæ ¹æ® report æ›´æ–° work logã€å†³å®š `next_spawn_allowed`ã€‚
- åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€è´¦å·å®‰å…¨ã€å…³ç³»ä¿¡æ¯é»˜è®¤ `local_only` ä¸” `review_required`ã€‚
- å¦‚æžœç»“æžœè¯æ®ä¸è¶³æˆ–å†²çªï¼ŒçŠ¶æ€å†™ `blocked`ï¼Œä¸è¦é™é»˜ç»§ç»­ä¸‹ä¸€æ£’ã€‚

### Step 7: å½¢æˆä¸ªäººè®°å¿†å¯¹è±¡

ç¡®è®¤åŽè¿›å…¥é•¿æœŸå±‚ï¼š

```text
memory
person
interaction
task
event
medical_record
finance_record
document_record
photo_event
account_notice
```

ä¸ªäººç‰ˆè®°å¿†å¯¹è±¡æœ€å°‘è¦æœ‰ï¼š

```yaml
id:
type:
title:
summary:
occurred_at:
entity_refs:
evidence_refs:
sensitivity:
review_state: confirmed
```

### Step 8: æ£€ç´¢ / ä½¿ç”¨

æ£€ç´¢é¡ºåºä¿æŒç®€å•ï¼š

```text
1. å…³é”®è¯ / æ—¥æœŸ / äºº / ç±»åž‹è¿‡æ»¤
2. æ‘˜è¦å’Œ confirmed memory
3. OCR / é‚®ä»¶æ­£æ–‡ / æ–‡æ¡£ chunk
4. åŽŸå§‹è¯æ®å›žæ‹‰
```

ç¬¬ä¸€ç‰ˆä¼˜å…ˆç²¾ç¡®æœç´¢ã€æ—¥æœŸæœç´¢ã€æ ‡ç­¾è¿‡æ»¤ã€æœ¬åœ°å…¨æ–‡æœç´¢ã€è¯æ®å›žæ‹‰ã€‚ä»¥åŽå†åŠ  vector searchã€routing indexã€å¤æ‚ graph traversalã€‚

## 4. å“ªäº›ç ”ç©¶å»ºè®®åº”è¯¥é™çº§

### 4.1 FHIR

ä¿ç•™æ€æƒ³ï¼šåŒ»ç–—å¯¹è±¡è¦èƒ½å›žåˆ°è¯æ®ï¼›å°±è¯Šã€åŒ–éªŒã€ç”¨è¯ã€ç—‡çŠ¶è¦åˆ†å¼€ã€‚

ä¸ªäººç‰ˆåšæ³•ï¼š

```text
medical_document / doctor_visit / lab_result / medication / symptom_note
```

æš‚ä¸åšå®Œæ•´ FHIR resource graphã€‚

### 4.2 Perkeep object_anchor / attribute_claim

ä¿ç•™æ€æƒ³ï¼šé•¿æœŸå¯¹è±¡ä¼šå˜åŒ–ï¼ŒåŽ†å²ä¸è¦ç›´æŽ¥è¦†ç›–ã€‚

ä¸ªäººç‰ˆåšæ³•ï¼šç¬¬ä¸€ç‰ˆåªä¿ç•™ `updated_at`ã€`previous_values` æˆ–ç®€å• `change_log`ã€‚åªæœ‰ person/account/medical/finance è¿™ç§é«˜ä»·å€¼å¯¹è±¡ï¼Œæœªæ¥å†è€ƒè™‘ claim æ¨¡åž‹ã€‚

### 4.3 source_snapshot / import_run / parse_error_record

ä¿ç•™æ€æƒ³ï¼šå¤§æ‰¹é‡å¯¼å…¥è¦çŸ¥é“â€œå“ªæ‰¹æ•°æ®è¿›æ¥äº†ï¼Œå“ªäº›å¤±è´¥äº†â€ã€‚

ä¸ªäººç‰ˆåšæ³•ï¼š

```yaml
import_batch:
  id:
  source_name:
  imported_at:
  item_count:
  error_count:
  notes:
```

è§£æžå¤±è´¥ç¬¬ä¸€ç‰ˆå¯ä»¥æ˜¯ç®€å•åˆ—è¡¨ï¼š

```yaml
failed_items:
  path:
  reason:
  retry_later:
```

ä¸ç”¨ä¸€å¼€å§‹åšå®Œæ•´æ•°æ®ç®¡çº¿å¯¹è±¡ã€‚

### 4.4 data warehouse / exploratory index

ä¿ç•™æ€æƒ³ï¼šæ‰¹é‡æ£€æŸ¥å’Œæœç´¢éœ€è¦ä¸€ä¸ªæœ¬åœ°ç´¢å¼•ã€‚

ä¸ªäººç‰ˆåšæ³•ï¼šç”¨æœ¬åœ° SQLite/FTS æˆ–è½»é‡ç´¢å¼•å³å¯ï¼Œä¸æŠŠå®ƒå½“æ­£å¼äº‹å®žåº“ï¼Œä¸åšåˆ†äº«è§†å›¾ã€‚

### 4.5 å…³ç³»å›¾è°±

ä¿ç•™æ€æƒ³ï¼šäººå’Œäº’åŠ¨å¾ˆé‡è¦ã€‚

ä¸ªäººç‰ˆåšæ³•ï¼š

```text
person + interaction + reminder
```

æš‚ä¸åšå¤æ‚ graph edgeã€consent ontologyã€visibility scope çŸ©é˜µã€‚æ•æ„Ÿå…³ç³»é  review å’Œ local_only æŽ§åˆ¶ã€‚

## 5. å½“å‰æŽ¨èæœ€å°ç›®å½•/å¯¹è±¡

å¦‚æžœçŽ°åœ¨è¦æŠŠä¸»å¹²è½æˆæ–‡ä»¶/æ•°æ®åº“æ¦‚å¿µï¼Œä¼˜å…ˆè¿™äº›ï¼š

```text
inbox_item
raw_evidence
media_asset
email_message
content_chunk
candidate_item
memory
person
interaction
task
event
medical_record
finance_record
document_record
import_batch
audit_log
source_membership
location_raw_point
health_sample
```

é«˜ä»·å€¼è¯æ®å¯ä»¥å¢žåŠ ä¸€ä¸ªè½»é‡ `evidence_packet`ï¼Œä¸æ˜¯æ‰€æœ‰æ–‡ä»¶éƒ½å¿…é¡»æœ‰ï¼š

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

ä¼˜å…ˆç”¨äºŽåŒ»ç–— PDFã€è´¢åŠ¡/ç¨ŽåŠ¡/ä¿é™©æ–‡ä»¶ã€åˆåŒã€è´¦å·å®‰å…¨æˆªå›¾ã€é‡è¦è¡Œæ”¿æ–‡ä»¶ã€‚

è¿™å·²ç»èƒ½è¦†ç›–å¤§å¤šæ•°ä¸ªäººè®°å¿†éœ€æ±‚ã€‚

æš‚ä¸è¿›å…¥ä¸»å¹²ï¼š

```text
full FHIR resources
full accounting ledger
full CRM graph
claim-fold object store
multi-device sync protocol
general data warehouse
automated medical/financial decisions
```

## 6. å½“å‰æœ€é‡è¦çš„ä¿¡æ¯ç‚¹ä¼˜å…ˆçº§

P0ï¼Œå¿…é¡»ä¿ç•™ï¼š

- `id`
- `type`
- `title/summary`
- `occurred_at`
- `ingested_at`
- `source_ref/evidence_refs`
- `sensitivity`
- `review_state`
- `sync_permission`
- `content_hash` for files/assets

P1ï¼Œå¼ºçƒˆå»ºè®®ï¼š

- `entity_refs`
- `confidence`
- `original_path`
- `mime_type`
- `extracted_values`
- `change_log`
- `import_batch_id`
- `interpretation_level`
- `temporal_anchor` for interval/stream data

P2ï¼Œä»¥åŽå†è¯´ï¼š

- `field_contract`
- `object_anchor`
- `attribute_claim`
- `context_routing_index`
- `candidate_verification`
- `local_data_warehouse_view`
- full domain-specific schemas

## 7. ä¸€å¥è¯ç‰ˆæœ¬

ä¸ªäººè®°å¿†åº“çš„ç¬¬ä¸€ç‰ˆä¸éœ€è¦åƒä¸€ä¸ªå°åž‹äº’è”ç½‘å…¬å¸åŽå°ã€‚

å®ƒéœ€è¦åƒä¸€ä¸ªå¾ˆå¯é çš„ç§äººæ¡£æ¡ˆå‘˜ï¼šä¸œè¥¿å…ˆè¿›æ¥ï¼ŒåŽŸä»¶åˆ«ä¸¢ï¼Œæ¥æºè¯´æ¸…æ¥šï¼ŒAI åªæå»ºè®®ï¼Œé‡è¦äº‹å®žä½ ç¡®è®¤ï¼Œä¹‹åŽèƒ½æŒ‰æ—¶é—´ã€äººã€ä¸»é¢˜ã€æ–‡ä»¶ã€è¯æ®æ‰¾å›žæ¥ã€‚

