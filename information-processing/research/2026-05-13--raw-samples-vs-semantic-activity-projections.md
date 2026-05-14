# 2026-05-13 17:26 EDT - Raw samples vs semantic activity projections

æœ¬è½®é—®é¢˜ï¼šä¸Šä¸€è½®å·²ç»æŠŠ `timeline_projection` å’Œ `temporal_anchor` çº³å…¥ P0ï¼Œä½†è¿˜éœ€è¦ç»§ç»­ç¡®è®¤ä½ç½®åŽ†å²ã€Apple Health / wearableã€æœªæ¥ audio stream è¿™ç±»è¿žç»­æ•°æ®åº”è¯¥æ€Žæ ·è¿›å…¥ä¸ªäººè®°å¿†åº“ï¼Œé¿å…æŠŠ Google/Apple/è®¾å¤‡åŽ‚å•†çš„è¯­ä¹‰æŽ¨æ–­ç›´æŽ¥å½“æˆäº‹å®žã€‚

## è¯»å–çš„æœ¬åœ°ä¸Šä¸‹æ–‡

- `information-processing/README.md`
- `information-processing/06-global-workflow.md`
- `information-processing/07-personal-memory-minimal-workflow.md`
- `information-processing/research/candidate-proposals.md`
- `docs/echo-information-processing-design.md`

å½“å‰æ–¹å‘ä»ç„¶æˆç«‹ï¼šlocal-firstã€file-first inboxã€åŽŸå§‹è¯æ®ä¿ç•™ã€AI/OCR/æ¥æºç³»ç»ŸæŽ¨æ–­å…ˆåš candidate/projectionï¼Œé‡è¦äº‹å®žéœ€è¦ evidence pullbackã€‚

## å¤–éƒ¨æ¥æº

1. Timelinize
   - GitHub: https://github.com/timelinize/timelinize
   - Go package docs: https://pkg.go.dev/github.com/timelinize/timelinize/timeline
   - å‘çŽ°ï¼šTimelinize æŠŠå¯¼å…¥æ•°æ®æ”¾åœ¨æœ¬åœ°æ–‡ä»¶å¤¹å’Œ SQLite ä¸­ï¼Œå¹¶é€šè¿‡ timeline / map / conversation / gallery ç­‰ projection ç»„ç»‡æµè§ˆï¼›å…¶æ¨¡åž‹æ”¯æŒ timestampã€timespanã€timeframeã€time_offsetã€time_uncertaintyï¼Œå¹¶ä¸”å¼ºè°ƒåŽŸå§‹ source data ä»è¦ä¿ç•™ã€‚
   - æ„ä¹‰ï¼šç»§ç»­æ”¯æŒä¸Šä¸€è½®åˆ¤æ–­ï¼Œtimeline/map/gallery ä¸èƒ½æˆä¸º truthï¼Œåªèƒ½æ˜¯ä»ŽåŽŸå§‹ itemã€entityã€locationã€conversation ç”Ÿæˆçš„è§†å›¾ã€‚

2. Google Takeout Location History / Semantic Location History
   - schema reference: https://locationhistoryformat.com/reference/semantic/
   - general structure: https://locationhistoryformat.com/guides/general-structure/
   - DFIR Review: https://dfir.pubpub.org/pub/d39u7lg1
   - Reddit: https://www.reddit.com/r/GoogleMaps/comments/1g6gx3v/the_semantic_location_history_from_google_takeout/
   - å‘çŽ°ï¼šGoogle Takeout é€šå¸¸åŒæ—¶æœ‰ raw `Records.json` å’Œè¾ƒé«˜å±‚çš„ `Semantic Location History`ï¼›è¯­ä¹‰å±‚ç”± `activitySegment` ä¸Ž `placeVisit` ç»„æˆï¼ŒæŒ‰æœˆ JSON å­˜æ”¾ã€‚DFIR åˆ†æžæ˜¾ç¤ºï¼Œç”¨æˆ·ç¼–è¾‘ä¼šå½±å“ Semantic Location Historyï¼Œè€Œ raw location data å¯ä»¥ä¿æŒä¸åŒæ€§è´¨çš„åŽŸå§‹è¯æ®ã€‚Reddit è®¨è®ºä¹Ÿæé†’æ—§ç‰ˆ Takeout çš„ semantic export å¯èƒ½æ¯”è¿ç§»åŽçš„è®¾å¤‡ç«¯å¯¼å‡ºæ›´å®Œæ•´ã€‚
   - æ„ä¹‰ï¼šä¸ªäººæ•°æ®åº“ä¸åº”æŠŠ `placeVisit` / `activitySegment` ç›´æŽ¥ç¡®è®¤æˆâ€œæˆ‘ç¡®å®žåŽ»äº†å“ªé‡Œ/åšäº†ä»€ä¹ˆâ€ã€‚å®ƒä»¬åº”å¸¦ `source_interpretation_level=source_semantic`ã€`confidence`ã€`time_source`ã€`location_source`ï¼Œå¹¶å¯ä»Ž raw records å›žæ‹‰ã€‚

3. Apple Health / HealthKit
   - Apple `HKSample.startDate`: https://developer.apple.com/documentation/healthkit/hksample/startdate
   - Apple `HKSourceRevision`: https://developer.apple.com/documentation/healthkit/hksourcerevision
   - Reddit export examples: https://www.reddit.com/r/AppleWatch/comments/1irkloq and https://www.reddit.com/r/AppleWatch/comments/1goka7n
   - å‘çŽ°ï¼šHealthKit sample æœ‰ start/end windowï¼›source revision/source/device å¯¹ provenance å¾ˆå…³é”®ã€‚Apple Health XML export åœ¨ç¤¾åŒºåé¦ˆé‡Œå¸¸è§é—®é¢˜æ˜¯ä½“é‡å¤§ã€éš¾å¤„ç†ã€å­—æ®µä¼šéšç±»åž‹å˜åŒ–ï¼Œç—‡çŠ¶ç­‰ç±»åˆ«å¯èƒ½ä¸¢å¤±ç»†èŠ‚ã€‚
   - æ„ä¹‰ï¼šæœªæ¥å¥åº·/wearable å¯¼å…¥çš„æœ€å°å¯¹è±¡ä¸åº”ä¸€å¼€å§‹å°±æ˜¯ `medical_record`ï¼Œè€Œåº”å…ˆæ˜¯ `health_sample` / `health_interval`ï¼šä¿ç•™ typeã€unitã€valueã€start/endã€source/deviceã€creation/import timeã€raw record refã€‚æ—¥/å‘¨ç»Ÿè®¡ã€ç¡çœ æ®µæ±‡æ€»ã€è¿åŠ¨è¶‹åŠ¿æ˜¯ cache/projectionã€‚

4. Fasten Health
   - GitHub: https://github.com/fastenhealth/fasten-onprem
   - Fasten docs / Connect event shape: https://docs.connect.fastenhealth.com/webhooks/events
   - Reddit: https://www.reddit.com/r/selfhosted/comments/12pcna3
   - å‘çŽ°ï¼šFasten OnPrem å®šä½ä¸º self-hosted personal/family health record viewerï¼Œå¼€æºç‰ˆå½“å‰å¼ºè°ƒæ‰‹åŠ¨å½•å…¥æˆ–å¯¼å…¥ FHIR bundleï¼›Connect ä¸€ä¾§å¯æŠŠåŒ»ç–—è®°å½•ä»¥ NDJSON/FHIR resource æ‰¹é‡è¾“å‡ºã€‚
   - æ„ä¹‰ï¼šåŒ»ç–—è®°å½•ä»åº”ä¿æŒâ€œæ–‡æ¡£è¯æ® + ç®€åŒ–å¯¹è±¡ + citationâ€çš„ä¸ªäººç‰ˆåšæ³•ï¼›FHIR resource åç§°å¯ä½œä¸ºå­—æ®µå‘½åå‚è€ƒï¼Œä½†ä¸åº”æŠŠæ‰€æœ‰å¥åº·/wearable samples éƒ½å‡çº§ä¸ºå®Œæ•´åŒ»ç–—è®°å½•ã€‚

5. QS Ledger
   - GitHub: https://github.com/markwk/qs_ledger
   - å‘çŽ°ï¼šä¸ªäºº quantified-self é¡¹ç›®å¸¸è§ç›®æ ‡æ˜¯ä¸‹è½½å„æœåŠ¡æ•°æ®ã€å­˜æœ¬åœ°ã€å†åšåˆ†æž/ä»ªè¡¨ç›˜ï¼›raw download ä¸Ž analysis output æ˜¯ä¸¤å±‚ã€‚
   - æ„ä¹‰ï¼šä¸ªäººè®°å¿†åº“é‡Œï¼Œè¿žç»­å¥åº·/ä½ç½®/æ´»åŠ¨æµçš„ç¬¬ä¸€ä»·å€¼æ˜¯â€œå¯ä¿ç•™ã€å¯æ£€ç´¢ã€å¯å›žæº¯â€ï¼Œåˆ†æžçœ‹æ¿æ˜¯å¯é‡å»ºè¾“å‡ºã€‚

## ç»“æž„æ€§å‘çŽ°

### 1. è¿žç»­æ•°æ®éœ€è¦åŒºåˆ† raw sample ä¸Ž source semantic object

ä½ç½®ã€å¥åº·ã€æ´»åŠ¨ã€æœªæ¥éŸ³é¢‘/å¯ç©¿æˆ´æµéƒ½ä¸åº”ç›´æŽ¥è¿›å…¥ `memory` æˆ– `medical_record`ã€‚æ›´ç¨³çš„ä¸ªäººç‰ˆåˆ†å±‚ï¼š

```text
raw_sample / raw_record
 -> source_semantic_object
 -> derived_projection
 -> reviewed memory / task / medical / finance object
```

å»ºè®®æ–°å¢žä¸€ä¸ªè½»é‡æ ‡ç­¾ï¼š

```yaml
interpretation_level: raw | source_semantic | derived_candidate | reviewed_fact | projection
```

å®ƒå’Œ `review_state` ä¸é‡å¤ï¼š`review_state` è¡¨ç¤ºäººæ˜¯å¦ç¡®è®¤ï¼›`interpretation_level` è¡¨ç¤ºè¿™æ¡è®°å½•æœ¬èº«ç¦»åŽŸå§‹è§‚æµ‹æœ‰å¤šè¿œã€‚

### 2. ä½ç½®åŽ†å²çš„æœ€å°ä¸ªäººç‰ˆå¯¹è±¡

å½“å‰ä¸å»ºè®®å®žçŽ° Google sync æˆ–åœ°å›¾åŠŸèƒ½ï¼Œåªå»ºè®®æŠŠæœªæ¥å…¼å®¹å¯¹è±¡å†™æ¸…ï¼š

```yaml
location_raw_point:
  source_ref:
  latitude:
  longitude:
  accuracy:
  captured_at:
  device_ref:
  evidence_ref:
  interpretation_level: raw

place_visit_candidate:
  place_label:
  start_time:
  end_time:
  source_confidence:
  built_from_refs:
  interpretation_level: source_semantic
  review_state: candidate

movement_segment_candidate:
  start_time:
  end_time:
  activity_type:
  start_location_ref:
  end_location_ref:
  source_confidence:
  built_from_refs:
  interpretation_level: source_semantic
```

è¿™äº›å¯¹è±¡åªæœåŠ¡äºŽ `travel_timeline`ã€`map_view`ã€`daily_projection` å’Œâ€œæˆ‘é‚£å¤©å¤§æ¦‚åœ¨å“ªé‡Œâ€è¿™ç±»æ£€ç´¢ã€‚é™¤éžç”¨æˆ·æ˜Žç¡®ç¡®è®¤ï¼Œä¸åº”è‡ªåŠ¨ç”Ÿæˆâ€œæˆ‘åŽ»äº† Xâ€çš„é•¿æœŸè®°å¿†ã€‚

### 3. å¥åº·/wearable æ ·æœ¬çš„æœ€å°ä¸ªäººç‰ˆå¯¹è±¡

ä¸æŠŠ Apple Health / Fitbit / Whoop ç­‰ future import ç›´æŽ¥æ··å…¥åŒ»ç–—æ¡£æ¡ˆã€‚å»ºè®®å…ˆä¿ç•™ï¼š

```yaml
health_sample:
  sample_type:
  value:
  unit:
  start_time:
  end_time:
  recorded_at:
  source_name:
  source_version:
  device_ref:
  evidence_ref:
  interpretation_level: raw
  sensitivity: health
  sync_permission: local_only
```

ä»Žè¿™äº›æ ·æœ¬ç”Ÿæˆçš„ sleep sessionã€exercise summaryã€weekly trendã€doctor prep summary éƒ½æ˜¯ `projection` æˆ– `working`ï¼Œä¸æ˜¯ truthã€‚

## æ˜¯å¦æ”¹å˜å½“å‰ç»“æž„

å»ºè®®å°å¹…æ”¹å˜ï¼š

- P0ï¼šæ–°å¢ž `interpretation_level`ï¼Œç”¨äºŽ raw/source semantic/derived/reviewed/projection çš„è½»é‡åŒºåˆ†ã€‚
- P1ï¼šä¸ºæœªæ¥ä½ç½®/å¥åº·è¿žç»­æ•°æ®é¢„ç•™ `location_raw_point`ã€`place_visit_candidate`ã€`movement_segment_candidate`ã€`health_sample`ï¼Œä½†ä¸çŽ°åœ¨å®žçŽ°å¯¼å…¥å™¨ã€‚
- ä¿æŒä¸Šä¸€è½® `temporal_anchor` ä¸Ž `timeline_projection` ä¸å˜ï¼›æœ¬è½®åªæ˜¯è¡¥å……â€œæŠ•å½±ä»Žå“ªé‡Œæ¥ï¼Œä»¥åŠæºç³»ç»Ÿè¯­ä¹‰ä¸èƒ½ç›´æŽ¥å½“äº‹å®žâ€ã€‚

## æŽ¨è category / label å˜åŒ–

æ–°å¢žæˆ–æ˜Žç¡®ï¼š

```yaml
domain: location | health_stream
semantic_type: raw_point | place_visit_candidate | movement_segment_candidate | health_sample | health_interval | activity_summary
interpretation_level: raw | source_semantic | derived_candidate | reviewed_fact | projection
temporal_precision: instant | interval | day | month | unknown
location_sensitivity: normal | home_work_pattern | precise_gps | third_party_presence
```

## Proposed schema impact

è½»é‡ schema å½±å“ï¼š

- `labels` æˆ– sidecar æœ€å°å­—æ®µå¢žåŠ å¯é€‰ `interpretation_level`ã€‚
- `temporal_anchor` å¯¹ continuous stream è‡³å°‘è¦æ±‚ `start_time/end_time/time_source/timezone`ã€‚
- `timeline_entry` å¢žåŠ æˆ–æ˜Žç¡® `built_from_refs`ï¼ŒæŒ‡å‘ raw sample æˆ– source semantic objectã€‚
- `health_sample` å’Œ `location_raw_point` åªä½œä¸ºæœªæ¥å¯¼å…¥å…¼å®¹å¯¹è±¡ï¼Œä¸è¿›å…¥å½“å‰ MVP ä¸»å¹²ã€‚

## é£Žé™© / tradeoff

- å¥½å¤„ï¼šé¿å… Google/Apple/è®¾å¤‡åŽ‚å•†æŽ¨æ–­æ±¡æŸ“ä¸ªäººäº‹å®žå±‚ï¼›æœªæ¥å¯¼å…¥å¥åº·/ä½ç½®æ•°æ®æ—¶ä¸ä¼šé‡æž„æ—¶é—´çº¿æ¨¡åž‹ã€‚
- æˆæœ¬ï¼šå¤šä¸€ä¸ªè½»é‡æ ‡ç­¾ `interpretation_level`ï¼Œéœ€è¦æ–‡æ¡£è§£é‡Šæ¸…æ¥šã€‚
- éšç§é£Žé™©ï¼šç²¾ç¡® GPSã€home/work patternã€å¥åº·æ ·æœ¬å’Œç¡çœ æ•°æ®éƒ½é«˜åº¦æ•æ„Ÿï¼›é»˜è®¤ `local_only`ï¼Œé»˜è®¤ä¸ embedï¼Œä¸å¯¼å‡º rawã€‚
- è´¨é‡é£Žé™©ï¼šGoogle semantic export ä¼šå—ç¼–è¾‘å½±å“ï¼ŒApple Health export å¯èƒ½å·¨å¤§ä¸”å­—æ®µä¸å®Œæ•´ï¼›å¿…é¡»ä¿ç•™ `source_name/source_version/import_batch/evidence_ref`ã€‚

## Confidence

ä¸­é«˜ã€‚Timelinizeã€Google Takeout/DFIRã€Apple Health/HealthKitã€Fasten ä¸Ž QS Ledger çš„æ¨¡å¼ä¸€è‡´ï¼šåŽŸå§‹å¯¼å‡ºå’Œè¯­ä¹‰/åˆ†æžè§†å›¾å¿…é¡»åˆ†å±‚ã€‚å”¯ä¸€ä¸ç¡®å®šç‚¹æ˜¯æœªæ¥å®žé™…é€‰æ‹©å“ªäº›è®¾å¤‡/å¯¼å‡ºæ ¼å¼ï¼Œå› æ­¤åªå»ºè®®æ–‡æ¡£çº§é¢„ç•™ï¼Œä¸å»ºè®®å®žçŽ°ã€‚

## ä¸‹æ¬¡è°ƒæŸ¥

- æ·±å…¥æ¯”è¾ƒ Apple Health exportã€HealthKit live sampleã€Fitbit/Whoop export çš„å­—æ®µå·®å¼‚ï¼Œç¡®å®š `health_sample` æœ€å°å­—æ®µæ˜¯å¦è¶³å¤Ÿã€‚
- è°ƒæŸ¥ Dawarich / OwnTracks / GPSLogger ä¸€ç±» local-first location history å·¥å…·ï¼ŒéªŒè¯ `location_raw_point -> place_visit_candidate -> map_view` æ˜¯å¦è¶³å¤Ÿã€‚
- ç»™ `daily_projection` å†™ä¸€é¡µè§„åˆ™ï¼šä½ç½®å’Œå¥åº·æ•°æ®é»˜è®¤æ˜¾ç¤ºç²’åº¦ã€å“ªäº›åªæ˜¾ç¤ºè®¡æ•°/è¶‹åŠ¿ã€å“ªäº›å¿…é¡» redactedã€‚


