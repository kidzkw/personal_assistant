# 06. Global Workflow（多轮迭代后的个人数据库总流程）

这份文档记录 Echo 当前 personal database / personal assistant information architecture 的最新全局 workflow。它是在多轮研究后，把 Paperless-ngx、Immich/PhotoPrism、Notmuch/afew、FHIR/PHR、Actual/Firefly、Monica、Basic Memory 等参考模式压缩成个人版后的当前方向。

一句话版本：

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

## 0. 当前设计原则

当前系统不是 todo app，也不是单纯 PKM，而是一个 whole-life personal database。

它要长期覆盖：

- 照片、截图、PDF、Markdown、JSON、邮件、附件、聊天导出。
- 健康记录、就诊、化验、处方、症状、保险、医疗账单。
- 财务记录、账单、订阅、税务、保险、收据、付款提醒。
- 人际关系、生日、家庭历史、朋友互动、共同事件。
- 账户、设备、房产、车辆、旅行、生活行政文件。
- 未来音频、wearable streams、Telegram/Hermes、Google sync。

因此底层原则是：

1. 原始证据优先，不把 AI 摘要当成真相。
2. 文件优先，数据库和索引是视图，不是唯一真相。
3. 所有派生对象必须能回拉 evidence。
4. 高风险信息默认 candidate，不自动确认。
5. 检索和同步必须 permission-aware。
6. 标签必须声明作用域，避免 thread、asset、chunk、observation 混在一起。

## 1. File-first Inbox

所有输入先进入文件式 inbox，不急着进入最终 schema。

输入包括：

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

Inbox 的职责：

- 保存原始文件或原始 payload。
- 记录 `ingested_at`、`source_category`、`source_account_id`、`original_path`。
- 打上最低限度标签：`review_state=inbox`、`processing_state=received`。
- 不在此阶段做永久事实确认。

## 2. Immutable Raw Evidence / Assets

进入系统后的原始证据尽量不可变。

核心对象：

```text
raw_evidence
media_asset
email_raw_message
attachment_asset
document_asset
stream_raw_event
```

最小字段：

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

要点：

- `occurred_at` 和 `ingested_at` 必须分开。
- 原件不直接写标签；标签、OCR、caption、修正记录写 sidecar。
- 大文件证据不放进 Git；文本规范、sidecar、索引描述可以 Git 化。

## 3. Sidecar Metadata + Provenance

sidecar 是证据层和结构层之间的桥。

照片优先兼容 XMP；其他文件可使用 `*.meta.json` 或 Markdown frontmatter。

sidecar 需要记录：

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

关键概念：

- `provenance.document`：原始文件从哪里来。
- `provenance.record`：当前标签、OCR、摘要、候选对象是谁生成的。
- `field_origin`：字段来自 EXIF、XMP、OCR、LLM、手工输入、规则等。
- `field_authority`：冲突时谁更可信。
- `field_merge_policy`：覆盖、合并、取最高敏感度、人工确认等。

## 4. Parse / OCR / Chunk / Segment

不同输入类型进入不同切分管线。

```text
Markdown/text -> chunks
PDF -> pages + OCR regions + text chunks
photo/screenshot -> EXIF + OCR + visual labels + thumbnails
email -> message + thread + attachment
chat -> message + thread/session
audio later -> transcript segments + conversation/session
continuous streams later -> stream + event(timestamp, duration, payload)
```

切分后的对象必须带：

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

`scope` 是当前迭代后的关键字段：

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

`aggregation_level` 用来说明这个对象是原子对象还是聚合视图：

```text
atomic
thread
session
event_cluster
duplicate_cluster
daily_view
```

## 5. Scope-aware Candidate Extraction

在 candidate extraction 前，系统应先为可检索内容生成轻量抽象层：

```text
chunks / messages / pages / sessions
 -> contextual_prefix
 -> context_routing_index
 -> sparse keys
```

这层借鉴 Claude/Anthropic 的 contextual retrieval 与 layered memory：常驻上下文只保留路由索引，细节按需加载；chunk 不只以孤立文本进入索引，而是带上它在整篇文档、邮件 thread、医疗报告、账单周期或照片事件中的位置说明。

新增对象：

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

`contextual_prefix` 是检索辅助文本，不是事实真相。它必须可重新生成，并保留 `generated_by`、`generated_at`、`source_prompt_version`。

AI、OCR、规则、文件名解析、邮件 header 解析都只能先生成候选对象。

候选类型：

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

候选对象必须有：

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

重要规则：

- AI 不直接创造 confirmed memory。
- OCR 不直接创造 confirmed transaction。
- 邮件 thread 标签不覆盖单封 message 的事实。
- duplicate cluster 不自动删除任何原件。
- 医疗、财务、法律、关系、账户安全默认需要 review。

## 6. Review Gate

在进入 review gate 之前，高风险候选可以先走一层结构化 verification pass。

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

这层借鉴 DeepSeek-R1 的 self-verification / reflection 和 Claude long-running agent 的 fresh-context evaluator 思路。它不能替代人工确认，只负责提前标出证据不足、冲突、低置信、需要优先 review 的候选。

Review gate 是当前全局 workflow 的核心控制点。

默认进入 review 的内容：

- 医疗、健康、症状、化验、处方。
- 财务、税务、保险、贷款、投资。
- 法律、身份、账户、安全通知。
- 人际关系、家庭关系、第三方隐私。
- 自动生成的长期 memory。
- 自动生成的 entity relation。
- 重复文件删除建议。

通用状态：

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

所有 confirmed 对象都应该保留：

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

审阅后进入长期核心层。这里才是 assistant 日后稳定使用的主对象。

### 7.1 Memory / Knowledge

长期记忆不再等于 summary，而是：

```text
memory_observation
entity_relation
memory_version
```

示例：

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

邮件采用双层结构：

```text
email_message
 -> email_thread
 -> email_attachment
 -> derived_item
```

派生对象包括：

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

thread sensitivity 采用 `max(child.sensitivity)`，但检索时仍按 message/attachment 裁剪权限。

### 7.3 Finance

财务不直接从 OCR 进入 transaction。

推荐结构：

```text
financial_evidence
finance_item_candidate
transaction
subscription_or_bill_schedule
payment_deadline
reconciliation_link
```

`reconciliation_link` 连接证据、候选项、真实交易和周期义务：

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

医疗采用 FHIR-inspired 最小视图，不实现完整 EHR。

最小对象：

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

默认策略：

```text
review_required = true
sync_permission = local_only
embedding_policy = none 或 summary_only_local
evidence_refs = required
```

系统只做归档、时间线、检索、就诊准备，不做诊断、用药或理赔决策。

### 7.5 People / Relationships

关系域独立于普通 memory。

核心对象：

```text
person_profile
relationship_edge
interaction
relationship_memory
relationship_reminder
```

关系边示例：

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

照片和文档 pipeline：

```text
original asset
 -> EXIF/GPS/device/source folder
 -> thumbnail/preview
 -> OCR/caption/visual labels
 -> content hash + perceptual hash
 -> duplicate cluster
 -> event/date/place/person clustering
```

去重对象：

```text
duplicate_group
representative_asset
stack_member
```

重要规则：

- 不自动删除原件。
- 高敏感 metadata（GPS、人脸、医疗/财务文档类型）默认不自动合并。
- `original_path`、`display_folder`、`logical_collection` 分离。

## 8. Entity Graph + Timeline + Indexes

confirmed objects 进入图谱和视图层。

Entity graph 包括：

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

Timeline 包括：

```text
daily_timeline
medical_timeline
finance_timeline
relationship_timeline
travel_timeline
household_timeline
account_security_timeline
```

Indexes 包括：

```text
exact search
date search
metadata filters
FTS / BM25
vector search later
graph lookup
domain-specific indexes
```

Embedding 不是默认全量开启。高敏感内容优先不 embed，或只做本地 summary embedding。

## 9. Permission-aware Retrieval

Assistant 检索时按层级逐步展开：

```text
1. context_routing_index
2. confirmed objects
3. summaries / metadata / graph
4. contextualized chunks / OCR / thread
5. raw evidence pullback
```

检索表示拆成三类：

```text
latent_summary 负责召回
sparse_keys 负责过滤
exact_ref 负责证据回拉
```

这是从 DeepSeek-V3 MLA / sparse attention 得到的结构启发：压缩表示不替代原始证据，稀疏选择后仍要能回拉精确原文。

每一步都检查：

```text
sensitivity
sync_permission
embedding_policy
review_state
claim_state
retention_class
source evidence availability
```

回答高风险问题时，必须能回拉证据：

- PDF 页码。
- OCR region。
- 邮件 message id。
- 附件 hash。
- 照片 asset id。
- 医疗 document reference。
- 财务 reconciliation link。

## 10. Controlled Sync / Actions / Export

Google、Telegram/Hermes、未来移动端都不是底层真相，而是展示层或行动层。

同步前检查：

```text
sync_permission
sensitivity
review_state
claim_state
target_system
field_allowlist
```

典型策略：

```text
task -> 可同步到任务系统
calendar event -> 可同步到日历
daily readable summary -> 可选择同步
medical raw evidence -> 默认 local_only
relationship graph -> 默认 local_only
finance/tax/insurance -> 默认 restricted
```

所有写入、同步、修正、删除建议都应该进入 append-only audit/change log。

## 11. Echo 当前核心流程

Echo 当前 personal database 的主流程是：

```text
evidence/assets
 -> scoped records/chunks/messages/threads/streams
 -> candidate observations/items/relations
 -> reviewed domain objects
 -> entity graph + timelines + retrieval indexes
 -> assistant actions with privacy gates
```

这个流程保留“证据 -> 理解 -> 行动/检索”的骨架，但把重点放在 whole-life personal database 需要的证据保留、审阅门、权限控制、长期对象历史和可回源解释上。

## 12. 当前最高优先级

下一步如果要把设计继续固化，优先写这几张表：

1. `field_cardinality / field_merge_semantics` 跨域表。
2. 医疗最小视图字段表：Encounter / Observation / MedicationStatement / DiagnosticReport / Claim。
3. 邮件 thread ingest 规则：Message-ID / In-Reply-To / References / attachment / derived item。
4. 关系图谱安全策略：哪些关系可自动抽取，哪些必须人工确认，哪些永不外部同步。
5. sidecar 最小 schema：`id/kind/provenance/labels/evidence_refs/field_origin/field_authority/field_merge_policy`。
