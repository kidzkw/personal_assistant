# 2026-05-13 -- Local archive, index cache, and medical citation loop

本轮目标：在“个人记忆库，不是企业级系统”的约束下，继续研究 whole-life personal database 的信息架构。重点不是增加复杂 schema，而是确认哪些轻量结构能让 5+ 年后的检索、纠错、隐私和迁移更稳。

## 已读本地上下文

- `information-processing/README.md`
- `information-processing/07-personal-memory-minimal-workflow.md`
- `information-processing/research/candidate-proposals.md`
- 自动化记忆：确认上轮已经把全局 workflow 压缩为个人可维护主干：`inbox -> raw evidence/asset -> light labels -> parse/OCR/chunks -> candidates -> review -> personal memory objects -> search/timeline/reminders -> evidence pullback`

## 外部来源

1. Thoth
   - GitHub: https://github.com/siddsachar/Thoth
   - Architecture: https://github.com/siddsachar/Thoth/blob/main/docs/ARCHITECTURE.md
   - 发现：本地优先 assistant 把长期记忆做成 entity + typed relation，并用 FAISS + 一跳图扩展召回；同时有后台 “Dream Cycle” 做去重、关系推断、过期置信度衰减和日志。
   - 对本项目的意义：可以借鉴“召回先轻量、后台再整理”的思想，但不要照搬 67 种关系或复杂 dream 流程。个人版只需要 `memory/person/interaction/task/event` 加少量关系，并保留 `source/evidence_refs/confidence/review_state`。
   - 风险：后台自动合并/推断容易污染个人事实，尤其是关系、医疗和财务。必须默认 candidate + review。

2. msgvault
   - 首页: https://www.msgvault.io/
   - Architecture overview: https://www.msgvault.io/architecture/overview/
   - Data storage: https://www.msgvault.io/architecture/storage/
   - Vector search: https://www.msgvault.io/usage/vector-search/
   - 发现：邮件/聊天归档采用 SQLite 作为 system of record，Parquet 是可重建 analytics cache，附件按 SHA-256 content-addressed 存本地文件，FTS5 做关键词检索，vector search 是 opt-in 且向量本地存储。
   - 对本项目的意义：强化“真相层 vs 检索/分析缓存”的边界。个人 DB 第一版可以保留 SQLite/JSONL/sidecar 作为事实索引，把 DuckDB/Parquet/vector 都定义为可重建缓存，不进入核心真相层。
   - 风险：邮件正文、附件、向量嵌入都可能包含高敏信息；embedding endpoint 若非本地，会泄露邮件内容和 query 意图。

3. ArchiveBox
   - 官网: https://archivebox.io/
   - 发现：长期归档强调普通文件夹 + SQLite/JSON 元数据，保存 HTML/PDF/PNG/TXT/JSON/WARC 等多种冗余格式；集合可通过 Web UI、CLI、REST API、SQLite 或直接文件夹访问。
   - 对本项目的意义：whole-life database 也应把每个高价值 evidence 做成“证据包”：原件 + 提取文本/OCR + 缩略图/预览 + 元数据 sidecar + 可选导出格式。这样即使应用不可用，文件夹仍可读。
   - 风险：多种派生文件会增加存储和隐私暴露面；证据包需要清楚区分 original、derived、preview、redacted。

4. GitEHR
   - 官网: https://gitehr.org/
   - 发现：医疗记录强调 patient-owned、offline-first、append-only history、cryptographic trust 和 portable files。
   - 对本项目的意义：不建议为个人记忆库引入完整 GitEHR；但医疗/法律/财务这类高风险对象应至少保留简单 `change_log`，记录何时从哪份 evidence 提取、谁确认、后来是否修正。
   - 风险：完整 append-only cryptographic chain 过重；个人版只需要 audit habit，不需要医疗级 ledger。

5. Reddit: Obsidian as a better personal health repository
   - https://www.reddit.com/r/ObsidianMD/comments/1slqg1y/obsidian_as_a_better_personal_health_repository/
   - 发现：真实用户用 Obsidian + 本地 Markdown 管理家人复杂医疗资料，痛点集中在 OCR 质量、LLM 可能跳过源文件、医疗隐私、以及“如何优雅引用 raw PDF”。评论也强调医疗 LLM 输出必须回看数据源。
   - 对本项目的意义：医疗流水线要新增一个非常朴素但关键的要求：任何 `medical_candidate` / `lab_result` / `doctor_visit` 必须有 `citation_refs`，粒度至少到文件 + 页码/区域/原文片段；没有 citation 不进入 confirmed。
   - 风险：引用粒度太细会增加维护成本；第一版可以只要求 file/page/message_id，OCR region 以后再加。

6. Reddit: large personal archives retrieval
   - https://www.reddit.com/r/DataHoarder/comments/1m05hm4/for_those_with_large_personal_archiveshow_do_you/
   - 发现：大规模个人归档用户仍大量依赖目录、日期命名、中央索引、hash、EXIF、硬盘编号/序列号、NAS/外接盘位置。照片靠 PhotoPrism 等工具浏览，冷数据靠 catalog 找到哪块盘。
   - 对本项目的意义：上轮的 `storage_location_ref/availability_state` 方向成立，但应降级为个人版最小字段：`volume_label/device_hint/original_path/last_seen_at/availability_state`，不要一开始做复杂存储库存。
   - 风险：路径、盘符、设备名本身敏感；展示和同步时需要 redaction。

7. Reddit: “Immich for documents?”
   - https://www.reddit.com/r/selfhosted/comments/1sdx0jn/is_there_an_immich_for_documents/
   - 发现：普通用户采用 Paperless 类工具的核心原因是“所有重要文档集中、OCR、tags、correspondent/type 检索”，而不是复杂流程。
   - 对本项目的意义：document_record 第一版不应过早细分太多法律/保险/税务子对象。优先保留 `document_type/counterparty/date/tags/ocr_text_ref/evidence_ref/review_state`，高价值对象再派生 bill、deadline、medical、finance。
   - 风险：过度自动命名/归类会产生误导；重要文档默认 inbox/review。

## 本轮结构判断

### 1. 增强“证据包”概念，但保持个人版

建议把 `raw_evidence` / `media_asset` 的文件组织说明从“一个文件 + sidecar”扩展为“证据包 evidence packet”：

```text
/evidence/<year>/<id>/
  original.ext
  original.meta.json
  text.txt              # optional, derived
  ocr.json              # optional, derived
  preview.jpg           # optional, derived
  redacted.ext          # optional, manually approved
```

最小字段：

```yaml
evidence_packet_id:
original_ref:
content_hash:
derived_refs:
source_category:
occurred_at:
ingested_at:
sensitivity:
review_state:
```

为什么重要：这比把所有派生结果塞进 DB 更耐久，也比只放散乱文件更好迁移。

是否改变当前结构：建议 P1 纳入，不取代现有 `raw_evidence/media_asset`，而是作为其文件组织约定。

### 2. 明确“真相层、缓存层、导出层”三分

当前个人版 workflow 已有轻量索引，但还可以更明确：

```text
truth layer: original files + sidecar + confirmed objects
cache layer: FTS/BM25 tables, thumbnails, OCR cache, analytics parquet/duckdb, vectors
export layer: markdown/wiki/static html/csv/json bundles
```

最小规则：

- cache layer 必须可重建。
- cache layer 不允许成为唯一事实来源。
- vector embeddings 默认 P2，且必须记录 embedding model/provider/local_or_remote。
- export layer 默认 redacted/allowlist，不直接暴露敏感 evidence。

是否改变当前结构：建议 P0 纳入文档原则，因为它可以防止以后把检索优化变成数据锁定。

### 3. 医疗候选新增 citation gate

对医疗/健康建议新增：

```yaml
citation_refs:
  evidence_ref:
  page:
  excerpt:
  extraction_method:
```

规则：

- `medical_candidate` 没有 citation_refs，只能保持 candidate。
- lab_result 的 `key_values` 必须能回到原始 PDF/截图/邮件。
- LLM 医疗总结只能作为 `summary_candidate`，不作为诊断或建议。

是否改变当前结构：建议 P0 纳入医疗/高风险候选的 review 规则。

### 4. 邮件/聊天采用 msgvault 式最小归档分层

个人版可以采用：

```text
communication_source
 -> conversation
 -> message
 -> raw_message
 -> attachment_asset/evidence_packet
 -> derived_candidate
```

最小字段：

```yaml
source_account:
conversation_id:
message_id:
sent_at:
participants:
subject_or_title:
body_text_ref:
raw_ref:
attachment_refs:
labels_from_source:
personal_labels:
```

关键是区分 `labels_from_source` 与 `personal_labels`。Gmail/IMAP/聊天软件的标签只是来源快照，不等于个人记忆库语义标签。

是否改变当前结构：建议 P1；与已有 email_message / email_thread 分层一致，只是补充“源标签 vs 个人标签”的个人版命名。

### 5. 离线/冷归档位置保持极简

不建议当前就做完整 storage inventory。个人版字段：

```yaml
storage_location:
  availability_state: online | offline_indexed | missing
  volume_label:
  device_hint:
  original_path:
  last_seen_at:
```

是否改变当前结构：建议作为 P1 加入 `raw_evidence/media_asset`，尤其面向旧硬盘、NAS、老照片和税务/家庭档案。

## 推荐 category / label 变化

新增或调整：

- `storage_layer`: `truth | cache | export`
- `artifact_role`: `original | sidecar | extracted_text | ocr | preview | redacted | index_record | embedding`
- `citation_state`: `none | file_level | page_level | region_level | excerpt_level`
- `source_label_type`: `source_native | personal_semantic | pipeline_state`
- `availability_state`: `online | offline_indexed | missing`

不建议新增大量 domain category。当前 `daily/photo/health/finance/email/relationship/admin/travel/account/other` 仍够用。

## Proposed schema impact

P0 建议：

1. 在全局原则中明确 `truth/cache/export` 三层。
2. 对 health/medical/legal/finance/account_security/relationship 高风险候选新增 `citation_refs` 或 `citation_state` 要求。
3. 在派生索引、向量、分析缓存上新增 `storage_layer=cache`，并要求 `built_from_refs`。

P1 建议：

1. 为 evidence/media/document 增加 `evidence_packet` 文件组织约定。
2. 为 email/chat 增加 `labels_from_source` 与 `personal_labels` 的命名区分。
3. 为旧硬盘/NAS/冷归档增加极简 `storage_location` 字段。

P2 暂缓：

- 完整 append-only cryptographic ledger。
- 完整 dream cycle / automated memory refinement。
- 全量 graph relation vocabulary。
- 默认 vector search。

## Confidence

中高。多个独立项目和用户经验都指向同一个结论：个人长期数据库的核心不是复杂 schema，而是原件可读、来源可追、缓存可重建、敏感候选可审阅。医疗 citation gate 的信心高；Thoth 式自动整理的适用性中等，需要严格降级。

## Privacy / safety

- 医疗、财务、关系、账号安全默认 `local_only`。
- embedding/vector search 不应默认启用；若启用，必须记录本地/远程 endpoint。
- evidence packet 中的 preview/OCR/export 可能泄露比原件更易搜索的敏感信息，权限不得低于 original。
- 邮件和聊天的 source-native labels、headers、路径、设备名、账户名都可能是敏感元数据。
- 医疗总结不得作为诊断、治疗或理赔建议；必须保留 source citation 并提示人工核对。

## 下一步调查

1. 把 `truth/cache/export` 三层写入 `07-personal-memory-minimal-workflow.md` 的检索/索引部分。
2. 为 `evidence_packet` 写一页个人版文件夹约定，不实现代码。
3. 为医疗/财务/法律/账号安全候选定义统一 `citation_refs` 最小字段。
4. 调查是否需要把 `source_native label` 与 `personal_semantic label` 纳入现有标签向量，而不是只在邮件域使用。
