# 2026-05-13 17:26 EDT - Raw samples vs semantic activity projections

本轮问题：上一轮已经把 `timeline_projection` 和 `temporal_anchor` 纳入 P0，但还需要继续确认位置历史、Apple Health / wearable、未来 audio stream 这类连续数据应该怎样进入个人记忆库，避免把 Google/Apple/设备厂商的语义推断直接当成事实。

## 读取的本地上下文

- `information-processing/README.md`
- `information-processing/06-global-workflow.md`
- `information-processing/07-personal-memory-minimal-workflow.md`
- `information-processing/research/candidate-proposals.md`
- `docs/omi-information-processing-analysis.md`

当前方向仍然成立：local-first、file-first inbox、原始证据保留、AI/OCR/来源系统推断先做 candidate/projection，重要事实需要 evidence pullback。

## 外部来源

1. Timelinize
   - GitHub: https://github.com/timelinize/timelinize
   - Go package docs: https://pkg.go.dev/github.com/timelinize/timelinize/timeline
   - 发现：Timelinize 把导入数据放在本地文件夹和 SQLite 中，并通过 timeline / map / conversation / gallery 等 projection 组织浏览；其模型支持 timestamp、timespan、timeframe、time_offset、time_uncertainty，并且强调原始 source data 仍要保留。
   - 意义：继续支持上一轮判断，timeline/map/gallery 不能成为 truth，只能是从原始 item、entity、location、conversation 生成的视图。

2. Google Takeout Location History / Semantic Location History
   - schema reference: https://locationhistoryformat.com/reference/semantic/
   - general structure: https://locationhistoryformat.com/guides/general-structure/
   - DFIR Review: https://dfir.pubpub.org/pub/d39u7lg1
   - Reddit: https://www.reddit.com/r/GoogleMaps/comments/1g6gx3v/the_semantic_location_history_from_google_takeout/
   - 发现：Google Takeout 通常同时有 raw `Records.json` 和较高层的 `Semantic Location History`；语义层由 `activitySegment` 与 `placeVisit` 组成，按月 JSON 存放。DFIR 分析显示，用户编辑会影响 Semantic Location History，而 raw location data 可以保持不同性质的原始证据。Reddit 讨论也提醒旧版 Takeout 的 semantic export 可能比迁移后的设备端导出更完整。
   - 意义：个人数据库不应把 `placeVisit` / `activitySegment` 直接确认成“我确实去了哪里/做了什么”。它们应带 `source_interpretation_level=source_semantic`、`confidence`、`time_source`、`location_source`，并可从 raw records 回拉。

3. Apple Health / HealthKit
   - Apple `HKSample.startDate`: https://developer.apple.com/documentation/healthkit/hksample/startdate
   - Apple `HKSourceRevision`: https://developer.apple.com/documentation/healthkit/hksourcerevision
   - Reddit export examples: https://www.reddit.com/r/AppleWatch/comments/1irkloq and https://www.reddit.com/r/AppleWatch/comments/1goka7n
   - 发现：HealthKit sample 有 start/end window；source revision/source/device 对 provenance 很关键。Apple Health XML export 在社区反馈里常见问题是体量大、难处理、字段会随类型变化，症状等类别可能丢失细节。
   - 意义：未来健康/wearable 导入的最小对象不应一开始就是 `medical_record`，而应先是 `health_sample` / `health_interval`：保留 type、unit、value、start/end、source/device、creation/import time、raw record ref。日/周统计、睡眠段汇总、运动趋势是 cache/projection。

4. Fasten Health
   - GitHub: https://github.com/fastenhealth/fasten-onprem
   - Fasten docs / Connect event shape: https://docs.connect.fastenhealth.com/webhooks/events
   - Reddit: https://www.reddit.com/r/selfhosted/comments/12pcna3
   - 发现：Fasten OnPrem 定位为 self-hosted personal/family health record viewer，开源版当前强调手动录入或导入 FHIR bundle；Connect 一侧可把医疗记录以 NDJSON/FHIR resource 批量输出。
   - 意义：医疗记录仍应保持“文档证据 + 简化对象 + citation”的个人版做法；FHIR resource 名称可作为字段命名参考，但不应把所有健康/wearable samples 都升级为完整医疗记录。

5. QS Ledger
   - GitHub: https://github.com/markwk/qs_ledger
   - 发现：个人 quantified-self 项目常见目标是下载各服务数据、存本地、再做分析/仪表盘；raw download 与 analysis output 是两层。
   - 意义：个人记忆库里，连续健康/位置/活动流的第一价值是“可保留、可检索、可回溯”，分析看板是可重建输出。

## 结构性发现

### 1. 连续数据需要区分 raw sample 与 source semantic object

位置、健康、活动、未来音频/可穿戴流都不应直接进入 `memory` 或 `medical_record`。更稳的个人版分层：

```text
raw_sample / raw_record
 -> source_semantic_object
 -> derived_projection
 -> reviewed memory / task / medical / finance object
```

建议新增一个轻量标签：

```yaml
interpretation_level: raw | source_semantic | derived_candidate | reviewed_fact | projection
```

它和 `review_state` 不重复：`review_state` 表示人是否确认；`interpretation_level` 表示这条记录本身离原始观测有多远。

### 2. 位置历史的最小个人版对象

当前不建议实现 Google sync 或地图功能，只建议把未来兼容对象写清：

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

这些对象只服务于 `travel_timeline`、`map_view`、`daily_projection` 和“我那天大概在哪里”这类检索。除非用户明确确认，不应自动生成“我去了 X”的长期记忆。

### 3. 健康/wearable 样本的最小个人版对象

不把 Apple Health / Fitbit / Whoop 等 future import 直接混入医疗档案。建议先保留：

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

从这些样本生成的 sleep session、exercise summary、weekly trend、doctor prep summary 都是 `projection` 或 `working`，不是 truth。

## 是否改变当前结构

建议小幅改变：

- P0：新增 `interpretation_level`，用于 raw/source semantic/derived/reviewed/projection 的轻量区分。
- P1：为未来位置/健康连续数据预留 `location_raw_point`、`place_visit_candidate`、`movement_segment_candidate`、`health_sample`，但不现在实现导入器。
- 保持上一轮 `temporal_anchor` 与 `timeline_projection` 不变；本轮只是补充“投影从哪里来，以及源系统语义不能直接当事实”。

## 推荐 category / label 变化

新增或明确：

```yaml
domain: location | health_stream
semantic_type: raw_point | place_visit_candidate | movement_segment_candidate | health_sample | health_interval | activity_summary
interpretation_level: raw | source_semantic | derived_candidate | reviewed_fact | projection
temporal_precision: instant | interval | day | month | unknown
location_sensitivity: normal | home_work_pattern | precise_gps | third_party_presence
```

## Proposed schema impact

轻量 schema 影响：

- `labels` 或 sidecar 最小字段增加可选 `interpretation_level`。
- `temporal_anchor` 对 continuous stream 至少要求 `start_time/end_time/time_source/timezone`。
- `timeline_entry` 增加或明确 `built_from_refs`，指向 raw sample 或 source semantic object。
- `health_sample` 和 `location_raw_point` 只作为未来导入兼容对象，不进入当前 MVP 主干。

## 风险 / tradeoff

- 好处：避免 Google/Apple/设备厂商推断污染个人事实层；未来导入健康/位置数据时不会重构时间线模型。
- 成本：多一个轻量标签 `interpretation_level`，需要文档解释清楚。
- 隐私风险：精确 GPS、home/work pattern、健康样本和睡眠数据都高度敏感；默认 `local_only`，默认不 embed，不导出 raw。
- 质量风险：Google semantic export 会受编辑影响，Apple Health export 可能巨大且字段不完整；必须保留 `source_name/source_version/import_batch/evidence_ref`。

## Confidence

中高。Timelinize、Google Takeout/DFIR、Apple Health/HealthKit、Fasten 与 QS Ledger 的模式一致：原始导出和语义/分析视图必须分层。唯一不确定点是未来实际选择哪些设备/导出格式，因此只建议文档级预留，不建议实现。

## 下次调查

- 深入比较 Apple Health export、HealthKit live sample、Fitbit/Whoop export 的字段差异，确定 `health_sample` 最小字段是否足够。
- 调查 Dawarich / OwnTracks / GPSLogger 一类 local-first location history 工具，验证 `location_raw_point -> place_visit_candidate -> map_view` 是否足够。
- 给 `daily_projection` 写一页规则：位置和健康数据默认显示粒度、哪些只显示计数/趋势、哪些必须 redacted。
