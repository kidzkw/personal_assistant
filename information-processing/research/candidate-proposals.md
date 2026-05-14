# Candidate Proposals（持续更新）

更新时间：2026-05-13

> 目的：把每次 research run 的“可落地结构建议”压缩成少量候选项，便于后续逐步固化为正式 IA/目录约定/元数据 schema（仅文档，不做代码实现）。

## P0（强烈建议纳入当前结构）

### P0-1：统一元数据为“多维标签向量”（替代单一 category）

- **发现来源**：Paperless-ngx 的 correspondents / document types / tags 多轴体系；Notmuch 的 tag-first 收件箱；Echo 的 system labels + semantic labels + derived labels 分层。
- **要点**：
  - `domain / source_category / media_type / semantic_type / counterparty / actionability / sensitivity / temporal / confidence / review_state / retention_class / criticality / sync_permission`
  - 强制区分 `occurred_at` 与 `ingested_at`（Paperless 的 date created vs date added 模式）。
- **收益**：跨域（照片/邮件/健康/财务）一致；便于长期演进与检索过滤。
- **schema 影响（提案级）**：新增 `labels` 结构；任何派生对象必须带 `evidence_refs`。
- **风险**：维度过多会导致人工维护成本上升；需要默认值与“逐步补全”策略（INBOX 审阅门）。

### P0-2：证据层不可变 + sidecar 元数据为一等公民（照片优先 XMP）

- **发现来源**：Immich XMP sidecar 读写与作业；PhotoPrism 的 metadata 合并与 YAML sidecar 导出。
- **要点**：
  - 原文件（evidence/assets）尽量不修改；
  - 元数据（标签、描述、OCR 引用、敏感级别、审阅状态、去重信息）写 sidecar（照片用 XMP；其他用 `*.meta.json`）。
- **收益**：降低 DB lock-in；长期迁移/工具互操作更强。
- **schema 影响（提案级）**：定义 sidecar 的最小键集合（`id/kind/provenance/timestamps/labels/evidence_refs`）。
- **风险**：sidecar 与未来索引/缓存的一致性与冲突策略需要先写清楚。

### P0-3：统一 `review_state=inbox` 审阅门（跨域通用）

- **发现来源**：Paperless-ngx 的 INBOX 标签工作流；社区经验“自动化只做到建议，最终要人工确认”。
- **要点**：
  - 默认进入 `inbox`；
  - 自动抽取只产生“候选派生对象”（task/event/fact），在 `reviewed` 前不进入核心记忆/关键索引。
- **收益**：长期正确性、降低噪声与误归类；特别适合医疗/财务。
- **风险**：需要明确“多长时间不审阅的处理策略”（提醒/降级/归档）。

### P0-4：把“溯源/审计（provenance）”提升为一等字段（区分文档溯源 vs 记录溯源）

- **发现来源**：FHIR `DocumentReference` 强调“被引用文档的溯源”与“引用记录本身的溯源”是两套信息；W3C PROV（entity/activity/agent）；以及 Paperless 的管线阶段差异带来的可解释性需求。
- **要点**：
  - 在 sidecar/frontmatter 的最小 schema 中加入 `provenance.document` 与 `provenance.record`；
  - 抽取结论类条目新增 `claim_state`（candidate/confirmed/disputed/superseded/retracted）与 `validity`（valid_from/valid_to/last_confirmed_at）；
  - 任何派生对象强制 `evidence_refs`（可回溯到文件 hash + 页码/区域/消息 id 等）。
- **收益**：医疗/法律/财务场景可解释、可纠错；长期维护不会“忘了这条信息怎么来的”。
- **schema 影响（提案级）**：sidecar/frontmatter 最小字段集需要扩展；并明确 provenance 字段也受 `sensitivity/sync_permission` 约束。
- **风险**：provenance 本身可能泄露敏感元信息（路径/机构/邮箱/设备名）；需要默认最小化与脱敏策略。

### P0-5：字段级“权威/合并语义”显式化（尤其是照片 XMP 的别名优先级与写回规则）

- **发现来源**：PhotoPrism 对 XMP 的两条解析路径与 sidecar reader 限制（embedded 经 ExifTool vs `.xmp` PoC reader）；Immich 对 XMP sidecar 的“合并写回（merge）”与字段优先级顺序、命名规则、DISCOVER/SYNC 作业。
- **要点**：
  - 为关键元数据字段补齐三件事：`field_origin`（来自 embedded/sidecar/OCR/手工/抽取…）、`field_authority`（冲突时谁是默认真相）、`field_merge_policy`（覆盖/合并/优先级列表）；
  - 照片域把“逻辑字段 → XMP/EXIF/IPTC 别名优先级列表 → 写回白名单”写成一张表，并明确只写回跨工具通用字段（描述/评分/标签/时间/位置等），敏感字段（GPS/人脸）默认不写回/不同步；
  - 写回需要显式权限与失败可观测性（避免 read-only 外部库下 silent fail）。
- **收益**：避免未来导入/编辑/多工具混用导致的“不可解释覆盖”；把冲突从实现层提前到 IA 规范层。
- **schema 影响（提案级）**：sidecar/frontmatter 最小 schema 需新增 `field_origin/field_authority/field_merge_policy`（可按对象或按字段字典表达）。
- **风险**：字段级规则会增加复杂度；需要从少量高价值字段（photo_datetime/location/tags/description 等）开始逐步扩展。

## P1（建议作为下一轮研究/提案深化）

### P1-1：连续流统一为 `stream + event(timestamp,duration,payload)` 原子

- **发现来源**：ActivityWatch buckets/events/heartbeats 数据模型。
- **要点**：
  - 每个来源一个 stream/bucket；
  - heartbeat merge 用于降噪；
  - 后续再派生 session、daily timeline、memories。
- **收益**：为未来音频/可穿戴/屏幕活动打基础；切段模型统一。
- **风险**：早做会引入复杂度；可先写“未来兼容字段”但不落地数据量。

### P1-2：医疗域采用“FHIR 资源命名 + 证据挂载 + 人类可读解释层”

- **发现来源**：Fasten Health（PHR 聚合，FHIR/SMART）。
- **要点**：
  - Encounter/Observation/Medication/Condition/Procedure/Coverage/Claim；
  - 每个资源挂载 evidence（PDF/截图/邮件）；
  - 解释层：把编码（LOINC/SNOMED 等）翻译成可读描述（先作为文档约定，不做自动化）。
- **收益**：医疗信息可组合与可追溯；便于生成就医时间线与问题清单。
- **风险**：FHIR 粒度过细会拖慢落地；需要定义“最小字段集”。

### P1-3：财务域拆分“证据 vs 结构化条目 vs 规则/周期”

- **发现来源**：Firefly III（交易对象分层、规则、recurring）；Actual（local-first）。
- **要点**：
  - 票据/账单/邮件作为 evidence；
  - transaction/subscription/deadline 作为结构化条目；
  - recurring 是一等对象，驱动任务/提醒派生。
- **收益**：从“搜索文档找账单”升级为“结构化提醒与对账”。
- **风险**：跨银行/信用卡导入格式差异大；先文档化 schema 与字段命名即可。

### P1-4：将“管线规则”写成 Paperless 风格的 `triggers + filters + actions` 说明书（stage-aware）

- **发现来源**：Paperless-ngx Workflows（触发器/动作、顺序执行、覆盖/合并语义、定时触发）；以及其社区/issue 对“OCR 尚未完成时字段不可用”的提醒。
- **要点**：
  - 规则显式标注 `pipeline_stage`（ingest/parse/ocr/extract/review/final），并列出该阶段可用字段；
  - 定义单值字段覆盖 vs 多值字段合并的固定语义；
  - 规则命中后的元数据变更写入审计记录（仅文档约定）。
- **收益**：可解释、可调试、可长期维护；为未来实现自动化执行器/同步器预留稳定接口。
- **风险**：文档写得太抽象会失效；需要用“跨域样例”（邮件账单/医疗化验单/截图验证码/照片事件）来校准。

### P1-5：引入“append-only 变更日志 + 资产引用（checksum-in-URL）”作为未来同步/审计格式预案（Receipts 风格）

- **发现来源**：Receipts Space / Receipts App 的 File-over-App 数据格式：`info.json` + `transactions/`（append-only JSON/JSONL，header 含 checksum/可选链式哈希）+ `assets/`（二进制附件，引用携带 checksum/size/mime/name）。
- **要点**：
  - 将“元数据变更/纠错/撤销”优先落在 **格式** 层：每次变更追加一条 log entry（而不是覆盖写）；
  - 资产（PDF/图片/原始附件）用 `asset://` 引用统一表达，引用内嵌 checksum 与大小，实现“引用即校验”；
  - 预留 `clientId/did` 与 LWW（Lamport clock）语义，但当前阶段只作为文档约定，不落地同步器。
- **收益**：天然审计轨迹；未来跨设备/外部硬盘/同步盘更稳；导出/迁移时不依赖单一 DB。
- **风险**：格式一旦确定会影响后续工具链；需要先用 1-2 个域（例如 receipts/bills）做最小试点规范。
## 2026-05-13 11:20 EDT 新增候选项

### P0-6：标签必须显式声明 `scope` 与 `aggregation_level`

- **发现来源**：Notmuch/afew 的 message vs thread 标签传播；Basic Memory 的 observation/relation 原子化；Immich duplicate groups；Actual/Firefly 的 schedule/transaction 分离。
- **要点**：
  - 新增 `scope`: `asset | message | thread | attachment | chunk | observation | relation | schedule | transaction | event | task`。
  - 新增 `aggregation_level`: `atomic | thread | session | event_cluster | duplicate_cluster | daily_view`。
  - 规则和字段变更必须声明作用域，避免“线程标签覆盖单封邮件事实”或“duplicate group 标签污染原始资产”。
- **收益**：跨邮件、聊天、照片、文档、财务、医疗的标签语义更稳定；方便权限裁剪和证据回拉。
- **schema 影响（提案级）**：所有 `labels` 增加 `scope`；所有 rule/action 增加 `target_scope`。
- **风险**：字段变多；需要默认值，否则早期手工维护成本上升。

### P0-7：长期记忆采用 atomic `memory_observation` + typed `entity_relation` + version history

- **发现来源**：Basic Memory 的 observations/relations；Memento MCP 的 entity/observation/version history；既有 provenance/claim_state 提案。
- **要点**：
  - `memory` 不直接等同 summary；长期层最小单位应是单条事实/偏好/经历/决定/风险。
  - `entity_relation` 表示 person/place/account/project/device/document/event 之间的 typed edge。
  - 每次抽取、合并、人工修改、撤回保留版本与 `supersedes/conflicts_with/derived_from`。
- **收益**：减少“一个 summary 里混入多个事实导致不可纠错”的问题；更适合 5+ 年维护。
- **schema 影响（提案级）**：新增 `memory_observation`、`entity_relation`、`memory_version` 或等价 sidecar 结构。
- **风险**：原子化过细会制造噪声；需要 extraction budget 与 review gate。

### P1-6：邮件/生活行政采用 `email_message -> email_thread -> attachment -> derived_item` 分层

- **发现来源**：Notmuch 初始标签、thread 搜索/输出、special tags；afew 的自动标签与 thread 标签传播。
- **要点**：
  - `email_message` 保存 Message-ID、headers、MIME、hash、raw evidence。
  - `email_thread` 保存参与者、主题、时间范围、聚合标签、最高敏感度。
  - `email_attachment` 保存 PDF/图片/ICS/CSV 等资产引用。
  - 派生 `bill/receipt/deadline/account_notice/security_notice/contact_update/task/event`。
- **收益**：旧邮箱与新邮箱都能以 thread 为人类可读视图，同时保留 message 级证据。
- **风险**：thread 聚合会扩大敏感范围；必须采用 max(child.sensitivity) 并按 message/attachment 裁剪权限。

### P1-7：财务增加 `reconciliation_link`，分离证据、候选项、真实交易与周期义务

- **发现来源**：Actual schedules/rules；Firefly III transaction group/journal/transaction、subscriptions、recurring transactions；Reddit 对 receipt OCR/line-item extraction 难点的讨论。
- **要点**：
  - `financial_evidence`：账单 PDF、收据照片、邮件、CSV、银行导出。
  - `finance_item_candidate`：OCR/邮件/规则抽取候选金额、商户、due date。
  - `transaction`：人工确认或可靠导入后的真实记账事件。
  - `subscription_or_bill_schedule`：周期义务/预期支出。
  - `reconciliation_link`：证据、候选项、交易、schedule 的匹配关系与置信度。
- **收益**：避免把 OCR 候选误当成财务事实；支持账单提醒和后续对账。
- **风险**：完整财务模型容易过重；第一版应只做 evidence/candidate/deadline/reconciliation，暂不做自动决策。

### P1-8：关系域拆为 `person_profile`、`relationship_edge`、`interaction`、`relationship_reminder`

- **发现来源**：Monica personal CRM 的 contacts、relationships、activities、reminders、birthday reminders、notes、documents/photos、multiple vaults/labels。
- **要点**：
  - `person_profile`：姓名、别名、生日、联系方式、地址、来源、敏感级别。
  - `relationship_edge`：有方向、有类型、有置信度、有有效期的关系边。
  - `interaction`：见面、电话、邮件、聊天、礼物、帮助、共同事件等日志。
  - `relationship_reminder`：生日、纪念日、多久没联系、承诺事项。
- **收益**：全生活数据库需要长期维护人际背景，不能只作为普通 memory/tag。
- **风险**：第三方隐私高；关系边必须默认候选、local_only，敏感字段禁止默认同步。

### P1-9：医疗采用 FHIR-inspired 最小视图，而不是完整 FHIR 或纯 OCR 文档

- **发现来源**：HL7 Personal Health Record Format IG 的 PHR data model；Fasten Health 的 self-hosted PHR/FHIR 方向。
- **要点**：
  - 最小视图建议覆盖 `Patient/RelatedPerson/Practitioner/Encounter/Appointment/Condition/Observation/DiagnosticReport/MedicationStatement/Immunization/Procedure/AllergyIntolerance/DocumentReference/Claim/Coverage/Device/Provenance`。
  - `Observation` 必须细分 `lab_result/vital/symptom/wearable/patient_reported`。
  - 每个医疗对象默认 evidence-backed、local_only、review_required。
- **收益**：能回答就诊时间线、化验趋势、处方历史、保险/账单关联，而不需要实现完整 EHR。
- **风险**：医疗自动化风险高；仅用于归档、检索、就诊准备，不做诊断/用药/理赔决策。

### P1-10：媒体/文档去重以 duplicate cluster 为对象，不自动删除原件

- **发现来源**：Immich duplicate utility 的 review、keep preselection、metadata sync/stack；PhotoPrism originals/storage/sidecar 分离；Reddit 对“Immich for documents”的文件夹视图和原件不修改需求。
- **要点**：
  - 新增 `duplicate_group_id / representative_asset_id / keep_reason / duplicate_review_state / stack_members`。
  - `original_path`、`display_folder`、`logical_collection` 分离。
  - 高敏感 metadata（GPS、人脸、医疗/财务文档类型）默认不自动合并。
- **收益**：照片、截图、PDF、附件可以统一去重，同时保留原始证据和用户可理解视图。
- **风险**：自动合并 caption/标签可能扩散错误；默认只生成建议，人工确认后合并。

## 2026-05-13 12:00 EDT 新增候选项（Claude / DeepSeek 信息抽象）

### P0-8：新增 `context_routing_index`，把“常驻上下文”压成路由索引

- **发现来源**：Claude Code layered memory issue（slim index + topic files + semantic search）；Anthropic Skills 的按需加载说明书模式。
- **要点**：
  - 常驻层只放主题、关键词、状态、敏感级别、detail_refs，不放完整记忆。
  - 每个 topic/domain/entity 可有按需加载的 detail file 或 indexed object。
  - index 条目本身也要有 `sensitivity`、`sync_permission`、`redacted_title`。
- **收益**：避免 personal database 变成巨大 always-loaded memory；更适合 5+ 年使用。
- **schema 影响（提案级）**：新增 `context_routing_index`，并在检索流程中先 route 再 pull evidence/detail。
- **风险**：索引过粗会漏召回；过细会泄露敏感主题或重新膨胀。

### P0-9：chunk 层增加 `contextual_prefix`，支持 Contextual Retrieval

- **发现来源**：Anthropic Contextual Retrieval / Claude Cookbooks：给 chunk 加文档级短上下文，再用于 embedding/BM25/reranking。
- **要点**：
  - 每个 chunk 保留 raw text，同时生成检索专用 `contextual_prefix`。
  - `contextual_prefix` 必须带 `generated_by/generated_at/source_prompt_version`，可重新生成。
  - 高敏感 chunk 可只做 local BM25 或 redacted prefix，不送外部 embedding。
- **收益**：减少 chunk 脱离文档/邮件 thread/医疗报告/账单周期后检索失败。
- **schema 影响（提案级）**：`content_chunk` 新增 `contextual_prefix/document_outline_ref/section_path/bm25_text`。
- **风险**：LLM prefix 可能引入偏差，不能当作事实层。

### P1-11：新增 `assistant_handoff` 与 `context_event_log`，把 AI 工作状态也作为过程记录

- **发现来源**：Claude Code persistent memory / compaction issues、Anthropic cwc-long-running-agents、MCP Memory Keeper。
- **要点**：
  - 在 stop/pre-compact/manual checkpoint 时写 handoff。
  - 记录 working_goal、decisions、open_questions、evidence_seen、candidate_objects_created、review_items_pending、next_actions。
  - 与 append-only audit/change log 区分：handoff 是工作状态，audit 是可追责事件。
- **收益**：长任务、自动化、并行 agent、跨 session 都能恢复上下文，不依赖聊天窗口。
- **风险**：日志膨胀；handoff 可能包含敏感路径/偏好/项目状态，需要 sensitivity 标注。

### P1-12：新增 `candidate_verification` pass，高风险候选先自检再进入 review

- **发现来源**：DeepSeek-R1 强调 self-verification/reflection；Claude long-running agent 的 evaluator/fresh-context review 模式。
- **要点**：
  - candidate extraction 后增加结构化 verification outcome。
  - 字段包括 `checked_against_evidence_refs`、`contradiction_found`、`missing_evidence`、`confidence_delta`、`recommended_review_state`。
  - 不保存隐藏推理链，只保存可审计的验证结果。
- **收益**：医疗、财务、法律、关系候选能更早暴露证据不足或冲突，减轻人工 review 压力。
- **风险**：自检不能替代人工确认；验证模型也可能错。

### P1-13：检索表示拆成 `latent_summary + sparse_keys + exact_ref`

- **发现来源**：DeepSeek-V3 MLA / FlashMLA 的压缩 KV cache、token-level sparse attention、FP8 KV cache；转译为信息架构类比。
- **要点**：
  - `latent_summary` 负责召回和粗路由。
  - `sparse_keys` 负责实体、日期、金额、代码、关键词过滤。
  - `exact_ref` 负责回拉原文、页码、OCR region、message id、timestamp。
- **收益**：不把完整原文常驻或全量 embed 当默认，同时保留精确证据回拉。
- **风险**：DeepSeek MLA 是模型内部机制，不能机械映射到数据库；这里只作为 P1 级设计启发。

## 2026-05-13 12:21 EDT 新增候选项（field cardinality / medical / email / relationship safety）

### P0-10：新增 `field_contract`，显式声明字段基数与合并语义

- **发现来源**：LinkML slots/cardinality（`required`、`multivalued`、`minimum_cardinality`、`maximum_cardinality`、UML `0..1/1/0..*/1..*`）；Logseq DB properties 的 typed property / multi-value / tag properties 模式。
- **要点**：
  - 为高价值字段增加 `field_contract`：`field_name/scope/cardinality/value_type/ordered/merge_semantics/conflict_policy/default_review_state/sensitivity_floor/sync_floor/provenance_required`。
  - 建议合并语义词表：`replace_by_authority`、`append_unique`、`append_versioned`、`max_sensitivity`、`min_sync_permission`、`union_tags`、`intersect_permissions`、`manual_only`、`derive_only`、`no_merge_cluster_only`。
  - 先覆盖跨域字段和高风险字段：identity、timestamps、sensitivity、sync_permission、review_state、entity_refs、evidence_refs、medical values、finance amounts、contact fields、relationship edges。
- **收益**：把“字段能不能多值、冲突时怎么合并、是否需要人工确认”从实现细节提升到 IA 规范层；支持未来规则引擎、导入器、同步器和审计日志。
- **schema 影响（提案级）**：在 sidecar/frontmatter/rule spec 中引用 `field_contract`；规则动作必须遵守字段的 cardinality 与 merge semantics。
- **风险**：字段契约过早铺太广会膨胀；第一版只维护 20-40 个核心字段，其他字段继承默认策略。

### P1-14：把 FHIR-inspired 医疗最小视图落成字段矩阵

- **发现来源**：HL7 FHIR R4 `DocumentReference`、`DiagnosticReport`、`Observation`、`Encounter`、`MedicationStatement`。
- **要点**：
  - 区分 `medical_document`（证据/文档引用）、`medical_encounter`（就诊上下文）、`diagnostic_report`（报告/面板）、`medical_observation`（原子结果/症状/生命体征/可穿戴数据）、`medication_statement`（用药陈述）。
  - `Observation` 不只是一段 OCR 文本，应至少有 `status/code/value/unit/reference_range/effective_at_or_period/encounter_ref/derived_from_refs`。
  - `DiagnosticReport` 负责把多个 observation 组合成报告，并保留 `presented_form_ref` 回拉原始 PDF/截图。
  - `MedicationStatement` 表示“被报告的用药事实”，不等同于处方、发药或实际服药事件。
- **收益**：个人 DB 可以回答就诊时间线、化验趋势、处方/用药历史、保险/账单关联，同时避免实现完整 EHR。
- **schema 影响（提案级）**：P1-9 需要补充最小字段表和默认 review/privacy 策略；医疗对象必须 evidence-backed。
- **风险**：医疗自动化风险高；默认 `medical_high/local_only/review_required/claim_state=candidate`，只用于归档、检索、就诊准备，不做诊断/用药/理赔决策。

### P1-15：邮件 ingest 分离 `ingest_tags`、`mail_client_flags` 与 thread rollup labels

- **发现来源**：Notmuch initial tagging 的 `new -> post-processing -> inbox/unread` 工作流；Notmuch special tags 对 Maildir flags、attachment、signed、encrypted 的区分。
- **要点**：
  - `email_raw_message` 保留 `message_id/thread_key/mailbox_account/folder_or_label_snapshot/header_hash/body_hash/mime_structure_ref/attachment_refs/mail_client_flags/ingest_tags`。
  - `ingest_tags` 只表示管线状态：`new/parsed/classified/reviewed/archived_only`。
  - `mail_client_flags` 镜像源邮箱状态，不等同于个人数据库语义。
  - `email_thread.rollup_labels` 从 child messages/attachments 派生；thread label 不覆盖 message-level facts。
  - attachment 必须成为独立 evidence asset，并回链 message/thread。
- **收益**：旧邮箱和新邮箱都能先安全归档，再逐步抽取 bills/receipts/deadlines/account notices/security notices/contact updates/tasks/events。
- **schema 影响（提案级）**：深化 P1-6，并与 P0-6 的 `scope/aggregation_level`、P0-10 的 `field_contract` 联动。
- **风险**：thread rollup 会扩大敏感范围；thread 层必须采用 `max_child_sensitivity` 与 `min_child_sync_permission`。

### P1-16：关系图谱增加 consent-aware edge 与 field-level privacy

- **发现来源**：Monica 的 contacts/relationships/reminders/activities/notes/documents/photos/custom fields；Reddit 对 personal CRM / graph-based relationships 的需求；Relaticle 的 dynamic custom fields 与 per-field encryption 模式。
- **要点**：
  - `relationship_edge` 增加 `directionality/claim_state/confidence/valid_from/valid_to/evidence_refs/visibility_scope/consent_state/sensitivity/sync_permission`。
  - `person_profile_field` 增加字段级 `field_sensitivity/field_sync_permission/review_state/cardinality/source`。
  - 默认值：关系图对象 `local_only`、`review_required`、不进入外部同步/外部检索，除非显式允许。
- **收益**：生日提醒、联系方式、共同经历、家庭关系、敏感冲突、第三方私人信息可以共享同一图谱，但采用不同权限和检索行为。
- **schema 影响（提案级）**：深化 P1-8；relationship graph 检索必须按 edge/field 权限裁剪，不只按 person_profile 裁剪。
- **风险**：隐私字段增加人工 review 成本；但这是全生活数据库必须承担的边界，尤其未来若接入 AI assistant 或 Telegram/Hermes 同步。

## 2026-05-13 13:24 EDT 新增候选项（source snapshots / import runs / error records）

### P0-11：新增 `source_snapshot` / `import_run` / `parse_error_record`，把导入批次和解析失败一等化

- **发现来源**：HPI/Human Programming Interface 的本地文件系统 source modules；cachew 的输入 hash、持久化解析缓存和 `Exception` 可序列化模式；Dogsheep/Datasette 的 source-to-SQLite 个人数据仓库；Reddit DataHoarder 对多硬盘归档、中央索引、hash/EXIF/perceptual hash 日志的实践讨论。
- **要点**：
  - `source_snapshot` 表示一批输入来源：`api_export | gdpr_archive | takeout | mailbox_dump | photo_library | filesystem_scan | device_backup | manual_import`。
  - `import_run` 表示一次导入/重跑/修复：`full | incremental | replay | repair | dry_run`，记录 adapter/parser 版本、输入 snapshot、输出数量、错误数量。
  - `parse_error_record` 表示解析失败、字段缺失、schema drift、OCR 失败、低置信、重复冲突等；错误不只写日志，而是可检索、可审阅、可在解析器升级后重跑的质量对象。
  - 所有 evidence/assets/chunks/candidates/errors 都应能回链到 `import_run_id`，再回链到 `source_snapshot_id`。
- **收益**：旧邮箱、Google Takeout、Apple Photos/Immich、旧硬盘、健康导出、银行/账单导出都能可复现导入；未来修复 parser 后可以精准重跑失败项，而不是重新扫全库。
- **schema 影响（提案级）**：在 inbox/raw_evidence 前后新增 source/import 层；`provenance.record` 可引用 `import_run_id`，避免重复塞入 adapter/parser 细节。
- **风险**：元数据膨胀；source snapshot 与 error message 可能泄露路径、账户、邮箱 header、医疗术语，默认 `local_only` 并继承 affected evidence 的最高 sensitivity。

### P0-12：为长期可变实体引入可选 `object_anchor + attribute_claim` 模型

- **发现来源**：Perkeep permanode/claim schema：不可变内容寻址 blob 之上，用稳定 permanode 承接可变对象，用 `add-attribute / set-attribute / del-attribute` claim 追加表达变更。
- **要点**：
  - `object_anchor` 只提供稳定身份，不直接承载会被覆盖的事实。
  - `attribute_claim` 表示 set/add/del/merge/retract，带 `claim_date`、`claim_state`、`review_state`、`field_contract`、`evidence_refs`、`created_by`。
  - 当前对象视图是把 claims 按 field_contract 和时间顺序 fold 出来的 materialized view。
  - 优先用于多年可变且高风险对象：`person_profile`、`relationship_edge`、`account`、`medical_condition`、`medication_statement`、`subscription_schedule`、`property`、`vehicle`、`device`。
- **收益**：避免“长期对象被覆盖写坏后不知道历史状态”的问题；支持撤回、纠错、冲突保留、时间有效性和审计回放。
- **schema 影响（提案级）**：深化 P0-4 provenance、P0-5 field authority/merge policy、P0-10 field_contract；不是替代现有对象表，而是为高风险对象提供变更底座。
- **风险**：第一版实现可能过重；建议先作为 IA 约定和少数对象试点，不要求所有低风险对象都 claim 化。

### P1-17：新增只读 `local_data_warehouse_view` / `exploratory_index_view` 作为审阅与调试层

- **发现来源**：Dogsheep 把 GitHub/Reddit/Twitter/photos 等个人数据导入 SQLite，Datasette 提供可浏览 API/UI，sqlite-utils 支持从 JSON/CSV 自动建表、FTS、lookup table。
- **要点**：
  - 从 file-first truth layer 和 confirmed/candidate objects 生成只读 SQLite/FTS/BM25 视图。
  - 视图必须记录 `built_from_import_run_ids`、`schema_version`、`generated_at`、`field_allowlist`。
  - 该视图服务于人工审阅、调试、临时分析和批量质量检查，不是唯一真相。
- **收益**：比直接浏览文件夹或主 DB 更适合发现导入缺口、重复项、OCR 失败、邮件附件漏解析、照片 EXIF 异常、账单周期异常。
- **schema 影响（提案级）**：新增可重建索引/视图层；与 retrieval 的 exact search / FTS / BM25 兼容。
- **风险**：share/subset 视图可能泄露 GPS、人脸、医疗、财务、关系图谱；必须默认本地、只读、字段白名单。

### P1-18：为离线硬盘/NAS/冷归档新增 `storage_location_ref` 与 `availability_state`

- **发现来源**：Reddit DataHoarder 关于大型个人归档检索的讨论：用户经常依赖中央目录、文件 hash、EXIF、perceptual hash、硬盘编号/序列号、路径索引来定位离线文件。
- **要点**：
  - `raw_evidence` / `media_asset` 增加 `storage_location_ref`。
  - `storage_location` 包含 `volume_id`、`volume_label`、`device_serial_hash`、`original_path`、`normalized_path`、`availability_state`、`last_seen_at`、`last_verified_at`。
  - `availability_state`: `online | offline_indexed | missing | cold_archive`。
  - 检索结果必须能说明“可立即打开 / 索引可见但原件离线 / 原件缺失 / 需要连接某块盘”。
- **收益**：让旧硬盘、家庭历史照片、税务归档、扫描件、NAS 冷数据进入同一检索体系，而不是只能依赖模糊记忆。
- **schema 影响（提案级）**：深化 raw evidence 的 location/provenance；影响 retrieval UI 和 source evidence pullback。
- **风险**：路径和设备信息本身敏感；设备序列号应 hash，路径展示应支持 redaction，离线索引必须用 `last_verified_at` 避免误导。

## 2026-05-13 14:25 EDT 新增候选项（local archive / index cache / citation gate）

### P0-13：明确 `truth / cache / export` 三层，防止检索缓存变成事实来源

- **发现来源**：msgvault 的 SQLite system of record + Parquet analytics cache + local vectors；ArchiveBox 的普通文件夹 + SQLite/JSON 元数据 + 可直接浏览的 snapshot 文件夹。
- **要点**：
  - `truth layer`：原始文件、sidecar、confirmed personal memory objects。
  - `cache layer`：FTS/BM25、OCR cache、thumbnail、analytics parquet/duckdb、vector embeddings。
  - `export layer`：Markdown/wiki/static HTML/CSV/JSON bundle。
  - cache 必须可重建，并带 `built_from_refs/generated_at/schema_or_model_version`。
  - export 默认字段白名单和 redaction，不直接暴露高敏 evidence。
- **收益**：以后可以优化搜索和分析而不破坏 file-first/local-first 真相层；也能避免 vector/Parquet/索引库锁定。
- **schema 影响（提案级）**：新增 `storage_layer: truth | cache | export`；派生索引/embedding/cache 对象新增 `built_from_refs`。
- **风险**：多一层概念会增加文档复杂度；个人版应只把它作为原则和少数字段，不要做完整数据平台。

### P0-14：高风险候选新增 `citation_refs / citation_state` 审阅门

- **发现来源**：Reddit 上用 Obsidian 管理复杂医疗记录的讨论强调 OCR、LLM 跳过源文件、医疗隐私和源文引用问题；GitEHR 强调医疗记录的审计与可追溯。
- **要点**：
  - 医疗、财务、法律、账号安全、关系类候选必须能回到 evidence。
  - `citation_state`: `none | file_level | page_level | region_level | excerpt_level`。
  - `citation_refs` 至少包含 `evidence_ref/page_or_message_id/excerpt/extraction_method`。
  - 没有 citation 的高风险候选只能保持 `candidate`，不能进入 confirmed。
- **收益**：降低 LLM/OCR 在高风险领域制造“看似确定事实”的风险；review 时能快速回看原件。
- **schema 影响（提案级）**：扩展 `candidate_item` 与 high-risk domain objects；与 `evidence_refs` 不冲突，`citation_refs` 是更细粒度证据定位。
- **风险**：引用粒度越细维护成本越高；第一版建议只强制 file/page/message_id，OCR region 以后再加。

### P1-19：把 `raw_evidence / media_asset` 文件组织升级为轻量 `evidence_packet`

- **发现来源**：ArchiveBox 每个 snapshot 保留多种输出文件和 `index.json`；msgvault 对附件 content-addressed 存储；Reddit 大型个人归档讨论强调普通目录、hash、EXIF、中央索引仍然最可靠。
- **要点**：
  - 一个高价值 evidence 可以组织为 `original + meta sidecar + extracted text/OCR + preview + optional redacted copy`。
  - `artifact_role`: `original | sidecar | extracted_text | ocr | preview | redacted | index_record | embedding`。
  - preview/OCR/redacted 都是派生物，权限不得低于 original，除非显式脱敏确认。
- **收益**：原件、OCR、预览和脱敏副本不会散落；应用不可用时，文件夹仍可理解和迁移。
- **schema 影响（提案级）**：不替换 `raw_evidence/media_asset`，只增加文件夹约定和 `derived_refs`。
- **风险**：派生文件增加存储与泄露面；需要清楚标注 original vs derived。

### P1-20：通信归档区分 `source_native labels` 与 `personal labels`

- **发现来源**：msgvault 对 Gmail/IMAP/MBOX/Apple Mail/聊天来源保留 source、conversation、message、raw MIME、labels、attachments；此前 Notmuch/afew 研究也支持 message/thread 分层。
- **要点**：
  - `labels_from_source`：Gmail label、IMAP folder、聊天 app 状态、历史导出标签。
  - `personal_labels`：个人记忆库语义标签，如 bill、receipt、security_notice、relationship、travel。
  - `pipeline_state`：new/parsed/classified/reviewed/archived_only，不与上述两类混用。
- **收益**：旧邮箱和新邮箱都能安全导入；来源标签不会污染个人语义分类。
- **schema 影响（提案级）**：深化 email/chat 最小字段；可推广到 photo albums、filesystem folders、cloud labels。
- **风险**：字段略增；但比把所有标签塞进一个 `tags` 数组更可维护。

## 2026-05-13 15:26 EDT 新增候选项（canonical membership / evidence packets）

### P0-15：新增 `source_membership`，把来源容器/标签/相册从个人语义标签中拆出

- **发现来源**：Birdclaw 的 canonical tweets/profiles + account-scoped timeline/collection edges；Discrawl 的 channel/thread/message/attachment 分层与 Git snapshot 发布白名单；此前 Notmuch/afew 与 msgvault 对 source labels 和 personal labels 的区分。
- **要点**：
  - 同一个 canonical object 可能出现在多个来源容器里：旧邮箱文件夹、新 Gmail label、聊天 thread、Apple Photos album、云盘目录、社交收藏、导出批次。
  - `source_membership` 只表达“来源系统如何组织它”，不表达个人数据库的长期语义。
  - 个人语义继续用 `personal_labels` / `semantic_type` / `domain` 表达。
  - 最小字段：

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

- **收益**：避免旧邮箱/新邮箱/相册/文件夹/聊天导出标签污染长期语义；支持同一资产多来源出现但只保留一个 canonical object；未来 Google/Telegram/Hermes sync 可以按 membership 裁剪。
- **schema 影响（提案级）**：`raw_evidence`、`media_asset`、`email_message`、`chat_message`、`person_profile`、`document_record` 都可挂多个 `source_membership`；`labels_from_source` 可降级为 membership 的字段，而不是对象主标签。
- **风险**：多一层边对象；来源容器名本身可能敏感，默认继承 canonical object 最高 sensitivity，外部 export 默认排除 `local_only` membership。

### P0-16：高价值证据采用个人版 `evidence_packet + citation_ref` 最小约定

- **发现来源**：Reddit 上用 Obsidian/LLM wiki 管理复杂医疗记录的实际痛点（OCR、LLM 跳过文件、回源困难、医疗隐私）；ArchiveBox snapshot 文件夹；SwarmVault raw/wiki/state 三层；Discrawl 附件二进制外置而只索引 metadata/可选 extracted text。
- **要点**：
  - `evidence_packet` 不是替换 `raw_evidence/media_asset`，而是把高价值证据的原件、sidecar、OCR/text、preview、redacted copy 放在一个可理解的包里。
  - `citation_ref` 不只指向文件，还可指向 packet 内 artifact 和 locator（页码、message id、section、OCR region、timestamp）。
  - 高风险 confirmed object（医疗、财务、法律、账号安全、关系）至少需要 file/page/message 级 citation；没有 citation 只能保持 candidate。
  - 最小字段：

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

- **收益**：review 时能快速从候选事实回到原 PDF/截图/邮件/附件；应用不可用时文件夹仍可迁移和理解；降低 OCR/LLM 把高风险信息说错但无法追溯的风险。
- **schema 影响（提案级）**：深化 P0-14 和 P1-19；`candidate_item` 与 high-risk domain objects 增加 `citation_refs`；`raw_evidence/media_asset` 增加可选 `packet_id` 或 `packet_ref`。
- **风险**：对所有资料强制 packet 化会过重；第一版只对医疗、财务、法律、账号安全、重要行政文件和少量高价值截图强制。

### P1-21：把 `truth / working / cache / export` 降级写成个人版四层边界

- **发现来源**：SwarmVault 的 `raw/ wiki/ state/` 三层；Engram 的 Markdown source of truth + 可重建 FTS/Xapian index；Discrawl 的 SQLite/FTS/embedding provider-model-input_version 约束。
- **要点**：
  - `truth`：原始文件、sidecar、confirmed personal memory objects。
  - `working`：人工可读 wiki/brief/summary/doctor visit prep，不是真相，必须带 `built_from_refs` 和 `review_state`。
  - `cache`：OCR cache、thumbnail、FTS/BM25、embedding、graph view，可删除重建。
  - `export`：Markdown/HTML/CSV/JSON bundle，必须字段白名单和 redaction。
  - cache 记录 `provider/model/input_version/generated_at`，避免不同 embedding 或解析版本混用。
- **收益**：让个人系统能同时保留原件、生成好读整理页、快速搜索，并避免把索引或 LLM wiki 当成唯一事实。
- **schema 影响（提案级）**：深化 P0-13；新增 `storage_layer`、`artifact_role`、`built_from_refs`、`cache_identity` 等少量字段。
- **风险**：概念增多；应作为目录/字段约定，而不是第一版就实现完整数据平台。

## 2026-05-13 16:26 EDT 新增候选项（timeline projection / temporal uncertainty）

### P0-17：把时间线升级为 `timeline_projection + timeline_entry`，但明确它不是事实主存储

- **发现来源**：Timelinize/Timeliner 把 timeline、map、conversation、gallery 明确作为不同 projections；ActivityWatch 的 bucket/event/heartbeat 模型；facebookresearch personal-timeline / TimelineQA 的 retrieval-based 与 view-based QA；Obsidian/Reddit daily note 实践对 rollup、Dataview、检索稳定性的经验。
- **要点**：
  - `daily_timeline / medical_timeline / finance_timeline / relationship_timeline / map_view / gallery_view` 都应是从 raw evidence、confirmed objects、candidate objects、source memberships 生成的投影视图。
  - 新增 `timeline_projection`：记录 projection 类型、构建规则、权限范围、redaction 策略、coverage 状态、cache identity。
  - 新增 `timeline_entry`：记录 canonical_ref、source_membership_refs、temporal_anchor、display_group、domain、entity_refs、place_refs、evidence_refs、citation_refs、sensitivity、sync_permission、review_state、confidence。
  - `daily_narrative_log` 只能是 working/export 层，必须带 `built_from_projection_id`，不能作为 evidence 或 confirmed fact。
- **收益**：用户可以按日、领域、人、地点、旅行、会话、图库浏览全生活数据，同时不把 AI 总结或日记视图污染事实层；也支持 “上次 X 是什么时候”“某月账单/运动/就诊有哪些”“某次旅行涉及哪些照片/邮件/票据” 这类聚合查询。
- **schema 影响（提案级）**：新增 `timeline_projection`、`timeline_entry`；深化 P0-6 `aggregation_level`、P0-13/P1-21 truth/cache/working 边界、P0-15 source_membership、P0-16 citation_ref。
- **风险**：时间线聚合会放大隐私风险；必须按 child objects 计算 `max_sensitivity` 与 `min_sync_permission`，并显示 `coverage_state=complete|partial|unknown`，避免不完整导入被误解为完整历史。

### P0-18：新增 `temporal_anchor`，显式表达时间角色、精度、时区和不确定性

- **发现来源**：Timelinize 对 item 使用 timestamp/timespan/timeframe/time_offset/time_uncertainty；ActivityWatch 事件模型提醒 continuous stream 需要 timestamp/duration，但其 UTC-only 行为也暴露了 timezone 丢失风险；TimelineQA 强调 lifelog QA 同时依赖自由文本、时间和地点结构。
- **要点**：
  - 不再假设所有对象只有一个 `occurred_at`。同一对象可能有 `captured_at/sent_at/received_at/issued_at/due_at/paid_at/appointment_at/observed_at/ingested_at/inferred_at`。
  - 最小字段：

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

  - 对照片、旧扫描件、医疗报告、账单、邮件、聊天、未来 wearable/audio stream 都保留 `time_source` 与 `temporal_precision`。
  - ActivityWatch 风格 stream 的 heartbeat/merge 结果应作为 projection/cache，不覆盖 raw event。
- **收益**：长期系统能正确处理旅行跨时区、旧照片只知年月、账单 due/paid 差异、医疗 observed/issued/imported 差异、邮件 sent/received/imported 差异；时间线和检索排序更可信。
- **schema 影响（提案级）**：`raw_evidence/media_asset/email_message/chat_message/medical_item/finance_item/event/task` 增加可选 `temporal_anchor`；`occurred_at` 可保留为便捷字段，但应由 `temporal_anchor.primary_time` 派生。
- **风险**：字段复杂度上升；第一版可只要求 `primary_time/primary_time_role/temporal_precision/timezone/time_source`，其余字段按需补充。

## 2026-05-13 17:26 EDT 新增候选项（raw samples vs semantic projections）

### P0-19：新增 `interpretation_level`，区分原始观测、来源语义推断、派生候选和投影视图

- **发现来源**：Timelinize 的本地原始数据 + timeline/map/conversation/gallery projections；Google Takeout Location History 的 raw `Records.json` vs `Semantic Location History`（`placeVisit` / `activitySegment`）；DFIR Review 对 Google semantic layer 受用户编辑影响的分析；Apple Health / HealthKit sample 的 start/end/source revision 模式。
- **要点**：
  - `review_state` 只表示人是否确认；`interpretation_level` 表示记录距离原始观测有多远。
  - 最小枚举：`raw | source_semantic | derived_candidate | reviewed_fact | projection`。
  - Google/Apple/可穿戴设备的自动 place visit、activity segment、sleep session、weekly trend 默认不是 truth，必须明确为 `source_semantic` 或 `projection`。
- **收益**：避免来源系统的语义推断污染个人事实层；未来导入位置、健康、wearable、audio stream 时，不需要重构 review/retrieval 模型。
- **schema 影响（提案级）**：`labels` 或 sidecar 最小字段新增可选 `interpretation_level`；`timeline_entry`、`candidate_item`、`health_sample`、`location_raw_point` 均可使用。
- **风险**：增加一个概念；但比引入完整的 source trust ontology 轻得多，适合个人版。

### P1-22：为位置和健康连续数据预留 `raw sample -> semantic candidate -> projection` 最小对象

- **发现来源**：Google Semantic Location History schema（`activitySegment` / `placeVisit`）；Apple Health XML/HealthKit sample 的 `type/value/unit/startDate/endDate/sourceName/sourceVersion/device` 社区导出经验；QS Ledger 的 local quantified-self downloader + analysis dashboard 分层。
- **要点**：
  - 位置：`location_raw_point` 保留原始点；`place_visit_candidate` 和 `movement_segment_candidate` 保留来源系统推断；`map_view/travel_timeline/daily_projection` 作为 projection。
  - 健康：`health_sample` 保留 sample type、value、unit、start/end、source/device、evidence_ref；sleep session、exercise summary、weekly trend、doctor prep summary 只是 projection/working layer。
  - 不现在实现 Google/Apple/wearable 导入，只把 IA 边界写清楚。
- **收益**：支持未来 lifelog/wearable/audio streams，同时保持现在的个人版轻量主干。
- **schema 影响（提案级）**：未来可新增 `location_raw_point/place_visit_candidate/movement_segment_candidate/health_sample`；现阶段只在文档中作 P1 预留。
- **风险**：GPS、home/work pattern、sleep、heart rate、symptom 等都是高敏感；默认 `local_only`、不 embed raw、不导出精确轨迹。

## 2026-05-13 17:49 EDT 新增候选项（PS 总管串行 agent work log）

### P0-20：新增 `ps_agent_work_log` + `domain_agent_queue`，强制小秘串行 processing/audit/proposal chain

- **发现来源**：本轮复核 `06-global-workflow.md`、`07-personal-memory-minimal-workflow.md`、既有 P1-11 `assistant_handoff/context_event_log` 与最近 agent workflow 讨论。现有结构已有 handoff、review gate、candidate verification，但还缺少总管层面的“先记录结果、再允许下一棒”的串行门闩。
- **要点**：
  - 总管是唯一全局 work log owner，负责分类、分派、记录结果、冲突/阻塞、下一步排队。
  - 每个小秘只维护一个 `active_chain_id`；同一时间只能有一条 active processing/audit/proposal chain。
  - processing agent 只处理一个 evidence packet，返回 `processing_result` 或 `abstract_result`。
  - audit agent 检查 processing result、citation_refs、scope boundary 和 risk flags，返回 `audit_result`。
  - proposal agent 根据 processing/audit 结果生成 `review_result` / `update_proposal` / `no_action`，但不直接写 truth layer。
  - 小秘汇总生成 `domain_event_summary_report`，并 report 给总管。
  - 只有总管把该 work log 状态推进到 `secretary_reported | closed`，并设置 `next_spawn_allowed=true` 后，小秘才能开始下一条 chain。
  - 失败、证据不足、冲突、超范围都必须写 `blocked_reason`，不能静默继续。
- **最小字段**：

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

- **收益**：保证“为什么这条记忆被写入/更新”可解释；避免小秘并发 spawn 导致重复候选、citation 丢失、冲突被覆盖；同时保持个人版轻量，不引入企业级任务平台。
- **schema 影响（提案级）**：新增 `ps_agent_work_log` 与 `domain_agent_queue`；加深 P1-11 `assistant_handoff`，但不保存 one-shot 长上下文，不改变 truth layer。
- **风险**：work log 可能包含敏感路径、对象、关系或医疗/财务上下文；必须继承最高 sensitivity，默认 `local_only`，外部 export 默认排除。

### P1-23：统一 `processing_result / audit_result / proposal_result` 最小输出 schema

- **要点**：短生命周期 agent 只能返回结构化中间结果，不直接写 confirmed memory 或 truth layer。

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

- **收益**：小秘可以用固定方式串接处理、审计、提案；总管可以用 `domain_event_summary_report` 固定字段排下一步。
- **风险**：字段过多会变成企业级 runner schema；第一版只把它作为文档约定，不实现运行器。
