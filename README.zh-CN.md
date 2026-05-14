# Echo Personal Assistant / 个人记忆库

ä¸€ä¸ª local-first çš„ä¸ªäººè®°å¿†åº“å®žéªŒé¡¹ç›®ã€‚å½“å‰é‡ç‚¹ä¸æ˜¯ä¸Šäº‘ï¼Œä¹Ÿä¸æ˜¯å¤æ‚å¤š agent å¹³å°ï¼Œè€Œæ˜¯å…ˆæŠŠä¸ªäººèµ„æ–™å¤„ç†çš„æœ€å°é—­çŽ¯è·‘é€šï¼š

```text
evidence -> sidecar -> candidate -> audit -> proposal -> review -> work log
```

å½“å‰ä»“åº“åŒ…å«ä¸¤ç±»å†…å®¹ï¼š

- è®¾è®¡æ–‡æ¡£ï¼š`information-processing/` å’Œ `docs/`
- å¯è¿è¡Œ dry runï¼š`runtime/`

æ‰€æœ‰ç¤ºä¾‹æ•°æ®éƒ½æ˜¯ fake dataã€‚ä¸è¦æŠŠçœŸå®žåŒ»ç–—ã€è´¢åŠ¡ã€è´¦å·å®‰å…¨ã€å…³ç³»ã€è¯ä»¶æˆ–ç§äººæ–‡ä»¶æäº¤åˆ°è¿™ä¸ªä»“åº“ã€‚

## å¿«é€Ÿå¼€å§‹

Clone åŽè¿›å…¥ä»“åº“æ ¹ç›®å½•ï¼š

```powershell
git clone https://github.com/kidzkw/personal_assistant.git
cd personal_assistant
```

è¿è¡Œå½“å‰ dry runï¼š

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

é¢„æœŸè¾“å‡ºï¼š

```text
DRY_RUN_OK
```

è¿™è¯´æ˜Žå½“å‰ fake packet çš„å¼•ç”¨é“¾æ˜¯å®Œæ•´çš„ï¼š

- evidence packet èƒ½æ‰¾åˆ°åŽŸå§‹ fake evidence
- candidate ä¿æŒåœ¨ reviewable çŠ¶æ€
- processing result æŒ‡å‘ candidate
- audit result å¯¹ financial ç±»åž‹è¦æ±‚ human review
- proposal result æ²¡æœ‰ç›´æŽ¥å†™ confirmed truth
- `ps_agent_work_log.next_spawn_allowed=false`ï¼Œç›´åˆ° review å®Œæˆ

## å¦‚ä½•ä½¿ç”¨å½“å‰ Runtime

å½“å‰ runtime è¿˜ä¸æ˜¯å®Œæ•´åº”ç”¨ï¼Œè€Œæ˜¯ä¸€ä¸ªæ–‡ä»¶å¼ dry-run scaffoldã€‚å®ƒç”¨çº¯æ–‡æœ¬å’Œ JSON æ¨¡æ‹Ÿç¬¬ä¸€æ¡ä¸ªäººè®°å¿†å¤„ç†é“¾è·¯ã€‚

ä¸»è¦å…¥å£ï¼š

```text
runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
runtime/truth/sidecars/ep_fake_bill_001.meta.json
runtime/working/review_queue/candidate_bill_fake_001.json
runtime/working/agent_work_log/pswl_fake_finance_001.json
runtime/scripts/validate-dry-run.ps1
```

è¯»é“¾è·¯æ—¶æŒ‰è¿™ä¸ªé¡ºåºçœ‹ï¼š

```text
1. raw evidence
   runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt

2. evidence packet sidecar
   runtime/truth/sidecars/ep_fake_bill_001.meta.json

3. reviewable candidate
   runtime/working/review_queue/candidate_bill_fake_001.json

4. processing result
   runtime/working/agent_work_log/processing_result_fake_001.json

5. audit result
   runtime/working/agent_work_log/audit_result_fake_001.json

6. proposal result
   runtime/working/agent_work_log/proposal_result_fake_001.json

7. domain event summary report
   runtime/working/domain_reports/domain_event_summary_report_fake_001.json

8. PS work log
   runtime/working/agent_work_log/pswl_fake_finance_001.json
```

ç›®å‰æ–°å¢ž fake packet çš„æ–¹å¼æ˜¯æ‰‹åŠ¨å¤åˆ¶è¿™äº› JSON å½¢çŠ¶ã€‚ä¸‹ä¸€æ­¥ä¼šåš CLIï¼ŒæŠŠè¿™ä¸ªè¿‡ç¨‹å˜æˆå‘½ä»¤ã€‚

## Agent Chain

å½“å‰ agent flow æ˜¯ä¸²è¡Œçš„ï¼Œä¸å…è®¸çŸ­ç”Ÿå‘½å‘¨æœŸ agent è‡ªå·±ä¹±è·‘ã€‚

```text
æ€»ç®¡ / orchestrator
  -> åˆ†æ´¾ work item ç»™å°ç§˜

å°ç§˜ / secretary_agent
  -> å¯åŠ¨ä¸€æ¡ active processing/audit/proposal chain

processing_agent
  -> åªå¤„ç†ä¸€ä¸ªå° evidence packet
  -> è¾“å‡º processing_result

audit_agent
  -> æ£€æŸ¥ processing_resultã€citationã€scope boundaryã€risk flags
  -> è¾“å‡º audit_result

proposal_agent
  -> æ ¹æ® processing_result + audit_result ç”Ÿæˆ
     review_result / update_proposal / no_action
  -> è¾“å‡º proposal_result

å°ç§˜ / secretary_agent
  -> ç”Ÿæˆ domain_event_summary_report
  -> report ç»™æ€»ç®¡

æ€»ç®¡ / orchestrator
  -> æ›´æ–° ps_agent_work_log
  -> å†³å®š next_spawn_allowed
```

é‡è¦è¾¹ç•Œï¼š

- `processing_agent` ä¸å†™ truth layer
- `audit_agent` ä¸åšæœ€ç»ˆä¸šåŠ¡åˆ¤æ–­
- `proposal_agent` ä¸ç›´æŽ¥å†™ confirmed memory
- å°ç§˜è´Ÿè´£é¢†åŸŸæ±‡æ€»
- æ€»ç®¡è´Ÿè´£å…¨å±€ work log å’Œä¸‹ä¸€æ­¥è§£é”
- åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹ã€è´¦å·å®‰å…¨ã€å…³ç³»ä¿¡æ¯é»˜è®¤ `local_only` + `review_required`

## ä»“åº“ç»“æž„

```text
docs/
  Echo ä¿¡æ¯å¤„ç†åˆ†æžå’Œå¤–éƒ¨ç³»ç»Ÿå‚è€ƒ

information-processing/
  ä¸ªäººè®°å¿†åº“ workflowã€candidate proposalsã€research notes

runtime/
  å½“å‰å¯è¿è¡Œ dry-run scaffold
```

Runtime ç›®å½•ï¼š

```text
runtime/
  truth/
    raw_evidence/        # åŽŸå§‹è¯æ®æˆ– fake evidence
    sidecars/            # evidence packet / metadata
    confirmed_objects/   # æœªæ¥ confirmed memory objects
  working/
    review_queue/        # candidates waiting for review
    agent_work_log/      # processing/audit/proposal/work log
    domain_reports/      # å°ç§˜ç»™æ€»ç®¡çš„ summary report
  cache/
    ocr/                 # å¯é‡å»º OCR cache
    fts/                 # å¯é‡å»º search cache
  export/                # æœªæ¥å¯¼å‡ºå±‚
  scripts/               # local commands
```

## å½“å‰å‘½ä»¤

éªŒè¯ dry runï¼š

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

æ£€æŸ¥ä»“åº“çŠ¶æ€ï¼š

```powershell
git status -sb
```

å½“å‰ä¸éœ€è¦å®‰è£…æ­¥éª¤ã€‚

## å½“å‰çŠ¶æ€

å·²å®Œæˆï¼š

- æ–‡æ¡£éª¨æž¶
- local runtime æ–‡ä»¶å¤¹ç»“æž„
- fake financial evidence packet
- evidence packet sidecar
- candidate item
- processing / audit / proposal result ç¤ºä¾‹
- domain event summary report
- PS agent work log ç¤ºä¾‹
- dry-run validation script

æœªå®Œæˆï¼š

- çœŸå®ž inbox ingestion
- åˆ›å»º packet çš„ CLI
- SQLite index
- OCR
- web UI
- çœŸå®ž agent runner
- Gmailã€Google Calendarã€Telegramã€Hermes æˆ– cloud storage åŒæ­¥
- Docker Compose

## è·¯çº¿å›¾

### Phase 0: Static Dry Run

çŠ¶æ€ï¼šå½“å‰é˜¶æ®µã€‚

ç›®æ ‡ï¼šåªç”¨ fake dataï¼Œè®©è®°å¿†å¤„ç† workflow å¯ä»¥è¢«æ£€æŸ¥ã€‚

é‡Œç¨‹ç¢‘ï¼š

- ä¿æŒ fake evidence packet chain æœ‰æ•ˆ
- ä¿æŒ `validate-dry-run.ps1` é€šè¿‡
- åœ¨ schema è¿˜ä¾¿å®œçš„æ—¶å€™ç»§ç»­è°ƒæ•´ JSON å½¢çŠ¶

### Phase 1: Tiny CLI

ç›®æ ‡ï¼šåœæ­¢æ‰‹å†™æ¯ä¸ª fake packetã€‚

è®¡åˆ’å‘½ä»¤ï¼š

```powershell
personal-db new-fake-packet --type bill
personal-db validate
personal-db show-work-log
personal-db list-review-queue
```

ç¬¬ä¸€ç‰ˆå¯ä»¥ç”¨ PowerShell æˆ– Pythonã€‚å®ƒä»ç„¶åº”è¯¥å†™ plain filesï¼Œä¸è¦ä¸€ä¸Šæ¥å˜æˆ database-first systemã€‚

### Phase 2: SQLite Index

ç›®æ ‡ï¼šè®© lookup å’Œ review queue navigation æ›´è½»æ¾ï¼Œä½†ä¸è®© SQLite å˜æˆ truth layerã€‚

SQLite åº”è¯¥ç´¢å¼•ï¼š

- evidence packets
- candidates
- processing / audit / proposal results
- PS work logs
- review queue status

Truth ä»ç„¶æ˜¯æ–‡ä»¶å±‚ã€‚

### Phase 3: Review Queue

ç›®æ ‡ï¼šè®© human review å¯æ“ä½œã€‚

éœ€è¦æ”¯æŒï¼š

- åˆ—å‡º candidates
- æ˜¾ç¤º citation refs
- approve / correct / reject / archive
- ä¿æŒ review result å¯è¿½æº¯
- ä¸è‡ªåŠ¨ç¡®è®¤é«˜é£Žé™©é¢†åŸŸ

### Phase 4: Real Ingestion

ç›®æ ‡ï¼šfake flow ç¨³å®šåˆ°æ— èŠä¹‹åŽï¼Œå†å¯¼å…¥å—æŽ§æœ¬åœ°æ–‡ä»¶ã€‚

å¯èƒ½çš„ç¬¬ä¸€æ‰¹ ingesterï¼š

- local text file
- local PDF metadata-only packet
- screenshot / image metadata packet
- email export packet

ä»ç„¶ä¸åšè‡ªåŠ¨åŒ»ç–—ã€è´¢åŠ¡ã€æ³•å¾‹æˆ–è´¦å·å®‰å…¨å†³ç­–ã€‚

### Phase 5: Local App Or Backend

ç›®æ ‡ï¼šæ–‡ä»¶ workflow ç¨³å®šåŽï¼Œå†åŠ ä¸€ä¸ªå°åž‹ local UI æˆ– APIã€‚

å¯èƒ½æŠ€æœ¯æ ˆï¼š

- Python FastAPI
- Next.js local dashboard
- SQLite + FTS5
- local filesystem storage

### Phase 6: Docker Compose

ç›®æ ‡ï¼šåªæœ‰å½“é¡¹ç›®çœŸçš„æœ‰å€¼å¾—æ‰“åŒ…çš„ä¾èµ–æ—¶ï¼Œå†åš Dockerã€‚

Docker åœ¨è¿™äº›ä¸œè¥¿å‡ºçŽ°åŽä¼šæœ‰ä»·å€¼ï¼š

- backend service
- worker process
- OCR dependency
- local search service
- repeatable development environment

åœ¨é‚£ä¹‹å‰ï¼ŒDocker ä¸»è¦åªæ˜¯æŠŠç®€å•æ–‡ä»¶è¡Œä¸ºè—è¿› container volume æƒé™é‡Œã€‚

## å®‰å…¨è§„åˆ™

ä¸è¦æäº¤çœŸå®žä¸ªäººæ•°æ®ã€‚

ç»å¯¹ä¸è¦ commitï¼š

- medical records
- financial statements
- legal documents
- credentials
- account-security notices
- private relationship notes
- identity documents
- real email exports
- real chat exports
- real photos with GPS/person metadata

æŽ¨èæŠŠæœªæ¥çœŸå®žæœ¬åœ°å®žéªŒæ”¾åœ¨è¿™äº›å·²è¢« git ignore çš„ç›®å½•ï¼š

```text
runtime/local/
runtime/private/
runtime/inbox/
```

è¿™äº›ç›®å½•å¯ä»¥ä»¥åŽç”¨äºŽçœŸå®žæœ¬åœ°å®žéªŒï¼Œä½†ä¸è¦è¿›å…¥ GitHubã€‚


