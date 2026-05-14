# 07. Personal Memory Minimal Workflow（个人记忆库精简主干）

这份文档把前面多轮 research 里的复杂架构压缩成“个人可维护”的版本。

目标不是做企业级 EHR、财务系统、CRM、数据仓库或通用 AI 平台，而是做一个长期好用的个人记忆库：能保存证据，能帮我找回事情，能提醒我该处理什么，能在需要时回到原始来源。

## 1. 当前核心判断

个人记忆库最重要的不是 schema 多完整，而是这几件事稳定：

1. 原始资料别丢。
2. 每条重要信息知道从哪里来。
3. 自动提取的东西先当候选，不要直接当事实。
4. 搜索时先找摘要和标签，不够再回到原文/原图/原邮件。
5. 医疗、财务、法律、关系、账号安全默认更谨慎。
6. 复杂标准只借鉴，不照搬。

当前主干：

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

## 2. 要记的信息点

### 2.1 日常记忆

包括每日重要事情、决定、想法、偏好、习惯变化、项目进展、以后值得问 assistant 的事实。

最低字段：

```yaml
type: memory
title:
summary:
occurred_at:
source_ref:
sensitivity:
review_state:
```

### 2.2 文件和证据

包括 PDF、Markdown、JSON 导出、截图、照片、扫描件、医疗文件、账单、保险、税务、合同、旅行文件、旧硬盘/旧邮箱/旧聊天导出的原始材料。

最低字段：

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

原则：原件优先保存；AI 摘要不是原件。

### 2.3 照片 / 截图 / 媒体

包括所有照片、截图、文档照片、EXIF 时间、GPS、设备、原始文件夹、OCR 文本、简单 caption、重复候选、事件聚类。

第一版最低处理：

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

暂不复杂化：

- 不急着做人脸库。
- 不自动合并/删除重复照片。
- GPS 和人脸默认敏感，不随便同步。

### 2.4 医疗 / 健康

包括医生就诊、化验单、处方、药物、症状、体检、保险理赔、医疗账单。

个人版只需要五类：

```text
medical_document
doctor_visit
lab_result
medication
symptom_note
```

最低字段：

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

暂不复杂化：

- 不实现完整 FHIR。
- 不自动诊断。
- 不自动给用药建议。
- 化验值可以结构化，但必须能回到原 PDF/截图。

### 2.5 财务 / 账单 / 生活行政

包括账单、收据、订阅、税务、保险、贷款、付款提醒、报销、银行/信用卡记录。

个人版对象：

```text
financial_document
bill_or_subscription
receipt
payment_deadline
finance_candidate
```

最低字段：

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

暂不复杂化：

- 不做完整复式记账。
- OCR 金额默认 candidate。
- 不自动做财务决策或投资建议。

### 2.6 邮件 / 账号 / 安全通知

包括旧邮箱和新邮箱、附件、账单、收据、验证码、安全提醒、账号变更、旅行预订、预约提醒。

个人版处理：

```text
email_message
email_thread_summary
attachment_asset
derived_notice
```

最低字段：

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

注意：

- thread 只是视图，不能覆盖单封邮件的事实。
- 附件要变成独立 evidence。
- 安全通知、账单、医疗邮件默认需要 review。

### 2.7 人 / 关系 / 生日 / 共同经历

包括朋友、家人、医生、同事、服务商、生日、联系方式、重要关系、最近互动、共同事件、要跟进的承诺。

个人版对象：

```text
person
interaction
relationship_note
reminder
```

最低字段：

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

暂不复杂化：

- 不急着做完整关系图谱。
- 不自动确认敏感关系。
- 第三方隐私默认 local_only。

### 2.8 任务 / 事件 / 提醒

包括待办、承诺、截止日期、预约、账单 due date、生日、旅行安排。

个人版对象：

```text
task
event
reminder
```

最低字段：

```yaml
title:
kind:
due_at:
status:
source_ref:
sync_permission:
review_state:
```

可以同步普通任务和普通日程。默认不同步医疗细节、财务细节、关系图谱和原始敏感文件。

## 3. 信息处理主流程

### Step 1: 收进 inbox

所有东西先进入 inbox，不要求一开始分类完美。

```text
photo / screenshot / pdf / markdown / json / email / attachment / chat export / note
 -> inbox
```

inbox 最少记录：

```yaml
id:
source_category:
original_path:
ingested_at:
basic_type:
review_state: inbox
```

### Step 2: 保存原始证据

进入系统后，原始文件尽量不改。

```text
inbox item
 -> raw_evidence / media_asset / email_message / attachment_asset
```

最重要的是有 hash、路径、来源、时间、敏感级别。

同时要区分四层：

```text
truth   = 原始文件、sidecar、confirmed memory objects
working = 可读整理页、wiki brief、就诊准备摘要、人工修正说明
cache   = OCR、thumbnail、FTS/BM25、embedding、graph view
export  = Markdown/HTML/CSV/JSON 导出包
```

个人版原则：

- `truth` 才是真相层。
- `working` 是帮助人理解和 review 的整理层，不替代原件。
- `cache` 可以删除重建，必须知道从哪些文件/对象生成。
- `export` 默认字段白名单和脱敏，不直接带出医疗、财务、关系、账号安全原件。

第一版最低字段：

```yaml
storage_layer: truth | working | cache | export
artifact_role: original | sidecar | extracted_text | ocr | preview | redacted | wiki_brief | index_record | embedding
built_from_refs:
generated_at:
review_state:
```

### Step 3: 轻量打标签

个人版先保留这些：

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

这是当前推荐的“个人版标签向量”。够用了，别再往里面塞太多花活。

来源系统自己的文件夹、标签、相册、thread、收藏夹不要混进个人语义标签。它们单独作为 `source_membership`：

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

这样同一张照片、同一封邮件、同一份 PDF 可以属于多个来源容器，但长期语义只确认一次。

### Step 4: 解析 / OCR / 切块

只在需要时做解析。

```text
PDF -> text + pages
photo/screenshot -> EXIF + OCR + thumbnail
email -> message + attachments
markdown/text -> chunks
json export -> source-specific records
audio later -> transcript segments
```

切块原则：

- 文本按段落/标题切。
- PDF 按页和章节切。
- 邮件按 message 和 attachment 切。
- 照片不强行切，只保留 metadata/OCR/caption。
- 未来音频按 transcript segment + session。

### Step 5: 提取候选

AI/OCR/规则只生成候选，不直接生成真相。

候选类型：

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

候选最低字段：

```yaml
candidate_type:
summary:
extracted_values:
confidence:
evidence_refs:
review_state: candidate
sensitivity:
```

高风险候选还需要 `citation_refs`，至少能回到文件、页码、message id 或截图/OCR 片段：

```yaml
citation_refs:
  evidence_ref:
  artifact_ref:
  locator:
  excerpt:
  extraction_method:
  confidence:
```

医疗、财务、法律、账号安全、关系类候选如果没有 citation，只能留在 candidate，不能 confirmed。

### Step 6: Review

个人版 review 不需要复杂工作流，只要分清：

```text
confirm
correct
ignore
archive
```

默认需要 review：

- 医疗。
- 财务。
- 法律。
- 账号安全。
- 人际关系。
- 自动生成的长期记忆。
- 删除/合并建议。

可以低 review 或自动归档：

- 普通照片 caption。
- 普通文件 OCR。
- 无行动项的营销邮件。
- 明确低价值噪声。

### Step 6.5: PS 总管和 agent 串行接力

agent workflow 只作为信息处理角色，不是无限自治系统。

个人版最小分工：

```text
总管 = 唯一总调度层，负责分类、分派、全局 work log、冲突记录、下一步排队
小秘 = 长期领域 steward，例如 health_xiaomi / finance_xiaomi / email_admin_xiaomi / relationship_xiaomi
processing_agent = 短生命周期处理者，只处理一个 evidence packet / object brief / update check
audit_agent = 短生命周期审计者，只检查 processing_result 的证据、引用、边界和风险
proposal_agent = 短生命周期提案者，只生成 review_result / update_proposal / no_action
```

核心约束：每个小秘同一时间只能有一条 active child chain。上一条 processing/audit/proposal chain 没有被小秘汇总、写入 work log、report 给总管之前，不允许开始下一条 chain。

个人版最小字段：

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

短生命周期 agent 的输出只能是结构化中间结果：

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

注意：

- processing/audit/proposal agent 都不直接写 confirmed memory 或 truth layer。
- 不保存短生命周期 agent 的长上下文，只保存结构化结果、citation、baton 和 work log 状态。
- 小秘负责生成 `domain_event_summary_report` 给总管；总管只根据 report 更新 work log、决定 `next_spawn_allowed`。
- 医疗、财务、法律、账号安全、关系信息默认 `local_only` 且 `review_required`。
- 如果结果证据不足或冲突，状态写 `blocked`，不要静默继续下一棒。

### Step 7: 形成个人记忆对象

确认后进入长期层：

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

个人版记忆对象最少要有：

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

### Step 8: 检索 / 使用

检索顺序保持简单：

```text
1. 关键词 / 日期 / 人 / 类型过滤
2. 摘要和 confirmed memory
3. OCR / 邮件正文 / 文档 chunk
4. 原始证据回拉
```

第一版优先精确搜索、日期搜索、标签过滤、本地全文搜索、证据回拉。以后再加 vector search、routing index、复杂 graph traversal。

## 4. 哪些研究建议应该降级

### 4.1 FHIR

保留思想：医疗对象要能回到证据；就诊、化验、用药、症状要分开。

个人版做法：

```text
medical_document / doctor_visit / lab_result / medication / symptom_note
```

暂不做完整 FHIR resource graph。

### 4.2 Perkeep object_anchor / attribute_claim

保留思想：长期对象会变化，历史不要直接覆盖。

个人版做法：第一版只保留 `updated_at`、`previous_values` 或简单 `change_log`。只有 person/account/medical/finance 这种高价值对象，未来再考虑 claim 模型。

### 4.3 source_snapshot / import_run / parse_error_record

保留思想：大批量导入要知道“哪批数据进来了，哪些失败了”。

个人版做法：

```yaml
import_batch:
  id:
  source_name:
  imported_at:
  item_count:
  error_count:
  notes:
```

解析失败第一版可以是简单列表：

```yaml
failed_items:
  path:
  reason:
  retry_later:
```

不用一开始做完整数据管线对象。

### 4.4 data warehouse / exploratory index

保留思想：批量检查和搜索需要一个本地索引。

个人版做法：用本地 SQLite/FTS 或轻量索引即可，不把它当正式事实库，不做分享视图。

### 4.5 关系图谱

保留思想：人和互动很重要。

个人版做法：

```text
person + interaction + reminder
```

暂不做复杂 graph edge、consent ontology、visibility scope 矩阵。敏感关系靠 review 和 local_only 控制。

## 5. 当前推荐最小目录/对象

如果现在要把主干落成文件/数据库概念，优先这些：

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

高价值证据可以增加一个轻量 `evidence_packet`，不是所有文件都必须有：

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

优先用于医疗 PDF、财务/税务/保险文件、合同、账号安全截图、重要行政文件。

这已经能覆盖大多数个人记忆需求。

暂不进入主干：

```text
full FHIR resources
full accounting ledger
full CRM graph
claim-fold object store
multi-device sync protocol
general data warehouse
automated medical/financial decisions
```

## 6. 当前最重要的信息点优先级

P0，必须保留：

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

P1，强烈建议：

- `entity_refs`
- `confidence`
- `original_path`
- `mime_type`
- `extracted_values`
- `change_log`
- `import_batch_id`
- `interpretation_level`
- `temporal_anchor` for interval/stream data

P2，以后再说：

- `field_contract`
- `object_anchor`
- `attribute_claim`
- `context_routing_index`
- `candidate_verification`
- `local_data_warehouse_view`
- full domain-specific schemas

## 7. 一句话版本

个人记忆库的第一版不需要像一个小型互联网公司后台。

它需要像一个很可靠的私人档案员：东西先进来，原件别丢，来源说清楚，AI 只提建议，重要事实你确认，之后能按时间、人、主题、文件、证据找回来。
