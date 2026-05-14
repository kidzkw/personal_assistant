# 2026-05-13 13:24 EDT - source snapshot / import run / error-as-record 研究

本轮目标：继续优化 local-first、file-first、whole-life personal database 的信息架构，重点检查旧硬盘、旧邮箱、GDPR/Takeout 导出、照片库、健康数据、浏览历史等“非实时、大批量、会反复导入”的长期数据源如何进入系统。

## 结论摘要

当前结构已经比较完整地覆盖了 evidence、sidecar、provenance、review gate、field contract、medical/email/relationship 等层。但还缺一个跨域对象：`source_snapshot` / `import_run` / `parse_error_record`。

原因是全生活数据库不会只接收干净的单条文件。真实输入经常是：

- 一个 Google Takeout / GitHub archive / Apple Photos library / old disk / old mailbox / bank export。
- 同一来源会多次导入，字段会变化，API 会断，文件会移动，部分记录会解析失败。
- 失败本身也有长期价值：它说明“这批数据里有东西没进来”，未来修复解析器后应可重跑。

因此建议把“导入批次”和“解析失败”提升为一等记录，而不是只留在日志里。

## Sources checked

### HPI / Human Programming Interface

- GitHub: https://github.com/karlicoss/HPI
- 说明页: https://karlicoss.github.io/hpi.html

发现的模式：

- HPI 的核心不是把所有个人数据先塞进一个巨型 DB，而是用 source-specific 模块把本地文件系统上的 JSON/SQLite/export 转成统一 Python 对象。
- 它覆盖社交、阅读、标注、todo、健康、位置、照片、浏览历史、聊天等非常接近本项目的 whole-life 范围。
- 它明确接受“本地同步数据有延迟”这个 tradeoff，换取快速、可靠、离线可用。

为什么重要：

- 对本项目来说，第一层不应只是 `raw_evidence`，还应记录“这一批 raw_evidence 来自哪个源快照/导入批次”。
- 不同 source adapter 的输出应该有同一层契约：adapter 版本、输入快照 hash、输出对象数量、失败数量、字段覆盖范围、隐私默认值。

是否改变当前结构：

- 建议新增 P0 级结构：`source_snapshot`、`import_run`、`parse_error_record`。
- 这不替代 file-first inbox，而是补在 inbox 与 raw_evidence/assets 之间。

风险 / tradeoff：

- 会增加元数据量，但这是换取长期可复现导入、增量导入、解析器升级后重跑的必要成本。
- source snapshot metadata 可能泄露账户名、目录结构、设备路径，需要默认 `local_only`。

### cachew

- GitHub: https://github.com/karlicoss/cachew

发现的模式：

- cachew 用函数参数/hash 判断输入是否变化，并把解析结果持久化到本地 SQLite。
- 它支持把 `Exception` 作为可缓存类型之一，这对“错误也是数据”很有启发。
- 它特别适合增量数据导出：一堆定期生成的数据切片可以被统一成一个流，而不用每次全量重算。

为什么重要：

- 本项目的解析层不应只输出成功对象；应该把失败、跳过、字段缺失、低置信解析都结构化保存。
- `parse_error_record` 可以挂到 `import_run` 和具体 `evidence_ref`，未来能回答“哪些医疗 PDF 没 OCR 成功”“哪些旧邮箱附件还没解析”“哪些照片缺 EXIF 时间”。

是否改变当前结构：

- 建议新增 `processing_artifact` 或 `materialized_view_cache`，但只作为可重建缓存，不作为事实真相。
- `parse_error_record` 则建议保留为审计/质量对象，因为它影响完整性。

风险 / tradeoff：

- 需要区分 transient error 和 permanent limitation，否则错误表会膨胀。
- 错误信息可能含敏感路径、文件名、邮件 header 或医疗术语，应继承源对象的 sensitivity/sync_permission。

### Dogsheep / Datasette / sqlite-utils

- Dogsheep GitHub-to-SQLite: https://github.com/dogsheep/github-to-sqlite
- Datasette ecosystem docs: https://docs.datasette.io/en/0.56/ecosystem.html
- Dogsheep photos: https://pypi.org/project/dogsheep-photos/

发现的模式：

- Dogsheep 把不同在线服务导入 SQLite，用 Datasette 做可浏览、可查询的个人数据仓库。
- sqlite-utils 支持从 JSON/CSV/TSV 自动创建/演进表、配置 FTS、拆 lookup table。
- dogsheep-photos 支持为照片生成 metadata DB，也支持创建 subset database；说明照片元数据尤其需要可裁剪分享，因为 GPS 等字段敏感。

为什么重要：

- 本项目可以保留 file-first 真相层，同时生成 read-only exploratory SQLite / FTS 视图，给调试、人工审阅、临时分析使用。
- 这个视图不应成为唯一真相；它应有 `built_from_import_run_ids`、`schema_version`、`generated_at`。

是否改变当前结构：

- 建议新增 P1：`exploratory_index_view` / `local_data_warehouse_view`，作为查询/审阅层，而不是核心事实层。
- 对照片/邮件/财务/健康的大批量导入尤其有价值。

风险 / tradeoff：

- Datasette/Dogsheep 偏“结构化数据探索”，不直接解决高敏感内容的权限裁剪。
- 任何 shareable subset 都必须显式声明字段 allowlist，尤其 GPS、人脸、医疗、财务、关系图谱。

### Perkeep

- Permanodes: https://perkeep.org/doc/schema/permanode.md
- Schema overview: https://perkeep.org/doc/schema/
- Terminology: https://perkeep.org/doc/terms.md

发现的模式：

- Perkeep 用内容寻址 blob 保存不可变数据，用 `permanode` 作为可变对象的稳定锚点。
- 对 permanode 的修改不是直接覆盖对象，而是追加 signed `claim`：`add-attribute`、`set-attribute`、`del-attribute`。
- 可变对象状态是把相关 claims 按顺序合成出来的结果。

为什么重要：

- 当前设计已有 immutable evidence、sidecar、append-only audit log、field merge policy，但“可变对象的稳定 identity”还不够明确。
- 一个 `person_profile`、`medical_condition`、`account`、`property`、`vehicle`、`subscription_schedule` 可能跨多年持续变化，不应把每次变更直接覆盖在主对象上。

是否改变当前结构：

- 建议引入 `object_anchor` + `attribute_claim` 抽象：
  - `object_anchor` 提供稳定 ID，不直接存可变事实。
  - `attribute_claim` 表示 set/add/del/merge/retract，并指向 evidence_refs、review_state、claim_state、field_contract。
  - 当前对象视图是 claim fold/materialized view。

风险 / tradeoff：

- 对第一版应用实现可能过重；但作为文档级 IA 约定很有价值。
- 不是每个对象都需要完整 claim 模型，优先用于长期可变且高风险对象：person/account/medical/finance/property/device。

### Reddit: personal archive retrieval / data hoarding

- 大型个人归档检索讨论: https://www.reddit.com/r/DataHoarder/comments/1m05hm4/for_those_with_large_personal_archiveshow_do_you/
- 搜索个人 hoard 的工具/目录结构讨论: https://www.reddit.com/r/DataHoarder/comments/1rlak32/how_are_you_actually_searching_your_hoard/
- 是否维护实际数据库: https://www.reddit.com/r/DataHoarder/comments/1icit95
- Reddit user archive to SQLite: https://www.reddit.com/r/DataHoarder/comments/13wyxhf

发现的模式：

- 真实用户长期依赖“好目录/好文件名 + 中央目录/索引 + 专用工具”的组合，而不是单一万能 app。
- 对多硬盘/离线盘，用户关心“在哪个硬盘、哪个路径、hash 是什么、需要接哪块盘”。
- 有用户明确描述用日志式文件记录新文件/删除/修改、hash、EXIF、perceptual hash，并可加载到 SQLite。
- 社区对“AI 管理全部内容”并不默认信任；可解释的目录、文件名、hash、索引更被接受。

为什么重要：

- 本项目的 `raw_evidence` 需要补充 `storage_location_ref` / `volume_ref` / `availability_state`，支持外接硬盘、NAS、冷归档。
- 检索结果应能区分：可立即打开、本地索引可见但原件离线、仅有目录记录、原件缺失。

是否改变当前结构：

- 建议把 storage/catalog 维度补进 raw evidence 和 retrieval：`volume_id`、`volume_label`、`device_serial_hash`、`last_seen_at`、`availability_state`。
- 这对照片、旧文档、税务、家庭历史、旧硬盘特别关键。

风险 / tradeoff：

- 设备序列号和路径本身敏感，需要 hash 或 redacted display。
- 离线盘索引可能过期，必须通过 `last_verified_at` 和 content hash 降低误导。

## 推荐 category / label changes

建议新增或明确以下标签维度：

```yaml
source_snapshot:
  snapshot_type: api_export | gdpr_archive | takeout | mailbox_dump | photo_library | filesystem_scan | device_backup | manual_import
  snapshot_state: complete | partial | interrupted | unknown
  source_account_id:
  source_adapter:
  adapter_version:
  captured_at:
  imported_at:
  content_hash:
  sensitivity:
  sync_permission: local_only

import_run:
  run_state: planned | running | completed | completed_with_errors | failed | superseded
  import_mode: full | incremental | replay | repair | dry_run
  parser_version:
  input_snapshot_refs:
  output_counts:
  error_counts:
  started_at:
  finished_at:

parse_error_record:
  error_scope: snapshot | file | message | attachment | chunk | field
  error_kind: missing_field | unsupported_format | decode_error | ocr_failed | auth_gap | schema_drift | duplicate_conflict | low_confidence
  recoverability: retryable | repairable | ignored | permanent_unknown
  affected_ref:
  evidence_refs:
  import_run_id:
  sensitivity:
  review_state:

storage_location:
  volume_id:
  volume_label:
  device_serial_hash:
  original_path:
  normalized_path:
  availability_state: online | offline_indexed | missing | cold_archive
  last_seen_at:
  last_verified_at:
```

## Proposed schema impact

P0 建议：

1. 在 file-first inbox 之前或并列新增 `source_snapshot`，表示“这批输入是什么”。
2. 每次导入/重跑/OCR/解析新增 `import_run`，并把所有新建 evidence、asset、chunk、candidate、error 都挂到该 run。
3. 新增 `parse_error_record`，把失败解析、字段缺失、低置信、schema drift 作为可检索/可审阅质量对象。
4. 对长期可变实体新增可选 `object_anchor` + `attribute_claim` 模型，优先用于人、账户、医疗、财务、设备、房产/车辆等对象。

P1 建议：

1. 新增 `local_data_warehouse_view` / `exploratory_index_view`，用只读 SQLite/FTS/BM25 视图辅助人工审阅和调试。
2. 为离线硬盘/NAS/冷归档新增 `storage_location_ref` 和 `availability_state`。

## Confidence

高。HPI、Dogsheep、Perkeep 和 Reddit 经验都从不同方向指向同一个结论：长期个人数据库的难点不是单条干净记录，而是跨多年、跨来源、跨格式、跨硬盘的导入复现、错误追踪、索引可解释性和可变对象身份。

## Privacy / safety considerations

- `source_snapshot` 和 `import_run` 默认 `local_only`，因为它们可能包含账户名、目录结构、设备路径、邮箱地址、医疗机构名。
- `parse_error_record` 继承 affected evidence 的最高 sensitivity；错误消息不要默认进入外部 LLM 或同步层。
- `storage_location` 中的设备序列号应 hash；原始路径可保存但 retrieval UI 应默认显示 redacted path。
- `object_anchor` / `attribute_claim` 不应自动确认高风险事实；claim 仍需 `review_state`、`claim_state`、`evidence_refs`。

## What to investigate next

1. 把 `source_snapshot/import_run/parse_error_record` 写成最小字段矩阵，并和现有 `provenance.record` 去重。
2. 为旧邮箱、Google Takeout、Apple Photos/Immich、旧硬盘 scan 各写一个导入批次示例。
3. 研究是否用 `object_anchor + attribute_claim` 统一 person/account/medical condition/subscription 等长期可变对象。
4. 为离线硬盘和冷归档制定 `availability_state` 与 `last_verified_at` 规则。
