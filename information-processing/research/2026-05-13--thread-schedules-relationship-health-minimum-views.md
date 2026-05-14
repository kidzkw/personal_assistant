# 2026-05-13 -- 邮件线程、财务周期、关系实体与医疗最小视图补强

运行时间：2026-05-13T11:20:35-04:00

## 本轮研究问题

上一轮已经确认了多维标签、不可变证据层、sidecar、provenance、review gate、字段级 authority/merge policy、append-only 日志等基础方向。本轮只寻找能进一步改变信息架构的增量，重点放在邮件/生活行政、财务/订阅、关系/人物、医疗/健康和检索权限。

## 已检查来源与发现

### 1. HL7 PHR：医疗不应只存“医疗文档”

来源：

- https://build.fhir.org/ig/HL7/personal-health-record-format-ig/en/datamodel.html
- https://github.com/HL7/personal-health-record-format-ig/

发现：HL7 Personal Health Record 草案把 PHR 建在 FHIR 数据模型上，覆盖临床、患者自报、设备/健身/营养等来源。它列出约 36 类个人可收到或导出的资源，比完整 FHIR 的 120+ 资源小，但仍超过本项目 MVP。建议只借鉴命名与边界，裁成个人数据库最小医疗视图：`Patient`、`RelatedPerson`、`Practitioner`、`Encounter`、`Appointment`、`Condition`、`Observation`、`DiagnosticReport`、`MedicationStatement`、`Immunization`、`Procedure`、`AllergyIntolerance`、`DocumentReference`、`Claim/Coverage`、`Device`、`Provenance`。

为什么重要：只存 OCR 文档很难回答“某项化验趋势”“某次就诊对应哪些药和账单”“这个症状从什么时候开始”。完整 FHIR 又太重，因此应采用 FHIR-inspired 最小视图，而不是实现完整 EHR。

风险/取舍：医疗对象默认 `claim_state=candidate`、`review_required=true`、`sync_permission=local_only`。系统只做归档、时间线、检索和就诊准备，不做诊断、用药建议或理赔自动决策。

### 2. Notmuch / afew：邮件应区分 message 标签与 thread 标签

来源：

- https://notmuchmail.org/initial_tagging/
- https://notmuchmail.org/doc/latest/man1/notmuch-search.html
- https://notmuchmail.org/special-tags/
- https://github.com/afewmail/afew

发现：Notmuch 常见策略是先给新邮件临时 `new` 标签，再由 post-processing 规则转成 inbox/unread 或其他标签。afew 支持初始标签、基于 header/Maildir folder 的规则、spam/killed thread、邮件列表标签、发件人自动归档、dry-run，并支持标签传播到整个 thread。Notmuch 搜索以 thread 为展示单元，但可以输出 thread/message/file/tag；同一 message 还可能有多个文件副本。

为什么重要：邮箱里的账单、安全通知、医生预约、保险 claim 经常跨多封邮件。个人数据库应分为 `email_message`（原始 MIME/message-id/header/hash）、`email_thread`（主题、参与者、时间范围、聚合标签）、`email_attachment`（PDF/图片/ICS/CSV 证据资产）、`derived_items`（bill、receipt、deadline、account_notice、security_notice、contact_update、task、event）。

风险/取舍：thread sensitivity 应等于子项最高敏感度，但检索时仍按 message/attachment 做权限裁剪。thread 标签可从 message 聚合，但不得反向覆盖单封 message 的来源事实。

### 3. Actual / Firefly III / Reddit：财务要分离 evidence、candidate、transaction、schedule

来源：

- https://www.actualbudget.com/docs/schedules/
- https://www.actualbudget.com/docs/tour/rules/
- https://docs.firefly-iii.org/explanation/more-information/architecture/
- https://docs.firefly-iii.org/how-to/firefly-iii/finances/subscriptions/
- https://docs.firefly-iii.org/how-to/firefly-iii/finances/recurring/
- https://www.reddit.com/r/selfhosted/comments/1qwktl1/any_selfhosted_budget_tracking_receipt_tracking/

发现：Actual 的 schedules 支持自动/手动入账、近似金额或范围、未来显示窗口、从历史交易找 recurring pattern、用 rules 自动分类。Firefly III 拆分 transaction group / journal / transaction，并把 subscription 与 recurring transaction 区分。Reddit 讨论指出自托管预算工具不少，难点是 receipt OCR 与 line-item extraction，常见现实做法是 Paperless-ngx + 财务工具 + 人工确认/脚本桥接。

为什么重要：第一版不应承诺“收据照片自动生成准确交易明细”。更稳的结构是 `financial_evidence`、`finance_item_candidate`、`transaction`、`subscription_or_bill_schedule`、`payment_deadline`、`reconciliation_link`。

风险/取舍：收据 line item 默认低置信候选；账单总额、付款截止日可更早进入可用视图。税务、保险、贷款、投资资料默认只做归档和检索；任何金额汇总都必须带 evidence_refs 与 review_state。

### 4. Monica：关系数据不是普通 memory，而是 people/contact sheet + interaction log

来源：

- https://github.com/monicahq/monica
- https://www.monicahq.com/api/relationships

发现：Monica 将个人关系管理拆成 contacts、relationships、reminders、birthday reminders、notes、how-you-met、activities、tasks、addresses、contact fields、photos、documents、journal entries、multiple vaults/labels。关系 API 把关系建模为“primary contact is [relationship type] of secondary contact”，即有方向、有类型的边。

为什么重要：朋友、家人、生日、上次联系、礼物、共同回忆、家庭历史、敏感边界不应混在普通 memory 中。建议拆为 `person_profile`、`relationship_edge`、`interaction`、`relationship_memory`、`relationship_reminder`。

风险/取舍：人际关系错误推断会伤害信任。关系边必须有 `confidence`、`claim_state`、`source_type`、`last_confirmed_at`，默认 `sync_permission=local_only`。

### 5. Basic Memory / Memento MCP：长期知识应拆为 observation + relation + version history

来源：

- https://github.com/basicmachines-co/basic-memory
- https://docs.basicmemory.com/concepts/observations-and-relations
- https://github.com/gannonh/memento-mcp

发现：Basic Memory 用 Markdown frontmatter + observation + relation 的轻量结构，让文件保持人类可读，同时用 SQLite/graph index 做检索。Observation 是单条事实，relation 是带类型的有向链接。Memento MCP 强调 entity、entity type、observations、vector embeddings、complete version history、temporal awareness。

为什么重要：长期层应以 atomic observation 为主，而不是整段 summary。建议加入 `memory_observation`、`entity_relation`、`memory_version`，支持 `supersedes`、`derived_from`、`conflicts_with`。

风险/取舍：Observation 过细会制造噪声。需要 review gate、retention_class、domain-specific extraction budget。

### 6. Immich / PhotoPrism / Reddit：去重不是删除，而是 duplicate cluster

来源：

- https://docs.immich.app/features/duplicates-utility/
- https://docs.photoprism.app/user-guide/library/metadata/
- https://www.reddit.com/r/selfhosted/comments/1sdx0jn/is_there_an_immich_for_documents/

发现：Immich duplicate utility 偏向保留大文件和 EXIF 更完整的资产，并允许把多个保留项组成 stack；删除前由用户 review；重复组的 album/favorite/rating/description 等元数据会合并/同步到保留资产。PhotoPrism 强调 originals 与 storage/cache/sidecar 分离。Reddit 文档管理讨论显示，用户仍需要“像文件夹”的视图，同时希望 OCR、多用户私有空间、原文件不被修改。

为什么重要：照片/文档去重应产生 `duplicate_group_id`、`representative_asset_id`、`keep_reason`、`duplicate_review_state`、`metadata_merge_policy`、`stack_members`，而不是自动删除。`original_path`、`display_folder`、`logical_collection` 应分离。

风险/取舍：自动同步 metadata 可能扩散错误 caption/人脸/GPS/文档类型。高敏感标签默认不自动合并，除非人工确认。

## 推荐 category / label 变更

新增或明确这些通用标签维度：

- `scope`: `asset | message | thread | attachment | chunk | observation | relation | schedule | transaction | event | task`
- `aggregation_level`: `atomic | thread | session | event_cluster | duplicate_cluster | daily_view`
- `field_cardinality`: `single | multi | set | ordered_list`
- `field_merge_semantics`: `override | append | union | max_sensitivity | manual_only`
- `entity_role`: `subject | counterparty | provider | payer | payee | practitioner | caregiver | dependent | household_member`
- `claim_state`: `candidate | confirmed | disputed | superseded | retracted`
- `validity`: `valid_from | valid_to | last_confirmed_at`
- `review_reason`: `new_ingest | low_confidence | high_sensitivity | conflict | duplicate_cluster | external_sync`

领域标签建议：

- 邮件：`email_message`、`email_thread`、`email_attachment`、`account_notice`、`security_notice`、`bill_notice`、`receipt_notice`、`appointment_notice`、`newsletter_archive`
- 财务：`financial_evidence`、`finance_item_candidate`、`transaction`、`subscription_or_bill_schedule`、`payment_deadline`、`reconciliation_link`、`tax_relevant`、`insurance_relevant`
- 医疗：`medical_document`、`encounter`、`appointment`、`condition`、`observation.lab_result`、`observation.vital`、`observation.symptom`、`medication_statement`、`diagnostic_report`、`claim`、`coverage`
- 关系：`person_profile`、`relationship_edge`、`interaction`、`relationship_memory`、`relationship_reminder`
- 媒体：`duplicate_group`、`representative_asset`、`stack_member`、`display_folder`、`logical_collection`

## Proposed Schema Impact

文档级 schema 提案，不实施迁移：

```yaml
email_thread:
  id:
  source_account_id:
  subject_normalized:
  participants:
  started_at:
  last_message_at:
  message_ids:
  labels:
  sensitivity: "max(child.sensitivity)"
  evidence_refs:
  review_state:

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
  sync_permission: "local_only"

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

## 置信度

中高。邮件、财务、照片、关系、医疗的资料来自成熟项目、官方文档或标准草案，并与前几轮方向一致。低置信部分是 FHIR 最小视图的具体字段数量，因为 PHR 草案仍是 ballot/continuous build，应只借鉴命名与边界。

## 隐私 / 安全考虑

- 邮件 thread 聚合采用最高敏感度上卷，但检索按 message/attachment 权限裁剪。
- 医疗对象默认 `local_only`，默认不进入云同步或外部 LLM；embedding 默认 `none` 或 `summary_only_local`。
- 人际关系边默认候选，不自动永久确认；第三方地址、生日、家庭关系、健康/财务背景默认高敏感。
- 财务金额、税务、保险、贷款、医疗账单默认需要 evidence_refs + review_state。
- 去重不自动删除原件，只生成 duplicate cluster 和建议保留项。

## 下一步调查

- 把 `field_cardinality / field_merge_semantics` 做成跨域表。
- 写“医疗最小视图字段表”：Encounter / Observation / MedicationStatement / DiagnosticReport / Claim。
- 写“邮件 thread ingest 规则”：Message-ID、In-Reply-To、References、附件、账单/安全/预约通知候选项。
- 写“关系图谱安全策略”：哪些关系可自动抽取，哪些必须人工确认，哪些永不外部同步。
