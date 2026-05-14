# Candidate Proposalsï¼ˆæŒç»­æ›´æ–°ï¼‰

æ›´æ–°æ—¶é—´ï¼š2026-05-13

> ç›®çš„ï¼šæŠŠæ¯æ¬¡ research run çš„â€œå¯è½åœ°ç»“æž„å»ºè®®â€åŽ‹ç¼©æˆå°‘é‡å€™é€‰é¡¹ï¼Œä¾¿äºŽåŽç»­é€æ­¥å›ºåŒ–ä¸ºæ­£å¼ IA/ç›®å½•çº¦å®š/å…ƒæ•°æ® schemaï¼ˆä»…æ–‡æ¡£ï¼Œä¸åšä»£ç å®žçŽ°ï¼‰ã€‚

## P0ï¼ˆå¼ºçƒˆå»ºè®®çº³å…¥å½“å‰ç»“æž„ï¼‰

### P0-1ï¼šç»Ÿä¸€å…ƒæ•°æ®ä¸ºâ€œå¤šç»´æ ‡ç­¾å‘é‡â€ï¼ˆæ›¿ä»£å•ä¸€ categoryï¼‰

- **å‘çŽ°æ¥æº**ï¼šPaperless-ngx çš„ correspondents / document types / tags å¤šè½´ä½“ç³»ï¼›Notmuch çš„ tag-first æ”¶ä»¶ç®±ï¼›Echo çš„ system labels + semantic labels + derived labels åˆ†å±‚ã€‚
- **è¦ç‚¹**ï¼š
  - `domain / source_category / media_type / semantic_type / counterparty / actionability / sensitivity / temporal / confidence / review_state / retention_class / criticality / sync_permission`
  - å¼ºåˆ¶åŒºåˆ† `occurred_at` ä¸Ž `ingested_at`ï¼ˆPaperless çš„ date created vs date added æ¨¡å¼ï¼‰ã€‚
- **æ”¶ç›Š**ï¼šè·¨åŸŸï¼ˆç…§ç‰‡/é‚®ä»¶/å¥åº·/è´¢åŠ¡ï¼‰ä¸€è‡´ï¼›ä¾¿äºŽé•¿æœŸæ¼”è¿›ä¸Žæ£€ç´¢è¿‡æ»¤ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢ž `labels` ç»“æž„ï¼›ä»»ä½•æ´¾ç”Ÿå¯¹è±¡å¿…é¡»å¸¦ `evidence_refs`ã€‚
- **é£Žé™©**ï¼šç»´åº¦è¿‡å¤šä¼šå¯¼è‡´äººå·¥ç»´æŠ¤æˆæœ¬ä¸Šå‡ï¼›éœ€è¦é»˜è®¤å€¼ä¸Žâ€œé€æ­¥è¡¥å…¨â€ç­–ç•¥ï¼ˆINBOX å®¡é˜…é—¨ï¼‰ã€‚

### P0-2ï¼šè¯æ®å±‚ä¸å¯å˜ + sidecar å…ƒæ•°æ®ä¸ºä¸€ç­‰å…¬æ°‘ï¼ˆç…§ç‰‡ä¼˜å…ˆ XMPï¼‰

- **å‘çŽ°æ¥æº**ï¼šImmich XMP sidecar è¯»å†™ä¸Žä½œä¸šï¼›PhotoPrism çš„ metadata åˆå¹¶ä¸Ž YAML sidecar å¯¼å‡ºã€‚
- **è¦ç‚¹**ï¼š
  - åŽŸæ–‡ä»¶ï¼ˆevidence/assetsï¼‰å°½é‡ä¸ä¿®æ”¹ï¼›
  - å…ƒæ•°æ®ï¼ˆæ ‡ç­¾ã€æè¿°ã€OCR å¼•ç”¨ã€æ•æ„Ÿçº§åˆ«ã€å®¡é˜…çŠ¶æ€ã€åŽ»é‡ä¿¡æ¯ï¼‰å†™ sidecarï¼ˆç…§ç‰‡ç”¨ XMPï¼›å…¶ä»–ç”¨ `*.meta.json`ï¼‰ã€‚
- **æ”¶ç›Š**ï¼šé™ä½Ž DB lock-inï¼›é•¿æœŸè¿ç§»/å·¥å…·äº’æ“ä½œæ›´å¼ºã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šå®šä¹‰ sidecar çš„æœ€å°é”®é›†åˆï¼ˆ`id/kind/provenance/timestamps/labels/evidence_refs`ï¼‰ã€‚
- **é£Žé™©**ï¼šsidecar ä¸Žæœªæ¥ç´¢å¼•/ç¼“å­˜çš„ä¸€è‡´æ€§ä¸Žå†²çªç­–ç•¥éœ€è¦å…ˆå†™æ¸…æ¥šã€‚

### P0-3ï¼šç»Ÿä¸€ `review_state=inbox` å®¡é˜…é—¨ï¼ˆè·¨åŸŸé€šç”¨ï¼‰

- **å‘çŽ°æ¥æº**ï¼šPaperless-ngx çš„ INBOX æ ‡ç­¾å·¥ä½œæµï¼›ç¤¾åŒºç»éªŒâ€œè‡ªåŠ¨åŒ–åªåšåˆ°å»ºè®®ï¼Œæœ€ç»ˆè¦äººå·¥ç¡®è®¤â€ã€‚
- **è¦ç‚¹**ï¼š
  - é»˜è®¤è¿›å…¥ `inbox`ï¼›
  - è‡ªåŠ¨æŠ½å–åªäº§ç”Ÿâ€œå€™é€‰æ´¾ç”Ÿå¯¹è±¡â€ï¼ˆtask/event/factï¼‰ï¼Œåœ¨ `reviewed` å‰ä¸è¿›å…¥æ ¸å¿ƒè®°å¿†/å…³é”®ç´¢å¼•ã€‚
- **æ”¶ç›Š**ï¼šé•¿æœŸæ­£ç¡®æ€§ã€é™ä½Žå™ªå£°ä¸Žè¯¯å½’ç±»ï¼›ç‰¹åˆ«é€‚åˆåŒ»ç–—/è´¢åŠ¡ã€‚
- **é£Žé™©**ï¼šéœ€è¦æ˜Žç¡®â€œå¤šé•¿æ—¶é—´ä¸å®¡é˜…çš„å¤„ç†ç­–ç•¥â€ï¼ˆæé†’/é™çº§/å½’æ¡£ï¼‰ã€‚

### P0-4ï¼šæŠŠâ€œæº¯æº/å®¡è®¡ï¼ˆprovenanceï¼‰â€æå‡ä¸ºä¸€ç­‰å­—æ®µï¼ˆåŒºåˆ†æ–‡æ¡£æº¯æº vs è®°å½•æº¯æºï¼‰

- **å‘çŽ°æ¥æº**ï¼šFHIR `DocumentReference` å¼ºè°ƒâ€œè¢«å¼•ç”¨æ–‡æ¡£çš„æº¯æºâ€ä¸Žâ€œå¼•ç”¨è®°å½•æœ¬èº«çš„æº¯æºâ€æ˜¯ä¸¤å¥—ä¿¡æ¯ï¼›W3C PROVï¼ˆentity/activity/agentï¼‰ï¼›ä»¥åŠ Paperless çš„ç®¡çº¿é˜¶æ®µå·®å¼‚å¸¦æ¥çš„å¯è§£é‡Šæ€§éœ€æ±‚ã€‚
- **è¦ç‚¹**ï¼š
  - åœ¨ sidecar/frontmatter çš„æœ€å° schema ä¸­åŠ å…¥ `provenance.document` ä¸Ž `provenance.record`ï¼›
  - æŠ½å–ç»“è®ºç±»æ¡ç›®æ–°å¢ž `claim_state`ï¼ˆcandidate/confirmed/disputed/superseded/retractedï¼‰ä¸Ž `validity`ï¼ˆvalid_from/valid_to/last_confirmed_atï¼‰ï¼›
  - ä»»ä½•æ´¾ç”Ÿå¯¹è±¡å¼ºåˆ¶ `evidence_refs`ï¼ˆå¯å›žæº¯åˆ°æ–‡ä»¶ hash + é¡µç /åŒºåŸŸ/æ¶ˆæ¯ id ç­‰ï¼‰ã€‚
- **æ”¶ç›Š**ï¼šåŒ»ç–—/æ³•å¾‹/è´¢åŠ¡åœºæ™¯å¯è§£é‡Šã€å¯çº é”™ï¼›é•¿æœŸç»´æŠ¤ä¸ä¼šâ€œå¿˜äº†è¿™æ¡ä¿¡æ¯æ€Žä¹ˆæ¥çš„â€ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šsidecar/frontmatter æœ€å°å­—æ®µé›†éœ€è¦æ‰©å±•ï¼›å¹¶æ˜Žç¡® provenance å­—æ®µä¹Ÿå— `sensitivity/sync_permission` çº¦æŸã€‚
- **é£Žé™©**ï¼šprovenance æœ¬èº«å¯èƒ½æ³„éœ²æ•æ„Ÿå…ƒä¿¡æ¯ï¼ˆè·¯å¾„/æœºæž„/é‚®ç®±/è®¾å¤‡åï¼‰ï¼›éœ€è¦é»˜è®¤æœ€å°åŒ–ä¸Žè„±æ•ç­–ç•¥ã€‚

### P0-5ï¼šå­—æ®µçº§â€œæƒå¨/åˆå¹¶è¯­ä¹‰â€æ˜¾å¼åŒ–ï¼ˆå°¤å…¶æ˜¯ç…§ç‰‡ XMP çš„åˆ«åä¼˜å…ˆçº§ä¸Žå†™å›žè§„åˆ™ï¼‰

- **å‘çŽ°æ¥æº**ï¼šPhotoPrism å¯¹ XMP çš„ä¸¤æ¡è§£æžè·¯å¾„ä¸Ž sidecar reader é™åˆ¶ï¼ˆembedded ç» ExifTool vs `.xmp` PoC readerï¼‰ï¼›Immich å¯¹ XMP sidecar çš„â€œåˆå¹¶å†™å›žï¼ˆmergeï¼‰â€ä¸Žå­—æ®µä¼˜å…ˆçº§é¡ºåºã€å‘½åè§„åˆ™ã€DISCOVER/SYNC ä½œä¸šã€‚
- **è¦ç‚¹**ï¼š
  - ä¸ºå…³é”®å…ƒæ•°æ®å­—æ®µè¡¥é½ä¸‰ä»¶äº‹ï¼š`field_origin`ï¼ˆæ¥è‡ª embedded/sidecar/OCR/æ‰‹å·¥/æŠ½å–â€¦ï¼‰ã€`field_authority`ï¼ˆå†²çªæ—¶è°æ˜¯é»˜è®¤çœŸç›¸ï¼‰ã€`field_merge_policy`ï¼ˆè¦†ç›–/åˆå¹¶/ä¼˜å…ˆçº§åˆ—è¡¨ï¼‰ï¼›
  - ç…§ç‰‡åŸŸæŠŠâ€œé€»è¾‘å­—æ®µ â†’ XMP/EXIF/IPTC åˆ«åä¼˜å…ˆçº§åˆ—è¡¨ â†’ å†™å›žç™½åå•â€å†™æˆä¸€å¼ è¡¨ï¼Œå¹¶æ˜Žç¡®åªå†™å›žè·¨å·¥å…·é€šç”¨å­—æ®µï¼ˆæè¿°/è¯„åˆ†/æ ‡ç­¾/æ—¶é—´/ä½ç½®ç­‰ï¼‰ï¼Œæ•æ„Ÿå­—æ®µï¼ˆGPS/äººè„¸ï¼‰é»˜è®¤ä¸å†™å›ž/ä¸åŒæ­¥ï¼›
  - å†™å›žéœ€è¦æ˜¾å¼æƒé™ä¸Žå¤±è´¥å¯è§‚æµ‹æ€§ï¼ˆé¿å… read-only å¤–éƒ¨åº“ä¸‹ silent failï¼‰ã€‚
- **æ”¶ç›Š**ï¼šé¿å…æœªæ¥å¯¼å…¥/ç¼–è¾‘/å¤šå·¥å…·æ··ç”¨å¯¼è‡´çš„â€œä¸å¯è§£é‡Šè¦†ç›–â€ï¼›æŠŠå†²çªä»Žå®žçŽ°å±‚æå‰åˆ° IA è§„èŒƒå±‚ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šsidecar/frontmatter æœ€å° schema éœ€æ–°å¢ž `field_origin/field_authority/field_merge_policy`ï¼ˆå¯æŒ‰å¯¹è±¡æˆ–æŒ‰å­—æ®µå­—å…¸è¡¨è¾¾ï¼‰ã€‚
- **é£Žé™©**ï¼šå­—æ®µçº§è§„åˆ™ä¼šå¢žåŠ å¤æ‚åº¦ï¼›éœ€è¦ä»Žå°‘é‡é«˜ä»·å€¼å­—æ®µï¼ˆphoto_datetime/location/tags/description ç­‰ï¼‰å¼€å§‹é€æ­¥æ‰©å±•ã€‚

## P1ï¼ˆå»ºè®®ä½œä¸ºä¸‹ä¸€è½®ç ”ç©¶/ææ¡ˆæ·±åŒ–ï¼‰

### P1-1ï¼šè¿žç»­æµç»Ÿä¸€ä¸º `stream + event(timestamp,duration,payload)` åŽŸå­

- **å‘çŽ°æ¥æº**ï¼šActivityWatch buckets/events/heartbeats æ•°æ®æ¨¡åž‹ã€‚
- **è¦ç‚¹**ï¼š
  - æ¯ä¸ªæ¥æºä¸€ä¸ª stream/bucketï¼›
  - heartbeat merge ç”¨äºŽé™å™ªï¼›
  - åŽç»­å†æ´¾ç”Ÿ sessionã€daily timelineã€memoriesã€‚
- **æ”¶ç›Š**ï¼šä¸ºæœªæ¥éŸ³é¢‘/å¯ç©¿æˆ´/å±å¹•æ´»åŠ¨æ‰“åŸºç¡€ï¼›åˆ‡æ®µæ¨¡åž‹ç»Ÿä¸€ã€‚
- **é£Žé™©**ï¼šæ—©åšä¼šå¼•å…¥å¤æ‚åº¦ï¼›å¯å…ˆå†™â€œæœªæ¥å…¼å®¹å­—æ®µâ€ä½†ä¸è½åœ°æ•°æ®é‡ã€‚

### P1-2ï¼šåŒ»ç–—åŸŸé‡‡ç”¨â€œFHIR èµ„æºå‘½å + è¯æ®æŒ‚è½½ + äººç±»å¯è¯»è§£é‡Šå±‚â€

- **å‘çŽ°æ¥æº**ï¼šFasten Healthï¼ˆPHR èšåˆï¼ŒFHIR/SMARTï¼‰ã€‚
- **è¦ç‚¹**ï¼š
  - Encounter/Observation/Medication/Condition/Procedure/Coverage/Claimï¼›
  - æ¯ä¸ªèµ„æºæŒ‚è½½ evidenceï¼ˆPDF/æˆªå›¾/é‚®ä»¶ï¼‰ï¼›
  - è§£é‡Šå±‚ï¼šæŠŠç¼–ç ï¼ˆLOINC/SNOMED ç­‰ï¼‰ç¿»è¯‘æˆå¯è¯»æè¿°ï¼ˆå…ˆä½œä¸ºæ–‡æ¡£çº¦å®šï¼Œä¸åšè‡ªåŠ¨åŒ–ï¼‰ã€‚
- **æ”¶ç›Š**ï¼šåŒ»ç–—ä¿¡æ¯å¯ç»„åˆä¸Žå¯è¿½æº¯ï¼›ä¾¿äºŽç”Ÿæˆå°±åŒ»æ—¶é—´çº¿ä¸Žé—®é¢˜æ¸…å•ã€‚
- **é£Žé™©**ï¼šFHIR ç²’åº¦è¿‡ç»†ä¼šæ‹–æ…¢è½åœ°ï¼›éœ€è¦å®šä¹‰â€œæœ€å°å­—æ®µé›†â€ã€‚

### P1-3ï¼šè´¢åŠ¡åŸŸæ‹†åˆ†â€œè¯æ® vs ç»“æž„åŒ–æ¡ç›® vs è§„åˆ™/å‘¨æœŸâ€

- **å‘çŽ°æ¥æº**ï¼šFirefly IIIï¼ˆäº¤æ˜“å¯¹è±¡åˆ†å±‚ã€è§„åˆ™ã€recurringï¼‰ï¼›Actualï¼ˆlocal-firstï¼‰ã€‚
- **è¦ç‚¹**ï¼š
  - ç¥¨æ®/è´¦å•/é‚®ä»¶ä½œä¸º evidenceï¼›
  - transaction/subscription/deadline ä½œä¸ºç»“æž„åŒ–æ¡ç›®ï¼›
  - recurring æ˜¯ä¸€ç­‰å¯¹è±¡ï¼Œé©±åŠ¨ä»»åŠ¡/æé†’æ´¾ç”Ÿã€‚
- **æ”¶ç›Š**ï¼šä»Žâ€œæœç´¢æ–‡æ¡£æ‰¾è´¦å•â€å‡çº§ä¸ºâ€œç»“æž„åŒ–æé†’ä¸Žå¯¹è´¦â€ã€‚
- **é£Žé™©**ï¼šè·¨é“¶è¡Œ/ä¿¡ç”¨å¡å¯¼å…¥æ ¼å¼å·®å¼‚å¤§ï¼›å…ˆæ–‡æ¡£åŒ– schema ä¸Žå­—æ®µå‘½åå³å¯ã€‚

### P1-4ï¼šå°†â€œç®¡çº¿è§„åˆ™â€å†™æˆ Paperless é£Žæ ¼çš„ `triggers + filters + actions` è¯´æ˜Žä¹¦ï¼ˆstage-awareï¼‰

- **å‘çŽ°æ¥æº**ï¼šPaperless-ngx Workflowsï¼ˆè§¦å‘å™¨/åŠ¨ä½œã€é¡ºåºæ‰§è¡Œã€è¦†ç›–/åˆå¹¶è¯­ä¹‰ã€å®šæ—¶è§¦å‘ï¼‰ï¼›ä»¥åŠå…¶ç¤¾åŒº/issue å¯¹â€œOCR å°šæœªå®Œæˆæ—¶å­—æ®µä¸å¯ç”¨â€çš„æé†’ã€‚
- **è¦ç‚¹**ï¼š
  - è§„åˆ™æ˜¾å¼æ ‡æ³¨ `pipeline_stage`ï¼ˆingest/parse/ocr/extract/review/finalï¼‰ï¼Œå¹¶åˆ—å‡ºè¯¥é˜¶æ®µå¯ç”¨å­—æ®µï¼›
  - å®šä¹‰å•å€¼å­—æ®µè¦†ç›– vs å¤šå€¼å­—æ®µåˆå¹¶çš„å›ºå®šè¯­ä¹‰ï¼›
  - è§„åˆ™å‘½ä¸­åŽçš„å…ƒæ•°æ®å˜æ›´å†™å…¥å®¡è®¡è®°å½•ï¼ˆä»…æ–‡æ¡£çº¦å®šï¼‰ã€‚
- **æ”¶ç›Š**ï¼šå¯è§£é‡Šã€å¯è°ƒè¯•ã€å¯é•¿æœŸç»´æŠ¤ï¼›ä¸ºæœªæ¥å®žçŽ°è‡ªåŠ¨åŒ–æ‰§è¡Œå™¨/åŒæ­¥å™¨é¢„ç•™ç¨³å®šæŽ¥å£ã€‚
- **é£Žé™©**ï¼šæ–‡æ¡£å†™å¾—å¤ªæŠ½è±¡ä¼šå¤±æ•ˆï¼›éœ€è¦ç”¨â€œè·¨åŸŸæ ·ä¾‹â€ï¼ˆé‚®ä»¶è´¦å•/åŒ»ç–—åŒ–éªŒå•/æˆªå›¾éªŒè¯ç /ç…§ç‰‡äº‹ä»¶ï¼‰æ¥æ ¡å‡†ã€‚

### P1-5ï¼šå¼•å…¥â€œappend-only å˜æ›´æ—¥å¿— + èµ„äº§å¼•ç”¨ï¼ˆchecksum-in-URLï¼‰â€ä½œä¸ºæœªæ¥åŒæ­¥/å®¡è®¡æ ¼å¼é¢„æ¡ˆï¼ˆReceipts é£Žæ ¼ï¼‰

- **å‘çŽ°æ¥æº**ï¼šReceipts Space / Receipts App çš„ File-over-App æ•°æ®æ ¼å¼ï¼š`info.json` + `transactions/`ï¼ˆappend-only JSON/JSONLï¼Œheader å« checksum/å¯é€‰é“¾å¼å“ˆå¸Œï¼‰+ `assets/`ï¼ˆäºŒè¿›åˆ¶é™„ä»¶ï¼Œå¼•ç”¨æºå¸¦ checksum/size/mime/nameï¼‰ã€‚
- **è¦ç‚¹**ï¼š
  - å°†â€œå…ƒæ•°æ®å˜æ›´/çº é”™/æ’¤é”€â€ä¼˜å…ˆè½åœ¨ **æ ¼å¼** å±‚ï¼šæ¯æ¬¡å˜æ›´è¿½åŠ ä¸€æ¡ log entryï¼ˆè€Œä¸æ˜¯è¦†ç›–å†™ï¼‰ï¼›
  - èµ„äº§ï¼ˆPDF/å›¾ç‰‡/åŽŸå§‹é™„ä»¶ï¼‰ç”¨ `asset://` å¼•ç”¨ç»Ÿä¸€è¡¨è¾¾ï¼Œå¼•ç”¨å†…åµŒ checksum ä¸Žå¤§å°ï¼Œå®žçŽ°â€œå¼•ç”¨å³æ ¡éªŒâ€ï¼›
  - é¢„ç•™ `clientId/did` ä¸Ž LWWï¼ˆLamport clockï¼‰è¯­ä¹‰ï¼Œä½†å½“å‰é˜¶æ®µåªä½œä¸ºæ–‡æ¡£çº¦å®šï¼Œä¸è½åœ°åŒæ­¥å™¨ã€‚
- **æ”¶ç›Š**ï¼šå¤©ç„¶å®¡è®¡è½¨è¿¹ï¼›æœªæ¥è·¨è®¾å¤‡/å¤–éƒ¨ç¡¬ç›˜/åŒæ­¥ç›˜æ›´ç¨³ï¼›å¯¼å‡º/è¿ç§»æ—¶ä¸ä¾èµ–å•ä¸€ DBã€‚
- **é£Žé™©**ï¼šæ ¼å¼ä¸€æ—¦ç¡®å®šä¼šå½±å“åŽç»­å·¥å…·é“¾ï¼›éœ€è¦å…ˆç”¨ 1-2 ä¸ªåŸŸï¼ˆä¾‹å¦‚ receipts/billsï¼‰åšæœ€å°è¯•ç‚¹è§„èŒƒã€‚
## 2026-05-13 11:20 EDT æ–°å¢žå€™é€‰é¡¹

### P0-6ï¼šæ ‡ç­¾å¿…é¡»æ˜¾å¼å£°æ˜Ž `scope` ä¸Ž `aggregation_level`

- **å‘çŽ°æ¥æº**ï¼šNotmuch/afew çš„ message vs thread æ ‡ç­¾ä¼ æ’­ï¼›Basic Memory çš„ observation/relation åŽŸå­åŒ–ï¼›Immich duplicate groupsï¼›Actual/Firefly çš„ schedule/transaction åˆ†ç¦»ã€‚
- **è¦ç‚¹**ï¼š
  - æ–°å¢ž `scope`: `asset | message | thread | attachment | chunk | observation | relation | schedule | transaction | event | task`ã€‚
  - æ–°å¢ž `aggregation_level`: `atomic | thread | session | event_cluster | duplicate_cluster | daily_view`ã€‚
  - è§„åˆ™å’Œå­—æ®µå˜æ›´å¿…é¡»å£°æ˜Žä½œç”¨åŸŸï¼Œé¿å…â€œçº¿ç¨‹æ ‡ç­¾è¦†ç›–å•å°é‚®ä»¶äº‹å®žâ€æˆ–â€œduplicate group æ ‡ç­¾æ±¡æŸ“åŽŸå§‹èµ„äº§â€ã€‚
- **æ”¶ç›Š**ï¼šè·¨é‚®ä»¶ã€èŠå¤©ã€ç…§ç‰‡ã€æ–‡æ¡£ã€è´¢åŠ¡ã€åŒ»ç–—çš„æ ‡ç­¾è¯­ä¹‰æ›´ç¨³å®šï¼›æ–¹ä¾¿æƒé™è£å‰ªå’Œè¯æ®å›žæ‹‰ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ‰€æœ‰ `labels` å¢žåŠ  `scope`ï¼›æ‰€æœ‰ rule/action å¢žåŠ  `target_scope`ã€‚
- **é£Žé™©**ï¼šå­—æ®µå˜å¤šï¼›éœ€è¦é»˜è®¤å€¼ï¼Œå¦åˆ™æ—©æœŸæ‰‹å·¥ç»´æŠ¤æˆæœ¬ä¸Šå‡ã€‚

### P0-7ï¼šé•¿æœŸè®°å¿†é‡‡ç”¨ atomic `memory_observation` + typed `entity_relation` + version history

- **å‘çŽ°æ¥æº**ï¼šBasic Memory çš„ observations/relationsï¼›Memento MCP çš„ entity/observation/version historyï¼›æ—¢æœ‰ provenance/claim_state ææ¡ˆã€‚
- **è¦ç‚¹**ï¼š
  - `memory` ä¸ç›´æŽ¥ç­‰åŒ summaryï¼›é•¿æœŸå±‚æœ€å°å•ä½åº”æ˜¯å•æ¡äº‹å®ž/åå¥½/ç»åŽ†/å†³å®š/é£Žé™©ã€‚
  - `entity_relation` è¡¨ç¤º person/place/account/project/device/document/event ä¹‹é—´çš„ typed edgeã€‚
  - æ¯æ¬¡æŠ½å–ã€åˆå¹¶ã€äººå·¥ä¿®æ”¹ã€æ’¤å›žä¿ç•™ç‰ˆæœ¬ä¸Ž `supersedes/conflicts_with/derived_from`ã€‚
- **æ”¶ç›Š**ï¼šå‡å°‘â€œä¸€ä¸ª summary é‡Œæ··å…¥å¤šä¸ªäº‹å®žå¯¼è‡´ä¸å¯çº é”™â€çš„é—®é¢˜ï¼›æ›´é€‚åˆ 5+ å¹´ç»´æŠ¤ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢ž `memory_observation`ã€`entity_relation`ã€`memory_version` æˆ–ç­‰ä»· sidecar ç»“æž„ã€‚
- **é£Žé™©**ï¼šåŽŸå­åŒ–è¿‡ç»†ä¼šåˆ¶é€ å™ªå£°ï¼›éœ€è¦ extraction budget ä¸Ž review gateã€‚

### P1-6ï¼šé‚®ä»¶/ç”Ÿæ´»è¡Œæ”¿é‡‡ç”¨ `email_message -> email_thread -> attachment -> derived_item` åˆ†å±‚

- **å‘çŽ°æ¥æº**ï¼šNotmuch åˆå§‹æ ‡ç­¾ã€thread æœç´¢/è¾“å‡ºã€special tagsï¼›afew çš„è‡ªåŠ¨æ ‡ç­¾ä¸Ž thread æ ‡ç­¾ä¼ æ’­ã€‚
- **è¦ç‚¹**ï¼š
  - `email_message` ä¿å­˜ Message-IDã€headersã€MIMEã€hashã€raw evidenceã€‚
  - `email_thread` ä¿å­˜å‚ä¸Žè€…ã€ä¸»é¢˜ã€æ—¶é—´èŒƒå›´ã€èšåˆæ ‡ç­¾ã€æœ€é«˜æ•æ„Ÿåº¦ã€‚
  - `email_attachment` ä¿å­˜ PDF/å›¾ç‰‡/ICS/CSV ç­‰èµ„äº§å¼•ç”¨ã€‚
  - æ´¾ç”Ÿ `bill/receipt/deadline/account_notice/security_notice/contact_update/task/event`ã€‚
- **æ”¶ç›Š**ï¼šæ—§é‚®ç®±ä¸Žæ–°é‚®ç®±éƒ½èƒ½ä»¥ thread ä¸ºäººç±»å¯è¯»è§†å›¾ï¼ŒåŒæ—¶ä¿ç•™ message çº§è¯æ®ã€‚
- **é£Žé™©**ï¼šthread èšåˆä¼šæ‰©å¤§æ•æ„ŸèŒƒå›´ï¼›å¿…é¡»é‡‡ç”¨ max(child.sensitivity) å¹¶æŒ‰ message/attachment è£å‰ªæƒé™ã€‚

### P1-7ï¼šè´¢åŠ¡å¢žåŠ  `reconciliation_link`ï¼Œåˆ†ç¦»è¯æ®ã€å€™é€‰é¡¹ã€çœŸå®žäº¤æ˜“ä¸Žå‘¨æœŸä¹‰åŠ¡

- **å‘çŽ°æ¥æº**ï¼šActual schedules/rulesï¼›Firefly III transaction group/journal/transactionã€subscriptionsã€recurring transactionsï¼›Reddit å¯¹ receipt OCR/line-item extraction éš¾ç‚¹çš„è®¨è®ºã€‚
- **è¦ç‚¹**ï¼š
  - `financial_evidence`ï¼šè´¦å• PDFã€æ”¶æ®ç…§ç‰‡ã€é‚®ä»¶ã€CSVã€é“¶è¡Œå¯¼å‡ºã€‚
  - `finance_item_candidate`ï¼šOCR/é‚®ä»¶/è§„åˆ™æŠ½å–å€™é€‰é‡‘é¢ã€å•†æˆ·ã€due dateã€‚
  - `transaction`ï¼šäººå·¥ç¡®è®¤æˆ–å¯é å¯¼å…¥åŽçš„çœŸå®žè®°è´¦äº‹ä»¶ã€‚
  - `subscription_or_bill_schedule`ï¼šå‘¨æœŸä¹‰åŠ¡/é¢„æœŸæ”¯å‡ºã€‚
  - `reconciliation_link`ï¼šè¯æ®ã€å€™é€‰é¡¹ã€äº¤æ˜“ã€schedule çš„åŒ¹é…å…³ç³»ä¸Žç½®ä¿¡åº¦ã€‚
- **æ”¶ç›Š**ï¼šé¿å…æŠŠ OCR å€™é€‰è¯¯å½“æˆè´¢åŠ¡äº‹å®žï¼›æ”¯æŒè´¦å•æé†’å’ŒåŽç»­å¯¹è´¦ã€‚
- **é£Žé™©**ï¼šå®Œæ•´è´¢åŠ¡æ¨¡åž‹å®¹æ˜“è¿‡é‡ï¼›ç¬¬ä¸€ç‰ˆåº”åªåš evidence/candidate/deadline/reconciliationï¼Œæš‚ä¸åšè‡ªåŠ¨å†³ç­–ã€‚

### P1-8ï¼šå…³ç³»åŸŸæ‹†ä¸º `person_profile`ã€`relationship_edge`ã€`interaction`ã€`relationship_reminder`

- **å‘çŽ°æ¥æº**ï¼šMonica personal CRM çš„ contactsã€relationshipsã€activitiesã€remindersã€birthday remindersã€notesã€documents/photosã€multiple vaults/labelsã€‚
- **è¦ç‚¹**ï¼š
  - `person_profile`ï¼šå§“åã€åˆ«åã€ç”Ÿæ—¥ã€è”ç³»æ–¹å¼ã€åœ°å€ã€æ¥æºã€æ•æ„Ÿçº§åˆ«ã€‚
  - `relationship_edge`ï¼šæœ‰æ–¹å‘ã€æœ‰ç±»åž‹ã€æœ‰ç½®ä¿¡åº¦ã€æœ‰æœ‰æ•ˆæœŸçš„å…³ç³»è¾¹ã€‚
  - `interaction`ï¼šè§é¢ã€ç”µè¯ã€é‚®ä»¶ã€èŠå¤©ã€ç¤¼ç‰©ã€å¸®åŠ©ã€å…±åŒäº‹ä»¶ç­‰æ—¥å¿—ã€‚
  - `relationship_reminder`ï¼šç”Ÿæ—¥ã€çºªå¿µæ—¥ã€å¤šä¹…æ²¡è”ç³»ã€æ‰¿è¯ºäº‹é¡¹ã€‚
- **æ”¶ç›Š**ï¼šå…¨ç”Ÿæ´»æ•°æ®åº“éœ€è¦é•¿æœŸç»´æŠ¤äººé™…èƒŒæ™¯ï¼Œä¸èƒ½åªä½œä¸ºæ™®é€š memory/tagã€‚
- **é£Žé™©**ï¼šç¬¬ä¸‰æ–¹éšç§é«˜ï¼›å…³ç³»è¾¹å¿…é¡»é»˜è®¤å€™é€‰ã€local_onlyï¼Œæ•æ„Ÿå­—æ®µç¦æ­¢é»˜è®¤åŒæ­¥ã€‚

### P1-9ï¼šåŒ»ç–—é‡‡ç”¨ FHIR-inspired æœ€å°è§†å›¾ï¼Œè€Œä¸æ˜¯å®Œæ•´ FHIR æˆ–çº¯ OCR æ–‡æ¡£

- **å‘çŽ°æ¥æº**ï¼šHL7 Personal Health Record Format IG çš„ PHR data modelï¼›Fasten Health çš„ self-hosted PHR/FHIR æ–¹å‘ã€‚
- **è¦ç‚¹**ï¼š
  - æœ€å°è§†å›¾å»ºè®®è¦†ç›– `Patient/RelatedPerson/Practitioner/Encounter/Appointment/Condition/Observation/DiagnosticReport/MedicationStatement/Immunization/Procedure/AllergyIntolerance/DocumentReference/Claim/Coverage/Device/Provenance`ã€‚
  - `Observation` å¿…é¡»ç»†åˆ† `lab_result/vital/symptom/wearable/patient_reported`ã€‚
  - æ¯ä¸ªåŒ»ç–—å¯¹è±¡é»˜è®¤ evidence-backedã€local_onlyã€review_requiredã€‚
- **æ”¶ç›Š**ï¼šèƒ½å›žç­”å°±è¯Šæ—¶é—´çº¿ã€åŒ–éªŒè¶‹åŠ¿ã€å¤„æ–¹åŽ†å²ã€ä¿é™©/è´¦å•å…³è”ï¼Œè€Œä¸éœ€è¦å®žçŽ°å®Œæ•´ EHRã€‚
- **é£Žé™©**ï¼šåŒ»ç–—è‡ªåŠ¨åŒ–é£Žé™©é«˜ï¼›ä»…ç”¨äºŽå½’æ¡£ã€æ£€ç´¢ã€å°±è¯Šå‡†å¤‡ï¼Œä¸åšè¯Šæ–­/ç”¨è¯/ç†èµ”å†³ç­–ã€‚

### P1-10ï¼šåª’ä½“/æ–‡æ¡£åŽ»é‡ä»¥ duplicate cluster ä¸ºå¯¹è±¡ï¼Œä¸è‡ªåŠ¨åˆ é™¤åŽŸä»¶

- **å‘çŽ°æ¥æº**ï¼šImmich duplicate utility çš„ reviewã€keep preselectionã€metadata sync/stackï¼›PhotoPrism originals/storage/sidecar åˆ†ç¦»ï¼›Reddit å¯¹â€œImmich for documentsâ€çš„æ–‡ä»¶å¤¹è§†å›¾å’ŒåŽŸä»¶ä¸ä¿®æ”¹éœ€æ±‚ã€‚
- **è¦ç‚¹**ï¼š
  - æ–°å¢ž `duplicate_group_id / representative_asset_id / keep_reason / duplicate_review_state / stack_members`ã€‚
  - `original_path`ã€`display_folder`ã€`logical_collection` åˆ†ç¦»ã€‚
  - é«˜æ•æ„Ÿ metadataï¼ˆGPSã€äººè„¸ã€åŒ»ç–—/è´¢åŠ¡æ–‡æ¡£ç±»åž‹ï¼‰é»˜è®¤ä¸è‡ªåŠ¨åˆå¹¶ã€‚
- **æ”¶ç›Š**ï¼šç…§ç‰‡ã€æˆªå›¾ã€PDFã€é™„ä»¶å¯ä»¥ç»Ÿä¸€åŽ»é‡ï¼ŒåŒæ—¶ä¿ç•™åŽŸå§‹è¯æ®å’Œç”¨æˆ·å¯ç†è§£è§†å›¾ã€‚
- **é£Žé™©**ï¼šè‡ªåŠ¨åˆå¹¶ caption/æ ‡ç­¾å¯èƒ½æ‰©æ•£é”™è¯¯ï¼›é»˜è®¤åªç”Ÿæˆå»ºè®®ï¼Œäººå·¥ç¡®è®¤åŽåˆå¹¶ã€‚

## 2026-05-13 12:00 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆClaude / DeepSeek ä¿¡æ¯æŠ½è±¡ï¼‰

### P0-8ï¼šæ–°å¢ž `context_routing_index`ï¼ŒæŠŠâ€œå¸¸é©»ä¸Šä¸‹æ–‡â€åŽ‹æˆè·¯ç”±ç´¢å¼•

- **å‘çŽ°æ¥æº**ï¼šClaude Code layered memory issueï¼ˆslim index + topic files + semantic searchï¼‰ï¼›Anthropic Skills çš„æŒ‰éœ€åŠ è½½è¯´æ˜Žä¹¦æ¨¡å¼ã€‚
- **è¦ç‚¹**ï¼š
  - å¸¸é©»å±‚åªæ”¾ä¸»é¢˜ã€å…³é”®è¯ã€çŠ¶æ€ã€æ•æ„Ÿçº§åˆ«ã€detail_refsï¼Œä¸æ”¾å®Œæ•´è®°å¿†ã€‚
  - æ¯ä¸ª topic/domain/entity å¯æœ‰æŒ‰éœ€åŠ è½½çš„ detail file æˆ– indexed objectã€‚
  - index æ¡ç›®æœ¬èº«ä¹Ÿè¦æœ‰ `sensitivity`ã€`sync_permission`ã€`redacted_title`ã€‚
- **æ”¶ç›Š**ï¼šé¿å… personal database å˜æˆå·¨å¤§ always-loaded memoryï¼›æ›´é€‚åˆ 5+ å¹´ä½¿ç”¨ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢ž `context_routing_index`ï¼Œå¹¶åœ¨æ£€ç´¢æµç¨‹ä¸­å…ˆ route å† pull evidence/detailã€‚
- **é£Žé™©**ï¼šç´¢å¼•è¿‡ç²—ä¼šæ¼å¬å›žï¼›è¿‡ç»†ä¼šæ³„éœ²æ•æ„Ÿä¸»é¢˜æˆ–é‡æ–°è†¨èƒ€ã€‚

### P0-9ï¼šchunk å±‚å¢žåŠ  `contextual_prefix`ï¼Œæ”¯æŒ Contextual Retrieval

- **å‘çŽ°æ¥æº**ï¼šAnthropic Contextual Retrieval / Claude Cookbooksï¼šç»™ chunk åŠ æ–‡æ¡£çº§çŸ­ä¸Šä¸‹æ–‡ï¼Œå†ç”¨äºŽ embedding/BM25/rerankingã€‚
- **è¦ç‚¹**ï¼š
  - æ¯ä¸ª chunk ä¿ç•™ raw textï¼ŒåŒæ—¶ç”Ÿæˆæ£€ç´¢ä¸“ç”¨ `contextual_prefix`ã€‚
  - `contextual_prefix` å¿…é¡»å¸¦ `generated_by/generated_at/source_prompt_version`ï¼Œå¯é‡æ–°ç”Ÿæˆã€‚
  - é«˜æ•æ„Ÿ chunk å¯åªåš local BM25 æˆ– redacted prefixï¼Œä¸é€å¤–éƒ¨ embeddingã€‚
- **æ”¶ç›Š**ï¼šå‡å°‘ chunk è„±ç¦»æ–‡æ¡£/é‚®ä»¶ thread/åŒ»ç–—æŠ¥å‘Š/è´¦å•å‘¨æœŸåŽæ£€ç´¢å¤±è´¥ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼š`content_chunk` æ–°å¢ž `contextual_prefix/document_outline_ref/section_path/bm25_text`ã€‚
- **é£Žé™©**ï¼šLLM prefix å¯èƒ½å¼•å…¥åå·®ï¼Œä¸èƒ½å½“ä½œäº‹å®žå±‚ã€‚

### P1-11ï¼šæ–°å¢ž `assistant_handoff` ä¸Ž `context_event_log`ï¼ŒæŠŠ AI å·¥ä½œçŠ¶æ€ä¹Ÿä½œä¸ºè¿‡ç¨‹è®°å½•

- **å‘çŽ°æ¥æº**ï¼šClaude Code persistent memory / compaction issuesã€Anthropic cwc-long-running-agentsã€MCP Memory Keeperã€‚
- **è¦ç‚¹**ï¼š
  - åœ¨ stop/pre-compact/manual checkpoint æ—¶å†™ handoffã€‚
  - è®°å½• working_goalã€decisionsã€open_questionsã€evidence_seenã€candidate_objects_createdã€review_items_pendingã€next_actionsã€‚
  - ä¸Ž append-only audit/change log åŒºåˆ†ï¼šhandoff æ˜¯å·¥ä½œçŠ¶æ€ï¼Œaudit æ˜¯å¯è¿½è´£äº‹ä»¶ã€‚
- **æ”¶ç›Š**ï¼šé•¿ä»»åŠ¡ã€è‡ªåŠ¨åŒ–ã€å¹¶è¡Œ agentã€è·¨ session éƒ½èƒ½æ¢å¤ä¸Šä¸‹æ–‡ï¼Œä¸ä¾èµ–èŠå¤©çª—å£ã€‚
- **é£Žé™©**ï¼šæ—¥å¿—è†¨èƒ€ï¼›handoff å¯èƒ½åŒ…å«æ•æ„Ÿè·¯å¾„/åå¥½/é¡¹ç›®çŠ¶æ€ï¼Œéœ€è¦ sensitivity æ ‡æ³¨ã€‚

### P1-12ï¼šæ–°å¢ž `candidate_verification` passï¼Œé«˜é£Žé™©å€™é€‰å…ˆè‡ªæ£€å†è¿›å…¥ review

- **å‘çŽ°æ¥æº**ï¼šDeepSeek-R1 å¼ºè°ƒ self-verification/reflectionï¼›Claude long-running agent çš„ evaluator/fresh-context review æ¨¡å¼ã€‚
- **è¦ç‚¹**ï¼š
  - candidate extraction åŽå¢žåŠ ç»“æž„åŒ– verification outcomeã€‚
  - å­—æ®µåŒ…æ‹¬ `checked_against_evidence_refs`ã€`contradiction_found`ã€`missing_evidence`ã€`confidence_delta`ã€`recommended_review_state`ã€‚
  - ä¸ä¿å­˜éšè—æŽ¨ç†é“¾ï¼Œåªä¿å­˜å¯å®¡è®¡çš„éªŒè¯ç»“æžœã€‚
- **æ”¶ç›Š**ï¼šåŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€å…³ç³»å€™é€‰èƒ½æ›´æ—©æš´éœ²è¯æ®ä¸è¶³æˆ–å†²çªï¼Œå‡è½»äººå·¥ review åŽ‹åŠ›ã€‚
- **é£Žé™©**ï¼šè‡ªæ£€ä¸èƒ½æ›¿ä»£äººå·¥ç¡®è®¤ï¼›éªŒè¯æ¨¡åž‹ä¹Ÿå¯èƒ½é”™ã€‚

### P1-13ï¼šæ£€ç´¢è¡¨ç¤ºæ‹†æˆ `latent_summary + sparse_keys + exact_ref`

- **å‘çŽ°æ¥æº**ï¼šDeepSeek-V3 MLA / FlashMLA çš„åŽ‹ç¼© KV cacheã€token-level sparse attentionã€FP8 KV cacheï¼›è½¬è¯‘ä¸ºä¿¡æ¯æž¶æž„ç±»æ¯”ã€‚
- **è¦ç‚¹**ï¼š
  - `latent_summary` è´Ÿè´£å¬å›žå’Œç²—è·¯ç”±ã€‚
  - `sparse_keys` è´Ÿè´£å®žä½“ã€æ—¥æœŸã€é‡‘é¢ã€ä»£ç ã€å…³é”®è¯è¿‡æ»¤ã€‚
  - `exact_ref` è´Ÿè´£å›žæ‹‰åŽŸæ–‡ã€é¡µç ã€OCR regionã€message idã€timestampã€‚
- **æ”¶ç›Š**ï¼šä¸æŠŠå®Œæ•´åŽŸæ–‡å¸¸é©»æˆ–å…¨é‡ embed å½“é»˜è®¤ï¼ŒåŒæ—¶ä¿ç•™ç²¾ç¡®è¯æ®å›žæ‹‰ã€‚
- **é£Žé™©**ï¼šDeepSeek MLA æ˜¯æ¨¡åž‹å†…éƒ¨æœºåˆ¶ï¼Œä¸èƒ½æœºæ¢°æ˜ å°„åˆ°æ•°æ®åº“ï¼›è¿™é‡Œåªä½œä¸º P1 çº§è®¾è®¡å¯å‘ã€‚

## 2026-05-13 12:21 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆfield cardinality / medical / email / relationship safetyï¼‰

### P0-10ï¼šæ–°å¢ž `field_contract`ï¼Œæ˜¾å¼å£°æ˜Žå­—æ®µåŸºæ•°ä¸Žåˆå¹¶è¯­ä¹‰

- **å‘çŽ°æ¥æº**ï¼šLinkML slots/cardinalityï¼ˆ`required`ã€`multivalued`ã€`minimum_cardinality`ã€`maximum_cardinality`ã€UML `0..1/1/0..*/1..*`ï¼‰ï¼›Logseq DB properties çš„ typed property / multi-value / tag properties æ¨¡å¼ã€‚
- **è¦ç‚¹**ï¼š
  - ä¸ºé«˜ä»·å€¼å­—æ®µå¢žåŠ  `field_contract`ï¼š`field_name/scope/cardinality/value_type/ordered/merge_semantics/conflict_policy/default_review_state/sensitivity_floor/sync_floor/provenance_required`ã€‚
  - å»ºè®®åˆå¹¶è¯­ä¹‰è¯è¡¨ï¼š`replace_by_authority`ã€`append_unique`ã€`append_versioned`ã€`max_sensitivity`ã€`min_sync_permission`ã€`union_tags`ã€`intersect_permissions`ã€`manual_only`ã€`derive_only`ã€`no_merge_cluster_only`ã€‚
  - å…ˆè¦†ç›–è·¨åŸŸå­—æ®µå’Œé«˜é£Žé™©å­—æ®µï¼šidentityã€timestampsã€sensitivityã€sync_permissionã€review_stateã€entity_refsã€evidence_refsã€medical valuesã€finance amountsã€contact fieldsã€relationship edgesã€‚
- **æ”¶ç›Š**ï¼šæŠŠâ€œå­—æ®µèƒ½ä¸èƒ½å¤šå€¼ã€å†²çªæ—¶æ€Žä¹ˆåˆå¹¶ã€æ˜¯å¦éœ€è¦äººå·¥ç¡®è®¤â€ä»Žå®žçŽ°ç»†èŠ‚æå‡åˆ° IA è§„èŒƒå±‚ï¼›æ”¯æŒæœªæ¥è§„åˆ™å¼•æ“Žã€å¯¼å…¥å™¨ã€åŒæ­¥å™¨å’Œå®¡è®¡æ—¥å¿—ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šåœ¨ sidecar/frontmatter/rule spec ä¸­å¼•ç”¨ `field_contract`ï¼›è§„åˆ™åŠ¨ä½œå¿…é¡»éµå®ˆå­—æ®µçš„ cardinality ä¸Ž merge semanticsã€‚
- **é£Žé™©**ï¼šå­—æ®µå¥‘çº¦è¿‡æ—©é“ºå¤ªå¹¿ä¼šè†¨èƒ€ï¼›ç¬¬ä¸€ç‰ˆåªç»´æŠ¤ 20-40 ä¸ªæ ¸å¿ƒå­—æ®µï¼Œå…¶ä»–å­—æ®µç»§æ‰¿é»˜è®¤ç­–ç•¥ã€‚

### P1-14ï¼šæŠŠ FHIR-inspired åŒ»ç–—æœ€å°è§†å›¾è½æˆå­—æ®µçŸ©é˜µ

- **å‘çŽ°æ¥æº**ï¼šHL7 FHIR R4 `DocumentReference`ã€`DiagnosticReport`ã€`Observation`ã€`Encounter`ã€`MedicationStatement`ã€‚
- **è¦ç‚¹**ï¼š
  - åŒºåˆ† `medical_document`ï¼ˆè¯æ®/æ–‡æ¡£å¼•ç”¨ï¼‰ã€`medical_encounter`ï¼ˆå°±è¯Šä¸Šä¸‹æ–‡ï¼‰ã€`diagnostic_report`ï¼ˆæŠ¥å‘Š/é¢æ¿ï¼‰ã€`medical_observation`ï¼ˆåŽŸå­ç»“æžœ/ç—‡çŠ¶/ç”Ÿå‘½ä½“å¾/å¯ç©¿æˆ´æ•°æ®ï¼‰ã€`medication_statement`ï¼ˆç”¨è¯é™ˆè¿°ï¼‰ã€‚
  - `Observation` ä¸åªæ˜¯ä¸€æ®µ OCR æ–‡æœ¬ï¼Œåº”è‡³å°‘æœ‰ `status/code/value/unit/reference_range/effective_at_or_period/encounter_ref/derived_from_refs`ã€‚
  - `DiagnosticReport` è´Ÿè´£æŠŠå¤šä¸ª observation ç»„åˆæˆæŠ¥å‘Šï¼Œå¹¶ä¿ç•™ `presented_form_ref` å›žæ‹‰åŽŸå§‹ PDF/æˆªå›¾ã€‚
  - `MedicationStatement` è¡¨ç¤ºâ€œè¢«æŠ¥å‘Šçš„ç”¨è¯äº‹å®žâ€ï¼Œä¸ç­‰åŒäºŽå¤„æ–¹ã€å‘è¯æˆ–å®žé™…æœè¯äº‹ä»¶ã€‚
- **æ”¶ç›Š**ï¼šä¸ªäºº DB å¯ä»¥å›žç­”å°±è¯Šæ—¶é—´çº¿ã€åŒ–éªŒè¶‹åŠ¿ã€å¤„æ–¹/ç”¨è¯åŽ†å²ã€ä¿é™©/è´¦å•å…³è”ï¼ŒåŒæ—¶é¿å…å®žçŽ°å®Œæ•´ EHRã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šP1-9 éœ€è¦è¡¥å……æœ€å°å­—æ®µè¡¨å’Œé»˜è®¤ review/privacy ç­–ç•¥ï¼›åŒ»ç–—å¯¹è±¡å¿…é¡» evidence-backedã€‚
- **é£Žé™©**ï¼šåŒ»ç–—è‡ªåŠ¨åŒ–é£Žé™©é«˜ï¼›é»˜è®¤ `medical_high/local_only/review_required/claim_state=candidate`ï¼Œåªç”¨äºŽå½’æ¡£ã€æ£€ç´¢ã€å°±è¯Šå‡†å¤‡ï¼Œä¸åšè¯Šæ–­/ç”¨è¯/ç†èµ”å†³ç­–ã€‚

### P1-15ï¼šé‚®ä»¶ ingest åˆ†ç¦» `ingest_tags`ã€`mail_client_flags` ä¸Ž thread rollup labels

- **å‘çŽ°æ¥æº**ï¼šNotmuch initial tagging çš„ `new -> post-processing -> inbox/unread` å·¥ä½œæµï¼›Notmuch special tags å¯¹ Maildir flagsã€attachmentã€signedã€encrypted çš„åŒºåˆ†ã€‚
- **è¦ç‚¹**ï¼š
  - `email_raw_message` ä¿ç•™ `message_id/thread_key/mailbox_account/folder_or_label_snapshot/header_hash/body_hash/mime_structure_ref/attachment_refs/mail_client_flags/ingest_tags`ã€‚
  - `ingest_tags` åªè¡¨ç¤ºç®¡çº¿çŠ¶æ€ï¼š`new/parsed/classified/reviewed/archived_only`ã€‚
  - `mail_client_flags` é•œåƒæºé‚®ç®±çŠ¶æ€ï¼Œä¸ç­‰åŒäºŽä¸ªäººæ•°æ®åº“è¯­ä¹‰ã€‚
  - `email_thread.rollup_labels` ä»Ž child messages/attachments æ´¾ç”Ÿï¼›thread label ä¸è¦†ç›– message-level factsã€‚
  - attachment å¿…é¡»æˆä¸ºç‹¬ç«‹ evidence assetï¼Œå¹¶å›žé“¾ message/threadã€‚
- **æ”¶ç›Š**ï¼šæ—§é‚®ç®±å’Œæ–°é‚®ç®±éƒ½èƒ½å…ˆå®‰å…¨å½’æ¡£ï¼Œå†é€æ­¥æŠ½å– bills/receipts/deadlines/account notices/security notices/contact updates/tasks/eventsã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– P1-6ï¼Œå¹¶ä¸Ž P0-6 çš„ `scope/aggregation_level`ã€P0-10 çš„ `field_contract` è”åŠ¨ã€‚
- **é£Žé™©**ï¼šthread rollup ä¼šæ‰©å¤§æ•æ„ŸèŒƒå›´ï¼›thread å±‚å¿…é¡»é‡‡ç”¨ `max_child_sensitivity` ä¸Ž `min_child_sync_permission`ã€‚

### P1-16ï¼šå…³ç³»å›¾è°±å¢žåŠ  consent-aware edge ä¸Ž field-level privacy

- **å‘çŽ°æ¥æº**ï¼šMonica çš„ contacts/relationships/reminders/activities/notes/documents/photos/custom fieldsï¼›Reddit å¯¹ personal CRM / graph-based relationships çš„éœ€æ±‚ï¼›Relaticle çš„ dynamic custom fields ä¸Ž per-field encryption æ¨¡å¼ã€‚
- **è¦ç‚¹**ï¼š
  - `relationship_edge` å¢žåŠ  `directionality/claim_state/confidence/valid_from/valid_to/evidence_refs/visibility_scope/consent_state/sensitivity/sync_permission`ã€‚
  - `person_profile_field` å¢žåŠ å­—æ®µçº§ `field_sensitivity/field_sync_permission/review_state/cardinality/source`ã€‚
  - é»˜è®¤å€¼ï¼šå…³ç³»å›¾å¯¹è±¡ `local_only`ã€`review_required`ã€ä¸è¿›å…¥å¤–éƒ¨åŒæ­¥/å¤–éƒ¨æ£€ç´¢ï¼Œé™¤éžæ˜¾å¼å…è®¸ã€‚
- **æ”¶ç›Š**ï¼šç”Ÿæ—¥æé†’ã€è”ç³»æ–¹å¼ã€å…±åŒç»åŽ†ã€å®¶åº­å…³ç³»ã€æ•æ„Ÿå†²çªã€ç¬¬ä¸‰æ–¹ç§äººä¿¡æ¯å¯ä»¥å…±äº«åŒä¸€å›¾è°±ï¼Œä½†é‡‡ç”¨ä¸åŒæƒé™å’Œæ£€ç´¢è¡Œä¸ºã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– P1-8ï¼›relationship graph æ£€ç´¢å¿…é¡»æŒ‰ edge/field æƒé™è£å‰ªï¼Œä¸åªæŒ‰ person_profile è£å‰ªã€‚
- **é£Žé™©**ï¼šéšç§å­—æ®µå¢žåŠ äººå·¥ review æˆæœ¬ï¼›ä½†è¿™æ˜¯å…¨ç”Ÿæ´»æ•°æ®åº“å¿…é¡»æ‰¿æ‹…çš„è¾¹ç•Œï¼Œå°¤å…¶æœªæ¥è‹¥æŽ¥å…¥ AI assistant æˆ– Telegram/Hermes åŒæ­¥ã€‚

## 2026-05-13 13:24 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆsource snapshots / import runs / error recordsï¼‰

### P0-11ï¼šæ–°å¢ž `source_snapshot` / `import_run` / `parse_error_record`ï¼ŒæŠŠå¯¼å…¥æ‰¹æ¬¡å’Œè§£æžå¤±è´¥ä¸€ç­‰åŒ–

- **å‘çŽ°æ¥æº**ï¼šHPI/Human Programming Interface çš„æœ¬åœ°æ–‡ä»¶ç³»ç»Ÿ source modulesï¼›cachew çš„è¾“å…¥ hashã€æŒä¹…åŒ–è§£æžç¼“å­˜å’Œ `Exception` å¯åºåˆ—åŒ–æ¨¡å¼ï¼›Dogsheep/Datasette çš„ source-to-SQLite ä¸ªäººæ•°æ®ä»“åº“ï¼›Reddit DataHoarder å¯¹å¤šç¡¬ç›˜å½’æ¡£ã€ä¸­å¤®ç´¢å¼•ã€hash/EXIF/perceptual hash æ—¥å¿—çš„å®žè·µè®¨è®ºã€‚
- **è¦ç‚¹**ï¼š
  - `source_snapshot` è¡¨ç¤ºä¸€æ‰¹è¾“å…¥æ¥æºï¼š`api_export | gdpr_archive | takeout | mailbox_dump | photo_library | filesystem_scan | device_backup | manual_import`ã€‚
  - `import_run` è¡¨ç¤ºä¸€æ¬¡å¯¼å…¥/é‡è·‘/ä¿®å¤ï¼š`full | incremental | replay | repair | dry_run`ï¼Œè®°å½• adapter/parser ç‰ˆæœ¬ã€è¾“å…¥ snapshotã€è¾“å‡ºæ•°é‡ã€é”™è¯¯æ•°é‡ã€‚
  - `parse_error_record` è¡¨ç¤ºè§£æžå¤±è´¥ã€å­—æ®µç¼ºå¤±ã€schema driftã€OCR å¤±è´¥ã€ä½Žç½®ä¿¡ã€é‡å¤å†²çªç­‰ï¼›é”™è¯¯ä¸åªå†™æ—¥å¿—ï¼Œè€Œæ˜¯å¯æ£€ç´¢ã€å¯å®¡é˜…ã€å¯åœ¨è§£æžå™¨å‡çº§åŽé‡è·‘çš„è´¨é‡å¯¹è±¡ã€‚
  - æ‰€æœ‰ evidence/assets/chunks/candidates/errors éƒ½åº”èƒ½å›žé“¾åˆ° `import_run_id`ï¼Œå†å›žé“¾åˆ° `source_snapshot_id`ã€‚
- **æ”¶ç›Š**ï¼šæ—§é‚®ç®±ã€Google Takeoutã€Apple Photos/Immichã€æ—§ç¡¬ç›˜ã€å¥åº·å¯¼å‡ºã€é“¶è¡Œ/è´¦å•å¯¼å‡ºéƒ½èƒ½å¯å¤çŽ°å¯¼å…¥ï¼›æœªæ¥ä¿®å¤ parser åŽå¯ä»¥ç²¾å‡†é‡è·‘å¤±è´¥é¡¹ï¼Œè€Œä¸æ˜¯é‡æ–°æ‰«å…¨åº“ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šåœ¨ inbox/raw_evidence å‰åŽæ–°å¢ž source/import å±‚ï¼›`provenance.record` å¯å¼•ç”¨ `import_run_id`ï¼Œé¿å…é‡å¤å¡žå…¥ adapter/parser ç»†èŠ‚ã€‚
- **é£Žé™©**ï¼šå…ƒæ•°æ®è†¨èƒ€ï¼›source snapshot ä¸Ž error message å¯èƒ½æ³„éœ²è·¯å¾„ã€è´¦æˆ·ã€é‚®ç®± headerã€åŒ»ç–—æœ¯è¯­ï¼Œé»˜è®¤ `local_only` å¹¶ç»§æ‰¿ affected evidence çš„æœ€é«˜ sensitivityã€‚

### P0-12ï¼šä¸ºé•¿æœŸå¯å˜å®žä½“å¼•å…¥å¯é€‰ `object_anchor + attribute_claim` æ¨¡åž‹

- **å‘çŽ°æ¥æº**ï¼šPerkeep permanode/claim schemaï¼šä¸å¯å˜å†…å®¹å¯»å€ blob ä¹‹ä¸Šï¼Œç”¨ç¨³å®š permanode æ‰¿æŽ¥å¯å˜å¯¹è±¡ï¼Œç”¨ `add-attribute / set-attribute / del-attribute` claim è¿½åŠ è¡¨è¾¾å˜æ›´ã€‚
- **è¦ç‚¹**ï¼š
  - `object_anchor` åªæä¾›ç¨³å®šèº«ä»½ï¼Œä¸ç›´æŽ¥æ‰¿è½½ä¼šè¢«è¦†ç›–çš„äº‹å®žã€‚
  - `attribute_claim` è¡¨ç¤º set/add/del/merge/retractï¼Œå¸¦ `claim_date`ã€`claim_state`ã€`review_state`ã€`field_contract`ã€`evidence_refs`ã€`created_by`ã€‚
  - å½“å‰å¯¹è±¡è§†å›¾æ˜¯æŠŠ claims æŒ‰ field_contract å’Œæ—¶é—´é¡ºåº fold å‡ºæ¥çš„ materialized viewã€‚
  - ä¼˜å…ˆç”¨äºŽå¤šå¹´å¯å˜ä¸”é«˜é£Žé™©å¯¹è±¡ï¼š`person_profile`ã€`relationship_edge`ã€`account`ã€`medical_condition`ã€`medication_statement`ã€`subscription_schedule`ã€`property`ã€`vehicle`ã€`device`ã€‚
- **æ”¶ç›Š**ï¼šé¿å…â€œé•¿æœŸå¯¹è±¡è¢«è¦†ç›–å†™ååŽä¸çŸ¥é“åŽ†å²çŠ¶æ€â€çš„é—®é¢˜ï¼›æ”¯æŒæ’¤å›žã€çº é”™ã€å†²çªä¿ç•™ã€æ—¶é—´æœ‰æ•ˆæ€§å’Œå®¡è®¡å›žæ”¾ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– P0-4 provenanceã€P0-5 field authority/merge policyã€P0-10 field_contractï¼›ä¸æ˜¯æ›¿ä»£çŽ°æœ‰å¯¹è±¡è¡¨ï¼Œè€Œæ˜¯ä¸ºé«˜é£Žé™©å¯¹è±¡æä¾›å˜æ›´åº•åº§ã€‚
- **é£Žé™©**ï¼šç¬¬ä¸€ç‰ˆå®žçŽ°å¯èƒ½è¿‡é‡ï¼›å»ºè®®å…ˆä½œä¸º IA çº¦å®šå’Œå°‘æ•°å¯¹è±¡è¯•ç‚¹ï¼Œä¸è¦æ±‚æ‰€æœ‰ä½Žé£Žé™©å¯¹è±¡éƒ½ claim åŒ–ã€‚

### P1-17ï¼šæ–°å¢žåªè¯» `local_data_warehouse_view` / `exploratory_index_view` ä½œä¸ºå®¡é˜…ä¸Žè°ƒè¯•å±‚

- **å‘çŽ°æ¥æº**ï¼šDogsheep æŠŠ GitHub/Reddit/Twitter/photos ç­‰ä¸ªäººæ•°æ®å¯¼å…¥ SQLiteï¼ŒDatasette æä¾›å¯æµè§ˆ API/UIï¼Œsqlite-utils æ”¯æŒä»Ž JSON/CSV è‡ªåŠ¨å»ºè¡¨ã€FTSã€lookup tableã€‚
- **è¦ç‚¹**ï¼š
  - ä»Ž file-first truth layer å’Œ confirmed/candidate objects ç”Ÿæˆåªè¯» SQLite/FTS/BM25 è§†å›¾ã€‚
  - è§†å›¾å¿…é¡»è®°å½• `built_from_import_run_ids`ã€`schema_version`ã€`generated_at`ã€`field_allowlist`ã€‚
  - è¯¥è§†å›¾æœåŠ¡äºŽäººå·¥å®¡é˜…ã€è°ƒè¯•ã€ä¸´æ—¶åˆ†æžå’Œæ‰¹é‡è´¨é‡æ£€æŸ¥ï¼Œä¸æ˜¯å”¯ä¸€çœŸç›¸ã€‚
- **æ”¶ç›Š**ï¼šæ¯”ç›´æŽ¥æµè§ˆæ–‡ä»¶å¤¹æˆ–ä¸» DB æ›´é€‚åˆå‘çŽ°å¯¼å…¥ç¼ºå£ã€é‡å¤é¡¹ã€OCR å¤±è´¥ã€é‚®ä»¶é™„ä»¶æ¼è§£æžã€ç…§ç‰‡ EXIF å¼‚å¸¸ã€è´¦å•å‘¨æœŸå¼‚å¸¸ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢žå¯é‡å»ºç´¢å¼•/è§†å›¾å±‚ï¼›ä¸Ž retrieval çš„ exact search / FTS / BM25 å…¼å®¹ã€‚
- **é£Žé™©**ï¼šshare/subset è§†å›¾å¯èƒ½æ³„éœ² GPSã€äººè„¸ã€åŒ»ç–—ã€è´¢åŠ¡ã€å…³ç³»å›¾è°±ï¼›å¿…é¡»é»˜è®¤æœ¬åœ°ã€åªè¯»ã€å­—æ®µç™½åå•ã€‚

### P1-18ï¼šä¸ºç¦»çº¿ç¡¬ç›˜/NAS/å†·å½’æ¡£æ–°å¢ž `storage_location_ref` ä¸Ž `availability_state`

- **å‘çŽ°æ¥æº**ï¼šReddit DataHoarder å…³äºŽå¤§åž‹ä¸ªäººå½’æ¡£æ£€ç´¢çš„è®¨è®ºï¼šç”¨æˆ·ç»å¸¸ä¾èµ–ä¸­å¤®ç›®å½•ã€æ–‡ä»¶ hashã€EXIFã€perceptual hashã€ç¡¬ç›˜ç¼–å·/åºåˆ—å·ã€è·¯å¾„ç´¢å¼•æ¥å®šä½ç¦»çº¿æ–‡ä»¶ã€‚
- **è¦ç‚¹**ï¼š
  - `raw_evidence` / `media_asset` å¢žåŠ  `storage_location_ref`ã€‚
  - `storage_location` åŒ…å« `volume_id`ã€`volume_label`ã€`device_serial_hash`ã€`original_path`ã€`normalized_path`ã€`availability_state`ã€`last_seen_at`ã€`last_verified_at`ã€‚
  - `availability_state`: `online | offline_indexed | missing | cold_archive`ã€‚
  - æ£€ç´¢ç»“æžœå¿…é¡»èƒ½è¯´æ˜Žâ€œå¯ç«‹å³æ‰“å¼€ / ç´¢å¼•å¯è§ä½†åŽŸä»¶ç¦»çº¿ / åŽŸä»¶ç¼ºå¤± / éœ€è¦è¿žæŽ¥æŸå—ç›˜â€ã€‚
- **æ”¶ç›Š**ï¼šè®©æ—§ç¡¬ç›˜ã€å®¶åº­åŽ†å²ç…§ç‰‡ã€ç¨ŽåŠ¡å½’æ¡£ã€æ‰«æä»¶ã€NAS å†·æ•°æ®è¿›å…¥åŒä¸€æ£€ç´¢ä½“ç³»ï¼Œè€Œä¸æ˜¯åªèƒ½ä¾èµ–æ¨¡ç³Šè®°å¿†ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– raw evidence çš„ location/provenanceï¼›å½±å“ retrieval UI å’Œ source evidence pullbackã€‚
- **é£Žé™©**ï¼šè·¯å¾„å’Œè®¾å¤‡ä¿¡æ¯æœ¬èº«æ•æ„Ÿï¼›è®¾å¤‡åºåˆ—å·åº” hashï¼Œè·¯å¾„å±•ç¤ºåº”æ”¯æŒ redactionï¼Œç¦»çº¿ç´¢å¼•å¿…é¡»ç”¨ `last_verified_at` é¿å…è¯¯å¯¼ã€‚

## 2026-05-13 14:25 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆlocal archive / index cache / citation gateï¼‰

### P0-13ï¼šæ˜Žç¡® `truth / cache / export` ä¸‰å±‚ï¼Œé˜²æ­¢æ£€ç´¢ç¼“å­˜å˜æˆäº‹å®žæ¥æº

- **å‘çŽ°æ¥æº**ï¼šmsgvault çš„ SQLite system of record + Parquet analytics cache + local vectorsï¼›ArchiveBox çš„æ™®é€šæ–‡ä»¶å¤¹ + SQLite/JSON å…ƒæ•°æ® + å¯ç›´æŽ¥æµè§ˆçš„ snapshot æ–‡ä»¶å¤¹ã€‚
- **è¦ç‚¹**ï¼š
  - `truth layer`ï¼šåŽŸå§‹æ–‡ä»¶ã€sidecarã€confirmed personal memory objectsã€‚
  - `cache layer`ï¼šFTS/BM25ã€OCR cacheã€thumbnailã€analytics parquet/duckdbã€vector embeddingsã€‚
  - `export layer`ï¼šMarkdown/wiki/static HTML/CSV/JSON bundleã€‚
  - cache å¿…é¡»å¯é‡å»ºï¼Œå¹¶å¸¦ `built_from_refs/generated_at/schema_or_model_version`ã€‚
  - export é»˜è®¤å­—æ®µç™½åå•å’Œ redactionï¼Œä¸ç›´æŽ¥æš´éœ²é«˜æ• evidenceã€‚
- **æ”¶ç›Š**ï¼šä»¥åŽå¯ä»¥ä¼˜åŒ–æœç´¢å’Œåˆ†æžè€Œä¸ç ´å file-first/local-first çœŸç›¸å±‚ï¼›ä¹Ÿèƒ½é¿å… vector/Parquet/ç´¢å¼•åº“é”å®šã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢ž `storage_layer: truth | cache | export`ï¼›æ´¾ç”Ÿç´¢å¼•/embedding/cache å¯¹è±¡æ–°å¢ž `built_from_refs`ã€‚
- **é£Žé™©**ï¼šå¤šä¸€å±‚æ¦‚å¿µä¼šå¢žåŠ æ–‡æ¡£å¤æ‚åº¦ï¼›ä¸ªäººç‰ˆåº”åªæŠŠå®ƒä½œä¸ºåŽŸåˆ™å’Œå°‘æ•°å­—æ®µï¼Œä¸è¦åšå®Œæ•´æ•°æ®å¹³å°ã€‚

### P0-14ï¼šé«˜é£Žé™©å€™é€‰æ–°å¢ž `citation_refs / citation_state` å®¡é˜…é—¨

- **å‘çŽ°æ¥æº**ï¼šReddit ä¸Šç”¨ Obsidian ç®¡ç†å¤æ‚åŒ»ç–—è®°å½•çš„è®¨è®ºå¼ºè°ƒ OCRã€LLM è·³è¿‡æºæ–‡ä»¶ã€åŒ»ç–—éšç§å’Œæºæ–‡å¼•ç”¨é—®é¢˜ï¼›GitEHR å¼ºè°ƒåŒ»ç–—è®°å½•çš„å®¡è®¡ä¸Žå¯è¿½æº¯ã€‚
- **è¦ç‚¹**ï¼š
  - åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€è´¦å·å®‰å…¨ã€å…³ç³»ç±»å€™é€‰å¿…é¡»èƒ½å›žåˆ° evidenceã€‚
  - `citation_state`: `none | file_level | page_level | region_level | excerpt_level`ã€‚
  - `citation_refs` è‡³å°‘åŒ…å« `evidence_ref/page_or_message_id/excerpt/extraction_method`ã€‚
  - æ²¡æœ‰ citation çš„é«˜é£Žé™©å€™é€‰åªèƒ½ä¿æŒ `candidate`ï¼Œä¸èƒ½è¿›å…¥ confirmedã€‚
- **æ”¶ç›Š**ï¼šé™ä½Ž LLM/OCR åœ¨é«˜é£Žé™©é¢†åŸŸåˆ¶é€ â€œçœ‹ä¼¼ç¡®å®šäº‹å®žâ€çš„é£Žé™©ï¼›review æ—¶èƒ½å¿«é€Ÿå›žçœ‹åŽŸä»¶ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ‰©å±• `candidate_item` ä¸Ž high-risk domain objectsï¼›ä¸Ž `evidence_refs` ä¸å†²çªï¼Œ`citation_refs` æ˜¯æ›´ç»†ç²’åº¦è¯æ®å®šä½ã€‚
- **é£Žé™©**ï¼šå¼•ç”¨ç²’åº¦è¶Šç»†ç»´æŠ¤æˆæœ¬è¶Šé«˜ï¼›ç¬¬ä¸€ç‰ˆå»ºè®®åªå¼ºåˆ¶ file/page/message_idï¼ŒOCR region ä»¥åŽå†åŠ ã€‚

### P1-19ï¼šæŠŠ `raw_evidence / media_asset` æ–‡ä»¶ç»„ç»‡å‡çº§ä¸ºè½»é‡ `evidence_packet`

- **å‘çŽ°æ¥æº**ï¼šArchiveBox æ¯ä¸ª snapshot ä¿ç•™å¤šç§è¾“å‡ºæ–‡ä»¶å’Œ `index.json`ï¼›msgvault å¯¹é™„ä»¶ content-addressed å­˜å‚¨ï¼›Reddit å¤§åž‹ä¸ªäººå½’æ¡£è®¨è®ºå¼ºè°ƒæ™®é€šç›®å½•ã€hashã€EXIFã€ä¸­å¤®ç´¢å¼•ä»ç„¶æœ€å¯é ã€‚
- **è¦ç‚¹**ï¼š
  - ä¸€ä¸ªé«˜ä»·å€¼ evidence å¯ä»¥ç»„ç»‡ä¸º `original + meta sidecar + extracted text/OCR + preview + optional redacted copy`ã€‚
  - `artifact_role`: `original | sidecar | extracted_text | ocr | preview | redacted | index_record | embedding`ã€‚
  - preview/OCR/redacted éƒ½æ˜¯æ´¾ç”Ÿç‰©ï¼Œæƒé™ä¸å¾—ä½ŽäºŽ originalï¼Œé™¤éžæ˜¾å¼è„±æ•ç¡®è®¤ã€‚
- **æ”¶ç›Š**ï¼šåŽŸä»¶ã€OCRã€é¢„è§ˆå’Œè„±æ•å‰¯æœ¬ä¸ä¼šæ•£è½ï¼›åº”ç”¨ä¸å¯ç”¨æ—¶ï¼Œæ–‡ä»¶å¤¹ä»å¯ç†è§£å’Œè¿ç§»ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šä¸æ›¿æ¢ `raw_evidence/media_asset`ï¼Œåªå¢žåŠ æ–‡ä»¶å¤¹çº¦å®šå’Œ `derived_refs`ã€‚
- **é£Žé™©**ï¼šæ´¾ç”Ÿæ–‡ä»¶å¢žåŠ å­˜å‚¨ä¸Žæ³„éœ²é¢ï¼›éœ€è¦æ¸…æ¥šæ ‡æ³¨ original vs derivedã€‚

### P1-20ï¼šé€šä¿¡å½’æ¡£åŒºåˆ† `source_native labels` ä¸Ž `personal labels`

- **å‘çŽ°æ¥æº**ï¼šmsgvault å¯¹ Gmail/IMAP/MBOX/Apple Mail/èŠå¤©æ¥æºä¿ç•™ sourceã€conversationã€messageã€raw MIMEã€labelsã€attachmentsï¼›æ­¤å‰ Notmuch/afew ç ”ç©¶ä¹Ÿæ”¯æŒ message/thread åˆ†å±‚ã€‚
- **è¦ç‚¹**ï¼š
  - `labels_from_source`ï¼šGmail labelã€IMAP folderã€èŠå¤© app çŠ¶æ€ã€åŽ†å²å¯¼å‡ºæ ‡ç­¾ã€‚
  - `personal_labels`ï¼šä¸ªäººè®°å¿†åº“è¯­ä¹‰æ ‡ç­¾ï¼Œå¦‚ billã€receiptã€security_noticeã€relationshipã€travelã€‚
  - `pipeline_state`ï¼šnew/parsed/classified/reviewed/archived_onlyï¼Œä¸ä¸Žä¸Šè¿°ä¸¤ç±»æ··ç”¨ã€‚
- **æ”¶ç›Š**ï¼šæ—§é‚®ç®±å’Œæ–°é‚®ç®±éƒ½èƒ½å®‰å…¨å¯¼å…¥ï¼›æ¥æºæ ‡ç­¾ä¸ä¼šæ±¡æŸ“ä¸ªäººè¯­ä¹‰åˆ†ç±»ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– email/chat æœ€å°å­—æ®µï¼›å¯æŽ¨å¹¿åˆ° photo albumsã€filesystem foldersã€cloud labelsã€‚
- **é£Žé™©**ï¼šå­—æ®µç•¥å¢žï¼›ä½†æ¯”æŠŠæ‰€æœ‰æ ‡ç­¾å¡žè¿›ä¸€ä¸ª `tags` æ•°ç»„æ›´å¯ç»´æŠ¤ã€‚

## 2026-05-13 15:26 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆcanonical membership / evidence packetsï¼‰

### P0-15ï¼šæ–°å¢ž `source_membership`ï¼ŒæŠŠæ¥æºå®¹å™¨/æ ‡ç­¾/ç›¸å†Œä»Žä¸ªäººè¯­ä¹‰æ ‡ç­¾ä¸­æ‹†å‡º

- **å‘çŽ°æ¥æº**ï¼šBirdclaw çš„ canonical tweets/profiles + account-scoped timeline/collection edgesï¼›Discrawl çš„ channel/thread/message/attachment åˆ†å±‚ä¸Ž Git snapshot å‘å¸ƒç™½åå•ï¼›æ­¤å‰ Notmuch/afew ä¸Ž msgvault å¯¹ source labels å’Œ personal labels çš„åŒºåˆ†ã€‚
- **è¦ç‚¹**ï¼š
  - åŒä¸€ä¸ª canonical object å¯èƒ½å‡ºçŽ°åœ¨å¤šä¸ªæ¥æºå®¹å™¨é‡Œï¼šæ—§é‚®ç®±æ–‡ä»¶å¤¹ã€æ–° Gmail labelã€èŠå¤© threadã€Apple Photos albumã€äº‘ç›˜ç›®å½•ã€ç¤¾äº¤æ”¶è—ã€å¯¼å‡ºæ‰¹æ¬¡ã€‚
  - `source_membership` åªè¡¨è¾¾â€œæ¥æºç³»ç»Ÿå¦‚ä½•ç»„ç»‡å®ƒâ€ï¼Œä¸è¡¨è¾¾ä¸ªäººæ•°æ®åº“çš„é•¿æœŸè¯­ä¹‰ã€‚
  - ä¸ªäººè¯­ä¹‰ç»§ç»­ç”¨ `personal_labels` / `semantic_type` / `domain` è¡¨è¾¾ã€‚
  - æœ€å°å­—æ®µï¼š

```yaml
source_membership:
  id:
  canonical_ref:
  source_category:
  source_account_ref:
  container_ref:
  source_label_or_folder:
  membership_type:
  first_seen_at:
  last_seen_at:
  import_batch_id:
  sensitivity:
  sync_permission:
  publish_policy:
```

- **æ”¶ç›Š**ï¼šé¿å…æ—§é‚®ç®±/æ–°é‚®ç®±/ç›¸å†Œ/æ–‡ä»¶å¤¹/èŠå¤©å¯¼å‡ºæ ‡ç­¾æ±¡æŸ“é•¿æœŸè¯­ä¹‰ï¼›æ”¯æŒåŒä¸€èµ„äº§å¤šæ¥æºå‡ºçŽ°ä½†åªä¿ç•™ä¸€ä¸ª canonical objectï¼›æœªæ¥ Google/Telegram/Hermes sync å¯ä»¥æŒ‰ membership è£å‰ªã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼š`raw_evidence`ã€`media_asset`ã€`email_message`ã€`chat_message`ã€`person_profile`ã€`document_record` éƒ½å¯æŒ‚å¤šä¸ª `source_membership`ï¼›`labels_from_source` å¯é™çº§ä¸º membership çš„å­—æ®µï¼Œè€Œä¸æ˜¯å¯¹è±¡ä¸»æ ‡ç­¾ã€‚
- **é£Žé™©**ï¼šå¤šä¸€å±‚è¾¹å¯¹è±¡ï¼›æ¥æºå®¹å™¨åæœ¬èº«å¯èƒ½æ•æ„Ÿï¼Œé»˜è®¤ç»§æ‰¿ canonical object æœ€é«˜ sensitivityï¼Œå¤–éƒ¨ export é»˜è®¤æŽ’é™¤ `local_only` membershipã€‚

### P0-16ï¼šé«˜ä»·å€¼è¯æ®é‡‡ç”¨ä¸ªäººç‰ˆ `evidence_packet + citation_ref` æœ€å°çº¦å®š

- **å‘çŽ°æ¥æº**ï¼šReddit ä¸Šç”¨ Obsidian/LLM wiki ç®¡ç†å¤æ‚åŒ»ç–—è®°å½•çš„å®žé™…ç—›ç‚¹ï¼ˆOCRã€LLM è·³è¿‡æ–‡ä»¶ã€å›žæºå›°éš¾ã€åŒ»ç–—éšç§ï¼‰ï¼›ArchiveBox snapshot æ–‡ä»¶å¤¹ï¼›SwarmVault raw/wiki/state ä¸‰å±‚ï¼›Discrawl é™„ä»¶äºŒè¿›åˆ¶å¤–ç½®è€Œåªç´¢å¼• metadata/å¯é€‰ extracted textã€‚
- **è¦ç‚¹**ï¼š
  - `evidence_packet` ä¸æ˜¯æ›¿æ¢ `raw_evidence/media_asset`ï¼Œè€Œæ˜¯æŠŠé«˜ä»·å€¼è¯æ®çš„åŽŸä»¶ã€sidecarã€OCR/textã€previewã€redacted copy æ”¾åœ¨ä¸€ä¸ªå¯ç†è§£çš„åŒ…é‡Œã€‚
  - `citation_ref` ä¸åªæŒ‡å‘æ–‡ä»¶ï¼Œè¿˜å¯æŒ‡å‘ packet å†… artifact å’Œ locatorï¼ˆé¡µç ã€message idã€sectionã€OCR regionã€timestampï¼‰ã€‚
  - é«˜é£Žé™© confirmed objectï¼ˆåŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€è´¦å·å®‰å…¨ã€å…³ç³»ï¼‰è‡³å°‘éœ€è¦ file/page/message çº§ citationï¼›æ²¡æœ‰ citation åªèƒ½ä¿æŒ candidateã€‚
  - æœ€å°å­—æ®µï¼š

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

citation_ref:
  evidence_ref:
  artifact_ref:
  locator:
  excerpt:
  extraction_method:
  confidence:
```

- **æ”¶ç›Š**ï¼šreview æ—¶èƒ½å¿«é€Ÿä»Žå€™é€‰äº‹å®žå›žåˆ°åŽŸ PDF/æˆªå›¾/é‚®ä»¶/é™„ä»¶ï¼›åº”ç”¨ä¸å¯ç”¨æ—¶æ–‡ä»¶å¤¹ä»å¯è¿ç§»å’Œç†è§£ï¼›é™ä½Ž OCR/LLM æŠŠé«˜é£Žé™©ä¿¡æ¯è¯´é”™ä½†æ— æ³•è¿½æº¯çš„é£Žé™©ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– P0-14 å’Œ P1-19ï¼›`candidate_item` ä¸Ž high-risk domain objects å¢žåŠ  `citation_refs`ï¼›`raw_evidence/media_asset` å¢žåŠ å¯é€‰ `packet_id` æˆ– `packet_ref`ã€‚
- **é£Žé™©**ï¼šå¯¹æ‰€æœ‰èµ„æ–™å¼ºåˆ¶ packet åŒ–ä¼šè¿‡é‡ï¼›ç¬¬ä¸€ç‰ˆåªå¯¹åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€è´¦å·å®‰å…¨ã€é‡è¦è¡Œæ”¿æ–‡ä»¶å’Œå°‘é‡é«˜ä»·å€¼æˆªå›¾å¼ºåˆ¶ã€‚

### P1-21ï¼šæŠŠ `truth / working / cache / export` é™çº§å†™æˆä¸ªäººç‰ˆå››å±‚è¾¹ç•Œ

- **å‘çŽ°æ¥æº**ï¼šSwarmVault çš„ `raw/ wiki/ state/` ä¸‰å±‚ï¼›Engram çš„ Markdown source of truth + å¯é‡å»º FTS/Xapian indexï¼›Discrawl çš„ SQLite/FTS/embedding provider-model-input_version çº¦æŸã€‚
- **è¦ç‚¹**ï¼š
  - `truth`ï¼šåŽŸå§‹æ–‡ä»¶ã€sidecarã€confirmed personal memory objectsã€‚
  - `working`ï¼šäººå·¥å¯è¯» wiki/brief/summary/doctor visit prepï¼Œä¸æ˜¯çœŸç›¸ï¼Œå¿…é¡»å¸¦ `built_from_refs` å’Œ `review_state`ã€‚
  - `cache`ï¼šOCR cacheã€thumbnailã€FTS/BM25ã€embeddingã€graph viewï¼Œå¯åˆ é™¤é‡å»ºã€‚
  - `export`ï¼šMarkdown/HTML/CSV/JSON bundleï¼Œå¿…é¡»å­—æ®µç™½åå•å’Œ redactionã€‚
  - cache è®°å½• `provider/model/input_version/generated_at`ï¼Œé¿å…ä¸åŒ embedding æˆ–è§£æžç‰ˆæœ¬æ··ç”¨ã€‚
- **æ”¶ç›Š**ï¼šè®©ä¸ªäººç³»ç»Ÿèƒ½åŒæ—¶ä¿ç•™åŽŸä»¶ã€ç”Ÿæˆå¥½è¯»æ•´ç†é¡µã€å¿«é€Ÿæœç´¢ï¼Œå¹¶é¿å…æŠŠç´¢å¼•æˆ– LLM wiki å½“æˆå”¯ä¸€äº‹å®žã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ·±åŒ– P0-13ï¼›æ–°å¢ž `storage_layer`ã€`artifact_role`ã€`built_from_refs`ã€`cache_identity` ç­‰å°‘é‡å­—æ®µã€‚
- **é£Žé™©**ï¼šæ¦‚å¿µå¢žå¤šï¼›åº”ä½œä¸ºç›®å½•/å­—æ®µçº¦å®šï¼Œè€Œä¸æ˜¯ç¬¬ä¸€ç‰ˆå°±å®žçŽ°å®Œæ•´æ•°æ®å¹³å°ã€‚

## 2026-05-13 16:26 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆtimeline projection / temporal uncertaintyï¼‰

### P0-17ï¼šæŠŠæ—¶é—´çº¿å‡çº§ä¸º `timeline_projection + timeline_entry`ï¼Œä½†æ˜Žç¡®å®ƒä¸æ˜¯äº‹å®žä¸»å­˜å‚¨

- **å‘çŽ°æ¥æº**ï¼šTimelinize/Timeliner æŠŠ timelineã€mapã€conversationã€gallery æ˜Žç¡®ä½œä¸ºä¸åŒ projectionsï¼›ActivityWatch çš„ bucket/event/heartbeat æ¨¡åž‹ï¼›facebookresearch personal-timeline / TimelineQA çš„ retrieval-based ä¸Ž view-based QAï¼›Obsidian/Reddit daily note å®žè·µå¯¹ rollupã€Dataviewã€æ£€ç´¢ç¨³å®šæ€§çš„ç»éªŒã€‚
- **è¦ç‚¹**ï¼š
  - `daily_timeline / medical_timeline / finance_timeline / relationship_timeline / map_view / gallery_view` éƒ½åº”æ˜¯ä»Ž raw evidenceã€confirmed objectsã€candidate objectsã€source memberships ç”Ÿæˆçš„æŠ•å½±è§†å›¾ã€‚
  - æ–°å¢ž `timeline_projection`ï¼šè®°å½• projection ç±»åž‹ã€æž„å»ºè§„åˆ™ã€æƒé™èŒƒå›´ã€redaction ç­–ç•¥ã€coverage çŠ¶æ€ã€cache identityã€‚
  - æ–°å¢ž `timeline_entry`ï¼šè®°å½• canonical_refã€source_membership_refsã€temporal_anchorã€display_groupã€domainã€entity_refsã€place_refsã€evidence_refsã€citation_refsã€sensitivityã€sync_permissionã€review_stateã€confidenceã€‚
  - `daily_narrative_log` åªèƒ½æ˜¯ working/export å±‚ï¼Œå¿…é¡»å¸¦ `built_from_projection_id`ï¼Œä¸èƒ½ä½œä¸º evidence æˆ– confirmed factã€‚
- **æ”¶ç›Š**ï¼šç”¨æˆ·å¯ä»¥æŒ‰æ—¥ã€é¢†åŸŸã€äººã€åœ°ç‚¹ã€æ—…è¡Œã€ä¼šè¯ã€å›¾åº“æµè§ˆå…¨ç”Ÿæ´»æ•°æ®ï¼ŒåŒæ—¶ä¸æŠŠ AI æ€»ç»“æˆ–æ—¥è®°è§†å›¾æ±¡æŸ“äº‹å®žå±‚ï¼›ä¹Ÿæ”¯æŒ â€œä¸Šæ¬¡ X æ˜¯ä»€ä¹ˆæ—¶å€™â€â€œæŸæœˆè´¦å•/è¿åŠ¨/å°±è¯Šæœ‰å“ªäº›â€â€œæŸæ¬¡æ—…è¡Œæ¶‰åŠå“ªäº›ç…§ç‰‡/é‚®ä»¶/ç¥¨æ®â€ è¿™ç±»èšåˆæŸ¥è¯¢ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢ž `timeline_projection`ã€`timeline_entry`ï¼›æ·±åŒ– P0-6 `aggregation_level`ã€P0-13/P1-21 truth/cache/working è¾¹ç•Œã€P0-15 source_membershipã€P0-16 citation_refã€‚
- **é£Žé™©**ï¼šæ—¶é—´çº¿èšåˆä¼šæ”¾å¤§éšç§é£Žé™©ï¼›å¿…é¡»æŒ‰ child objects è®¡ç®— `max_sensitivity` ä¸Ž `min_sync_permission`ï¼Œå¹¶æ˜¾ç¤º `coverage_state=complete|partial|unknown`ï¼Œé¿å…ä¸å®Œæ•´å¯¼å…¥è¢«è¯¯è§£ä¸ºå®Œæ•´åŽ†å²ã€‚

### P0-18ï¼šæ–°å¢ž `temporal_anchor`ï¼Œæ˜¾å¼è¡¨è¾¾æ—¶é—´è§’è‰²ã€ç²¾åº¦ã€æ—¶åŒºå’Œä¸ç¡®å®šæ€§

- **å‘çŽ°æ¥æº**ï¼šTimelinize å¯¹ item ä½¿ç”¨ timestamp/timespan/timeframe/time_offset/time_uncertaintyï¼›ActivityWatch äº‹ä»¶æ¨¡åž‹æé†’ continuous stream éœ€è¦ timestamp/durationï¼Œä½†å…¶ UTC-only è¡Œä¸ºä¹Ÿæš´éœ²äº† timezone ä¸¢å¤±é£Žé™©ï¼›TimelineQA å¼ºè°ƒ lifelog QA åŒæ—¶ä¾èµ–è‡ªç”±æ–‡æœ¬ã€æ—¶é—´å’Œåœ°ç‚¹ç»“æž„ã€‚
- **è¦ç‚¹**ï¼š
  - ä¸å†å‡è®¾æ‰€æœ‰å¯¹è±¡åªæœ‰ä¸€ä¸ª `occurred_at`ã€‚åŒä¸€å¯¹è±¡å¯èƒ½æœ‰ `captured_at/sent_at/received_at/issued_at/due_at/paid_at/appointment_at/observed_at/ingested_at/inferred_at`ã€‚
  - æœ€å°å­—æ®µï¼š

```yaml
temporal_anchor:
  primary_time:
  primary_time_role:
  start_time:
  end_time:
  timeframe:
  temporal_precision:
  timezone:
  utc_offset:
  time_uncertainty:
  time_source:
  alternative_times:
```

  - å¯¹ç…§ç‰‡ã€æ—§æ‰«æä»¶ã€åŒ»ç–—æŠ¥å‘Šã€è´¦å•ã€é‚®ä»¶ã€èŠå¤©ã€æœªæ¥ wearable/audio stream éƒ½ä¿ç•™ `time_source` ä¸Ž `temporal_precision`ã€‚
  - ActivityWatch é£Žæ ¼ stream çš„ heartbeat/merge ç»“æžœåº”ä½œä¸º projection/cacheï¼Œä¸è¦†ç›– raw eventã€‚
- **æ”¶ç›Š**ï¼šé•¿æœŸç³»ç»Ÿèƒ½æ­£ç¡®å¤„ç†æ—…è¡Œè·¨æ—¶åŒºã€æ—§ç…§ç‰‡åªçŸ¥å¹´æœˆã€è´¦å• due/paid å·®å¼‚ã€åŒ»ç–— observed/issued/imported å·®å¼‚ã€é‚®ä»¶ sent/received/imported å·®å¼‚ï¼›æ—¶é—´çº¿å’Œæ£€ç´¢æŽ’åºæ›´å¯ä¿¡ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼š`raw_evidence/media_asset/email_message/chat_message/medical_item/finance_item/event/task` å¢žåŠ å¯é€‰ `temporal_anchor`ï¼›`occurred_at` å¯ä¿ç•™ä¸ºä¾¿æ·å­—æ®µï¼Œä½†åº”ç”± `temporal_anchor.primary_time` æ´¾ç”Ÿã€‚
- **é£Žé™©**ï¼šå­—æ®µå¤æ‚åº¦ä¸Šå‡ï¼›ç¬¬ä¸€ç‰ˆå¯åªè¦æ±‚ `primary_time/primary_time_role/temporal_precision/timezone/time_source`ï¼Œå…¶ä½™å­—æ®µæŒ‰éœ€è¡¥å……ã€‚

## 2026-05-13 17:26 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆraw samples vs semantic projectionsï¼‰

### P0-19ï¼šæ–°å¢ž `interpretation_level`ï¼ŒåŒºåˆ†åŽŸå§‹è§‚æµ‹ã€æ¥æºè¯­ä¹‰æŽ¨æ–­ã€æ´¾ç”Ÿå€™é€‰å’ŒæŠ•å½±è§†å›¾

- **å‘çŽ°æ¥æº**ï¼šTimelinize çš„æœ¬åœ°åŽŸå§‹æ•°æ® + timeline/map/conversation/gallery projectionsï¼›Google Takeout Location History çš„ raw `Records.json` vs `Semantic Location History`ï¼ˆ`placeVisit` / `activitySegment`ï¼‰ï¼›DFIR Review å¯¹ Google semantic layer å—ç”¨æˆ·ç¼–è¾‘å½±å“çš„åˆ†æžï¼›Apple Health / HealthKit sample çš„ start/end/source revision æ¨¡å¼ã€‚
- **è¦ç‚¹**ï¼š
  - `review_state` åªè¡¨ç¤ºäººæ˜¯å¦ç¡®è®¤ï¼›`interpretation_level` è¡¨ç¤ºè®°å½•è·ç¦»åŽŸå§‹è§‚æµ‹æœ‰å¤šè¿œã€‚
  - æœ€å°æžšä¸¾ï¼š`raw | source_semantic | derived_candidate | reviewed_fact | projection`ã€‚
  - Google/Apple/å¯ç©¿æˆ´è®¾å¤‡çš„è‡ªåŠ¨ place visitã€activity segmentã€sleep sessionã€weekly trend é»˜è®¤ä¸æ˜¯ truthï¼Œå¿…é¡»æ˜Žç¡®ä¸º `source_semantic` æˆ– `projection`ã€‚
- **æ”¶ç›Š**ï¼šé¿å…æ¥æºç³»ç»Ÿçš„è¯­ä¹‰æŽ¨æ–­æ±¡æŸ“ä¸ªäººäº‹å®žå±‚ï¼›æœªæ¥å¯¼å…¥ä½ç½®ã€å¥åº·ã€wearableã€audio stream æ—¶ï¼Œä¸éœ€è¦é‡æž„ review/retrieval æ¨¡åž‹ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼š`labels` æˆ– sidecar æœ€å°å­—æ®µæ–°å¢žå¯é€‰ `interpretation_level`ï¼›`timeline_entry`ã€`candidate_item`ã€`health_sample`ã€`location_raw_point` å‡å¯ä½¿ç”¨ã€‚
- **é£Žé™©**ï¼šå¢žåŠ ä¸€ä¸ªæ¦‚å¿µï¼›ä½†æ¯”å¼•å…¥å®Œæ•´çš„ source trust ontology è½»å¾—å¤šï¼Œé€‚åˆä¸ªäººç‰ˆã€‚

### P1-22ï¼šä¸ºä½ç½®å’Œå¥åº·è¿žç»­æ•°æ®é¢„ç•™ `raw sample -> semantic candidate -> projection` æœ€å°å¯¹è±¡

- **å‘çŽ°æ¥æº**ï¼šGoogle Semantic Location History schemaï¼ˆ`activitySegment` / `placeVisit`ï¼‰ï¼›Apple Health XML/HealthKit sample çš„ `type/value/unit/startDate/endDate/sourceName/sourceVersion/device` ç¤¾åŒºå¯¼å‡ºç»éªŒï¼›QS Ledger çš„ local quantified-self downloader + analysis dashboard åˆ†å±‚ã€‚
- **è¦ç‚¹**ï¼š
  - ä½ç½®ï¼š`location_raw_point` ä¿ç•™åŽŸå§‹ç‚¹ï¼›`place_visit_candidate` å’Œ `movement_segment_candidate` ä¿ç•™æ¥æºç³»ç»ŸæŽ¨æ–­ï¼›`map_view/travel_timeline/daily_projection` ä½œä¸º projectionã€‚
  - å¥åº·ï¼š`health_sample` ä¿ç•™ sample typeã€valueã€unitã€start/endã€source/deviceã€evidence_refï¼›sleep sessionã€exercise summaryã€weekly trendã€doctor prep summary åªæ˜¯ projection/working layerã€‚
  - ä¸çŽ°åœ¨å®žçŽ° Google/Apple/wearable å¯¼å…¥ï¼ŒåªæŠŠ IA è¾¹ç•Œå†™æ¸…æ¥šã€‚
- **æ”¶ç›Š**ï¼šæ”¯æŒæœªæ¥ lifelog/wearable/audio streamsï¼ŒåŒæ—¶ä¿æŒçŽ°åœ¨çš„ä¸ªäººç‰ˆè½»é‡ä¸»å¹²ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæœªæ¥å¯æ–°å¢ž `location_raw_point/place_visit_candidate/movement_segment_candidate/health_sample`ï¼›çŽ°é˜¶æ®µåªåœ¨æ–‡æ¡£ä¸­ä½œ P1 é¢„ç•™ã€‚
- **é£Žé™©**ï¼šGPSã€home/work patternã€sleepã€heart rateã€symptom ç­‰éƒ½æ˜¯é«˜æ•æ„Ÿï¼›é»˜è®¤ `local_only`ã€ä¸ embed rawã€ä¸å¯¼å‡ºç²¾ç¡®è½¨è¿¹ã€‚

## 2026-05-13 17:49 EDT æ–°å¢žå€™é€‰é¡¹ï¼ˆPS æ€»ç®¡ä¸²è¡Œ agent work logï¼‰

### P0-20ï¼šæ–°å¢ž `ps_agent_work_log` + `domain_agent_queue`ï¼Œå¼ºåˆ¶å°ç§˜ä¸²è¡Œ processing/audit/proposal chain

- **å‘çŽ°æ¥æº**ï¼šæœ¬è½®å¤æ ¸ `06-global-workflow.md`ã€`07-personal-memory-minimal-workflow.md`ã€æ—¢æœ‰ P1-11 `assistant_handoff/context_event_log` ä¸Žæœ€è¿‘ agent workflow è®¨è®ºã€‚çŽ°æœ‰ç»“æž„å·²æœ‰ handoffã€review gateã€candidate verificationï¼Œä½†è¿˜ç¼ºå°‘æ€»ç®¡å±‚é¢çš„â€œå…ˆè®°å½•ç»“æžœã€å†å…è®¸ä¸‹ä¸€æ£’â€çš„ä¸²è¡Œé—¨é—©ã€‚
- **è¦ç‚¹**ï¼š
  - æ€»ç®¡æ˜¯å”¯ä¸€å…¨å±€ work log ownerï¼Œè´Ÿè´£åˆ†ç±»ã€åˆ†æ´¾ã€è®°å½•ç»“æžœã€å†²çª/é˜»å¡žã€ä¸‹ä¸€æ­¥æŽ’é˜Ÿã€‚
  - æ¯ä¸ªå°ç§˜åªç»´æŠ¤ä¸€ä¸ª `active_chain_id`ï¼›åŒä¸€æ—¶é—´åªèƒ½æœ‰ä¸€æ¡ active processing/audit/proposal chainã€‚
  - processing agent åªå¤„ç†ä¸€ä¸ª evidence packetï¼Œè¿”å›ž `processing_result` æˆ– `abstract_result`ã€‚
  - audit agent æ£€æŸ¥ processing resultã€citation_refsã€scope boundary å’Œ risk flagsï¼Œè¿”å›ž `audit_result`ã€‚
  - proposal agent æ ¹æ® processing/audit ç»“æžœç”Ÿæˆ `review_result` / `update_proposal` / `no_action`ï¼Œä½†ä¸ç›´æŽ¥å†™ truth layerã€‚
  - å°ç§˜æ±‡æ€»ç”Ÿæˆ `domain_event_summary_report`ï¼Œå¹¶ report ç»™æ€»ç®¡ã€‚
  - åªæœ‰æ€»ç®¡æŠŠè¯¥ work log çŠ¶æ€æŽ¨è¿›åˆ° `secretary_reported | closed`ï¼Œå¹¶è®¾ç½® `next_spawn_allowed=true` åŽï¼Œå°ç§˜æ‰èƒ½å¼€å§‹ä¸‹ä¸€æ¡ chainã€‚
  - å¤±è´¥ã€è¯æ®ä¸è¶³ã€å†²çªã€è¶…èŒƒå›´éƒ½å¿…é¡»å†™ `blocked_reason`ï¼Œä¸èƒ½é™é»˜ç»§ç»­ã€‚
- **æœ€å°å­—æ®µ**ï¼š

```yaml
ps_agent_work_log:
  log_id:
  created_at:
  owner: ps_orchestrator
  secretary_agent:
  work_item_ref:
  object_refs:
  evidence_packet_refs:
  current_status: queued | assigned | processing_running | processing_returned | audit_running | audit_returned | proposal_running | secretary_reported | closed | blocked
  active_chain_id:
  next_spawn_allowed:
  processing_result_ref:
  audit_result_ref:
  proposal_ref:
  baton_ref:
  domain_event_summary_report_ref:
  recommended_next_step:
  risk_level:
  sensitivity:

domain_agent_queue:
  secretary_agent:
  active_chain_id:
  active_work_log_id:
  queued_work_item_refs:
  blocked_reason:
  next_spawn_allowed:
```

- **æ”¶ç›Š**ï¼šä¿è¯â€œä¸ºä»€ä¹ˆè¿™æ¡è®°å¿†è¢«å†™å…¥/æ›´æ–°â€å¯è§£é‡Šï¼›é¿å…å°ç§˜å¹¶å‘ spawn å¯¼è‡´é‡å¤å€™é€‰ã€citation ä¸¢å¤±ã€å†²çªè¢«è¦†ç›–ï¼›åŒæ—¶ä¿æŒä¸ªäººç‰ˆè½»é‡ï¼Œä¸å¼•å…¥ä¼ä¸šçº§ä»»åŠ¡å¹³å°ã€‚
- **schema å½±å“ï¼ˆææ¡ˆçº§ï¼‰**ï¼šæ–°å¢ž `ps_agent_work_log` ä¸Ž `domain_agent_queue`ï¼›åŠ æ·± P1-11 `assistant_handoff`ï¼Œä½†ä¸ä¿å­˜ one-shot é•¿ä¸Šä¸‹æ–‡ï¼Œä¸æ”¹å˜ truth layerã€‚
- **é£Žé™©**ï¼šwork log å¯èƒ½åŒ…å«æ•æ„Ÿè·¯å¾„ã€å¯¹è±¡ã€å…³ç³»æˆ–åŒ»ç–—/è´¢åŠ¡ä¸Šä¸‹æ–‡ï¼›å¿…é¡»ç»§æ‰¿æœ€é«˜ sensitivityï¼Œé»˜è®¤ `local_only`ï¼Œå¤–éƒ¨ export é»˜è®¤æŽ’é™¤ã€‚

### P1-23ï¼šç»Ÿä¸€ `processing_result / audit_result / proposal_result` æœ€å°è¾“å‡º schema

- **è¦ç‚¹**ï¼šçŸ­ç”Ÿå‘½å‘¨æœŸ agent åªèƒ½è¿”å›žç»“æž„åŒ–ä¸­é—´ç»“æžœï¼Œä¸ç›´æŽ¥å†™ confirmed memory æˆ– truth layerã€‚

```yaml
processing_result:
  processing_run_id:
  work_log_id:
  evidence_packet_ref:
  output_type: extracted_candidate | object_brief | update_check | no_signal
  structured_output_ref:
  citation_refs:
  confidence:
  processor_baton:
    what_was_checked:
    open_questions:
    stop_reason:
  recommended_next_step:

audit_result:
  audit_run_id:
  work_log_id:
  processing_run_id:
  checked_citation_refs:
  evidence_sufficient:
  citation_valid:
  contradiction_found:
  scope_violation:
  audit_decision: pass | retry | human_review | reject
  risk_flags:

proposal_result:
  proposal_run_id:
  work_log_id:
  processing_result_ref:
  audit_result_ref:
  final_output_type: review_result | update_proposal | no_action
  final_output_ref:
  recommended_next_step:
```

- **æ”¶ç›Š**ï¼šå°ç§˜å¯ä»¥ç”¨å›ºå®šæ–¹å¼ä¸²æŽ¥å¤„ç†ã€å®¡è®¡ã€ææ¡ˆï¼›æ€»ç®¡å¯ä»¥ç”¨ `domain_event_summary_report` å›ºå®šå­—æ®µæŽ’ä¸‹ä¸€æ­¥ã€‚
- **é£Žé™©**ï¼šå­—æ®µè¿‡å¤šä¼šå˜æˆä¼ä¸šçº§ runner schemaï¼›ç¬¬ä¸€ç‰ˆåªæŠŠå®ƒä½œä¸ºæ–‡æ¡£çº¦å®šï¼Œä¸å®žçŽ°è¿è¡Œå™¨ã€‚

