# 2026-05-13 时间线投影视图与时间不确定性（GitHub/Reddit）

运行时间：2026-05-13 16:26 EDT

## 本轮问题

当前结构已经有 `daily_timeline / medical_timeline / finance_timeline / relationship_timeline` 等概念，也已有 `scope / aggregation_level`、`truth / cache / export`、`source_membership`、`citation_ref` 等提案。本轮重点检查：长期 whole-life personal database 是否应该把“时间线/每日总结”作为主对象，还是作为从原子证据和 confirmed/candidate objects 生成的投影视图。

结论：**时间线应该是一等投影视图，但不应成为事实主存储**。需要新增一个轻量 `timeline_projection` / `timeline_entry` 约定，用来表达“某个对象如何出现在某个时间线视图里”，并显式处理时间不确定性、来源成员关系、权限裁剪和证据回拉。

## 来源与发现

### 1. Timelinize / Timeliner：时间线、地图、会话、图库是 projections

- 来源：
  - Timelinize 官网：https://timelinize.com/
  - Timeliner GitHub README：https://github.com/mholt/timeliner
  - Timelinize Go package docs：https://pkg.go.dev/github.com/timelinize/timelinize/timeline
- 发现：
  - Timelinize 是本地个人归档套件，目标是把照片、视频、短信、聊天、邮件、旅行、社交、联系人、运动、文档等统一到本地 timeline folder：SQLite database + data files。
  - Timeliner README 说明其基本架构是把导入数据存到本机 SQLite，二进制文件放在相邻文件夹；Timelinize 的改进包括 entity-aware schema、多个时间字段、保留 original path 和 intermediate path。
  - README 明确列出 timeline / map / conversation / gallery / raw item list / raw entity list，其中前四个是不同 paradigm 的 projections。
  - Timelinize 的时间字段包括 `timestamp`、`timespan`、`timeframe`、`time_offset`、`time_uncertainty`，用于表达跨时段、不确定时间、不同时区、旧照片扫描等情况。
- 为什么重要：
  - 当前 personal DB 已经有 daily/domain timeline，但还没有明确“时间线条目本身是 projection，不是事实层”。
  - whole-life 数据里时间经常不确定：老照片只知道年份，账单有 bill date/due date/paid date，就诊记录有 appointment time/report issued time/import time，邮件有 sent/received/imported，照片有 EXIF captured/file modified/imported。单一 `occurred_at` 不够。
- 是否改变当前结构：
  - 建议改变：新增 `temporal_anchor` 与 `timeline_projection` 概念，避免把 daily log / map / gallery 的显示结果写成事实。
- 风险/权衡：
  - 增加时间字段复杂度；第一版可只在高价值对象上使用完整 temporal fields，其余对象保留 `occurred_at + temporal_precision + timezone`。

### 2. ActivityWatch：source stream/bucket + event(timestamp,duration,payload) 适合未来连续流，但 timezone 不能丢

- 来源：
  - ActivityWatch data model：https://docs.activitywatch.net/en/latest/buckets-and-events.html
  - ActivityWatch intro：https://docs.activitywatch.net/en/stable/intro.html
- 发现：
  - ActivityWatch 建议一个 watcher/host 一个 bucket；bucket 有 event type，event 是 `timestamp + duration + data`。
  - heartbeats 会把相邻且 data 相同的事件在 pulsetime 窗口内合并，用来降低连续采集的噪声和存储。
  - 文档也提醒所有 timestamp 存 UTC，timezone offset 当前会被丢弃。
- 为什么重要：
  - 这支持现有 P1-1：未来音频、wearable、屏幕活动等连续流应该先以 stream/bucket/event 保存，再派生日视图、session、记忆。
  - 但 whole-life DB 不能丢 timezone：旅行、医疗预约、航班、账单截止日期、照片 EXIF 都需要本地时间语义。
- 是否改变当前结构：
  - 建议深化 P1-1：`stream_event` 应保留 `timezone` 或 `utc_offset_at_source`，并把 heartbeat/merge 结果标成 `aggregation_level=session|event_cluster`，不能覆盖 raw event。
- 风险/权衡：
  - 保存 raw event 与 merged event 会增加存储；但可把 merged event 作为 cache/projection，raw event 按 retention class 控制。

### 3. TimelineQA / personal-timeline：个人时间线问答同时需要 retrieval-based 与 view-based 查询

- 来源：
  - facebookresearch personal-timeline GitHub：https://github.com/facebookresearch/personal-timeline
  - TimelineQA paper：https://arxiv.org/abs/2306.01069
- 发现：
  - personal-timeline pipeline 把多源数据导入 SQLite/raw CSV，构建 summaries，用于可视化和搜索。
  - QA 有三类：普通 ChatGPT、retrieval-based QA、view-based QA。view-based 通过 SQL/tabular views 回答 aggregate/min/max 类问题，如数量、最后一次旅行等。
  - TimelineQA 强调 lifelog 同时包含自由文本、结构化时间/地理信息，个人助理问答需要能处理 atomic 与 multi-hop 时间线问题。
- 为什么重要：
  - 当前检索设计已包括 exact search、BM25、vector later、graph lookup，但 timeline/domain view 的“聚合问答”还可更明确。
  - `daily_timeline` 不能只是一篇文字总结；它还要支持“上次 X 是什么时候”“四月买了多少书/药/票”“某城市旅行期间看了哪些医生/见了谁”等 view-based 查询。
- 是否改变当前结构：
  - 建议新增 `projection_entry` 的 sparse keys：`date_bucket`、`entity_refs`、`place_refs`、`domain`、`amount_refs`、`source_refs`、`confidence`，供 SQL/FTS/BM25/graph 混合查询。
- 风险/权衡：
  - view-based 查询可能让用户误以为聚合结果一定正确。高风险领域必须显示 `coverage_state`：complete / partial / unknown。

### 4. Obsidian / Reddit：daily note 适合 capture 和回顾，但长期检索依赖结构化链接、标签、Dataview/rollup

- 来源：
  - Reddit: How do you keep short daily logs in Obsidian? https://www.reddit.com/r/ObsidianMD/comments/1sjjoft/how_do_you_keep_short_daily_logs_in_obsidian_one/
  - Reddit: Using Obsidian as a Life Record https://www.reddit.com/r/ObsidianMD/comments/1cxaprw
  - Reddit: PKMs that help create personal timeline https://www.reddit.com/r/PKMS/comments/1e0ir4o
- 发现：
  - 用户常把 daily note 作为当天入口、工作日志、临时想法、创建/修改笔记 rollup；重要或可行动内容会拆到独立 note。
  - 有用户用 Dataview/weekly note 聚合 daily entries，也有人用 GPS/GPX 或 Google Timeline 导入来做地图/日视图。
  - 讨论中反复出现两个痛点：daily note 太大时难复用；每件小事都拆 note 会产生 clutter。关键不是单文件还是多文件，而是 retrieval method 是否稳定。
  - PKM timeline 讨论提醒：把银行/健康等敏感数据放入第三方时间线有安全难题，过滤后的 timeline 比“全量混合 timeline”更有用。
- 为什么重要：
  - 对个人系统，daily readable summary 可以存在，但只能是 working/export 层；长期检索应依赖原子对象、标签、链接和 projection entry。
  - 时间线需要按权限过滤：普通日记可显示，医疗/财务/关系细节默认不进入外部同步或公开摘要。
- 是否改变当前结构：
  - 建议为 `daily_narrative_log` 增加 `built_from_projection_id`、`redaction_policy`、`coverage_state`，并默认不作为 evidence。
- 风险/权衡：
  - 如果投影视图太抽象，个人维护成本会上升；第一版可以只维护 `daily_projection` 和 `domain_projection` 两类。

### 5. Reddit DataHoarder：本地照片/文档检索的长期痛点是“能找到”，不是分类完美

- 来源：
  - Reddit: Digital Photos, Organizing, and Local AI https://www.reddit.com/r/DataHoarder/comments/1rmwmiq/digital_photos_organizing_and_local_ai/
  - Reddit: How to best organise photos/videos of 15 years https://www.reddit.com/r/DataHoarder/comments/1rl8dy8/how_to_best_organise_photosvideos_of_15_years/
  - Reddit: For large personal archives, how do you retrieve what you need https://www.reddit.com/r/DataHoarder/comments/1m05hm4/for_those_with_large_personal_archiveshow_do_you/
- 发现：
  - 用户会按 year/month/day 文件夹、轮换硬盘、NAS、本地/云备份组织照片，但仍希望有本地 AI 搜索、标签、事件/地点/人检索。
  - 多年照片/视频整理常见需求是去重、备份、按年月组织、删除低价值内容、可选云端；但完全手工分类成本高。
  - 大型个人归档检索往往按大类树、专用系统（Immich/PhotoPrism/Paperless/ArchiveBox）和本地搜索组合，而不是一个完美分类法。
- 为什么重要：
  - 照片/文档 pipeline 不应强制用户先完美归档；应先保存 original_path/source_folder/content hash，然后通过 projection/label/index 渐进增强检索。
- 是否改变当前结构：
  - 建议 `timeline_entry` 支持 `display_group`（例如 event/day/trip/album/thread）和 `source_membership_refs`，让同一资产可出现在多个视图而不复制事实。
- 风险/权衡：
  - AI caption/semantic search 很有用但可能误标；caption 只能是 candidate/cache，不能污染 original evidence。

## 建议新增结构

### `temporal_anchor`

用于替代“所有对象只有一个 occurred_at”的隐含假设。

```yaml
temporal_anchor:
  primary_time:
  primary_time_role: captured_at | sent_at | received_at | issued_at | due_at | paid_at | appointment_at | observed_at | created_at | modified_at | ingested_at | inferred_at
  start_time:
  end_time:
  timeframe:
  temporal_precision: exact | minute | hour | day | month | year | approximate | unknown
  timezone:
  utc_offset:
  time_uncertainty:
  time_source:
  alternative_times:
```

### `timeline_projection`

```yaml
timeline_projection:
  projection_id:
  projection_type: daily | domain | entity | place | trip | conversation | gallery | map | review
  query_or_rule_ref:
  built_at:
  built_from_refs:
  permission_scope:
  redaction_policy:
  coverage_state: complete | partial | unknown
  cache_identity:
```

### `timeline_entry`

```yaml
timeline_entry:
  entry_id:
  projection_id:
  canonical_ref:
  source_membership_refs:
  temporal_anchor:
  display_time:
  sort_time:
  display_group:
  domain:
  entity_refs:
  place_refs:
  evidence_refs:
  citation_refs:
  sensitivity:
  sync_permission:
  review_state:
  confidence:
  entry_role: evidence | candidate | confirmed_object | summary | reminder | cache
```

## 推荐 category / label changes

- 新增 `semantic_type`: `timeline_projection`、`timeline_entry`、`temporal_anchor`。
- 新增/固化 `aggregation_level`: `projection_entry`、`daily_view`、`domain_view`、`map_view`、`gallery_view`、`conversation_view`。
- 在时间相关标签中增加：
  - `temporal_precision`
  - `primary_time_role`
  - `time_uncertainty`
  - `coverage_state`
- 在 projection/view 层增加：
  - `permission_scope`
  - `redaction_policy`
  - `built_from_refs`
  - `cache_identity`

## Proposed schema impact

- P0 级：把 `timeline_projection/timeline_entry` 写入候选提案，明确时间线是 projection，不是事实主存储。
- P0 级：为 `raw_evidence/media_asset/email_message/chat_message/medical_item/finance_item/event/task` 增加可选 `temporal_anchor`。
- P1 级：把 ActivityWatch 风格 `stream_event` 的 timezone/merge semantics 补充到 P1-1。
- P1 级：`daily_narrative_log` 增加 `built_from_projection_id`、`coverage_state`、`redaction_policy`，并标记为 working/export 层。

## Confidence

中高。GitHub/文档来源与 Reddit 实践一致：本地归档和长期检索都需要时间线，但可靠系统会把时间线视为 projection/view，而不是把 daily note 或 AI summary 作为事实源。主要不确定点是第一版是否要完整实现 `timeline_projection`，还是先只在文档中约定字段。

## Privacy / safety considerations

- 时间线会把分散的敏感信息重新聚合，隐私风险高于单条记录；必须按 child objects 计算 `max_sensitivity` 和 `min_sync_permission`。
- 地图/旅行/医疗/关系/财务时间线默认 `local_only`，外部导出只允许 redacted summary。
- `daily_narrative_log` 不能默认包含医疗、财务、关系、账号安全细节；需要 `redaction_policy`。
- 聚合视图必须显示 `coverage_state`，避免用户把不完整导入误认为完整历史。
- AI caption、LLM daily summary、semantic cluster 只属于 candidate/cache/working 层，不能作为 confirmed fact。

## 下一步调查

1. 深入 Timelinize schema / migration：确认 item/entity/attribute/time fields 的实际表设计，提炼个人版最小字段。
2. 调查 location history / GPX / Google Timeline Takeout 的本地归档结构，补足 `place_ref` 与 `map_view`。
3. 调查 Apple Health / HealthKit export、QS Ledger、Fasten Health 的时间字段，验证 health timeline 是否需要独立 `observed_at / recorded_at / effective_at`。
4. 调查 calendar/email/chat 中同一事件的多重时间：sent/received/imported/due/confirmed/cancelled。
5. 为 `daily_projection` 写一页最小规范：哪些条目进入日视图、哪些被 redacted、哪些只显示计数。
