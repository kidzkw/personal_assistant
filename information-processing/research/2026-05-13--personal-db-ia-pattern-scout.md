# 2026-05-13 个人全生命周期数据库 IA 参考模式扫描（GitHub/Reddit）

目标：在不写应用代码的前提下，为“local-first + file-first inbox + 保留原始证据”的个人助理/个人数据库，补强 5+ 年可持续的信息架构：分类维度、标签体系、媒体/健康/邮件管线、切段与迁移、检索与隐私耐久性。

## 0. 本地现状（仓库内既有方向）

当前仓库主要整理了 Omi 的信息处理链路，核心可借鉴点是三层分离：

- **证据层（Evidence）**：原始 transcript segments / 原始输入，不做“结论式”覆盖，强调可回溯。
- **理解层（Understanding）**：LLM/规则产生的结构化摘要与语义标签（title/overview/category…）。
- **行动/检索层（Action & Retrieval）**：memories、action_items、events、向量/索引元数据，用于任务化与检索。  
  参考：Omi 分析与信息处理文件夹（仓库内）。

这套“证据→理解→行动/检索”的分层，适合扩展到：照片/截图、PDF/票据、邮件、健康记录、财务流水、关系 CRM、设备/账号资产等。

## 1. 外部参考模式（强相关，偏原始 repo/doc/讨论）

### 1.1 照片/媒体：**Sidecar 元数据 + 去重/相似度 + 可导出**

关键模式：

1) **不要修改原图/原视频**，优先通过 sidecar（XMP/YAML/JSON）写入可编辑元数据（标签、描述、评分、时间/地点等），便于长期可移植与外部工具协作。  
   - Immich：支持 XMP sidecar 读写，并在 UI 编辑后可写回 sidecar（带命名规则与作业队列）。[Immich XMP Sidecars](https://docs.immich.app/features/xmp-sidecars/)  
   - PhotoPrism：读取原始与 sidecar 元数据，并强调“可独立于数据库访问元数据”，会生成可读 YAML sidecar；同时也能读取 Google Photos JSON/Apple XMP 等。  
     [PhotoPrism Metadata Support](https://docs.photoprism.app/user-guide/library/metadata/)

2) **去重分两层**：精确去重（hash/size）与近似去重（视觉相似/ML embedding）。两层输出都应能回溯并可人工审阅。  
   - PhotoPrism：精确重复以 SHA1+size 跳过；相似度能力与感知哈希用于“按视觉相似排序”。  
     [PhotoPrism Duplicate Detection](https://docs.photoprism.app/user-guide/library/duplicates/)  
     [PhotoPrism Perceptual Hashes](https://docs.photoprism.app/developer-guide/metadata/perceptual-hashes/)  
   - Immich：提供 duplicates utility（基于 ML），并在“保留/删除”决策时做**元数据同步**（相册/评分/描述/可见性/位置/标签等合并）。  
     [Immich Duplicates Utility](https://docs.immich.app/features/duplicates-utility)

落到个人数据库 IA 的启示：

- “图片证据文件”应当是不可变资产；所有人工/自动标签优先写入 sidecar（照片用 XMP；截图/PDF 可用 JSON sidecar），减少 DB lock-in。
- 去重/合并要有“**合并策略**（选择保留哪份 + 元数据合并规则）”，并留下审计记录。

### 1.2 文档/票据：**多轴分类（对应人/类型/标签）+ INBOX 审阅门 + 双时间**

Paperless-ngx 的文档管线给出了一套非常“生活管理友好”的分类轴：

- **Correspondent**（来往方：机构/个人）
- **Document type**（文档类型：invoice/contract/medical record…，建议保持粗粒度）
- **Tags**（多标签，比文件夹更灵活）
- 并区分 **date added**（摄入时间，不应修改） vs **date created**（文档签发/发生时间）。  
  [Paperless-ngx Basic Usage / Terms](https://docs.paperless-ngx.com/usage/)

社区讨论中反复出现的稳定工作流：

- 所有新摄入文档默认打 `_INBOX/INBOX` 标签；人工校验后再移除（保留“最终验证”步骤）。  
  [Reddit: Paperlessngx 扫描最佳实践讨论](https://www.reddit.com/r/Paperlessngx/comments/1i8qbqq)

落到个人数据库 IA 的启示：

- “生活管理文档”天然适合 **3 个主轴**（来往方/文档类型/标签），比单一层级目录更稳定。
- 时间字段必须拆开：`captured_at/ingested_at`（进入系统时间）与 `occurred_at/issued_at`（事件发生/签发时间）。
- INBOX 审阅门是长期正确性的关键（尤其用于医疗/财务/法律关键记录）。

### 1.3 邮件：**tag-first**（收件箱不是文件夹，而是状态集合）

Notmuch 的核心是一句话：**全局搜索 + 任意 tag 的邮件系统**，并希望你的 inbox 变得“not much”。  
[Notmuch 官网](https://notmuchmail.org/)  
其文档还给出“new→inbox/unread”等 post-processing tagging 的实践。  
[Notmuch initial tagging](https://notmuchmail.org/initial_tagging/)

落到个人数据库 IA 的启示：

- 邮件应被视为“不可变证据（message + headers + attachments）”，其“是否需要处理/归档/生成任务”用标签与派生对象表达，而不是移动文件夹。

### 1.4 健康/医疗：**FHIR 资源化 + 证据挂载 + 解释层（人类可读）**

Fasten Health（自托管个人/家庭 PHR 聚合器）的信息点：

- 目标是把多机构记录拉到个人手里，基于 FHIR/SMART on FHIR（OAuth2），并强调自托管。  
  [Fasten Health GitHub 组织页](https://github.com/fastenhealth)  
- Reddit 长帖展示了“按 Condition 汇总 Encounter/Lab/Practitioner”的视图，以及“上传 FHIR Bundle JSON、上传文档/影像”等路线，并讨论了安全/合规与网关组件的权衡。  
  [Reddit: Fasten Health (selfhosted) 2023 贴](https://www.reddit.com/r/selfhosted/comments/10ky6tb)

落到个人数据库 IA 的启示：

- 医疗域建议采用“**资源化**”的命名：Encounter（就诊/就医接触）、Observation（指标/检验结果）、Medication、Condition、Procedure、Coverage/Claim 等；并把 PDF/照片/邮件作为每个资源的 evidence attachments。
- 需要区分：`source-of-truth`（来自机构的证据） vs `user-notes`（自述症状/体感/记忆），并分别标注置信度与审阅状态。

### 1.5 关系/人际：**关系图谱 + 互动日志 + 提醒**

Monica（个人 CRM/PRM）强调：联系人、关系、活动记录、重要日期与提醒。  
[Monica GitHub](https://github.com/monicahq/monica)  
[Monica 官网介绍](https://www.monicahq.com/)

落到个人数据库 IA 的启示：

- “人”应当是第一类实体（entity），与邮件/照片/事件/礼物/对话都能建立关联边（relations）。
- 关系维度建议独立于 domain（例如医疗也会关联医生；财务也会关联收款方）。

### 1.6 财务：**复杂对象拆分 + 规则/周期 + 可回溯**

Firefly III 的架构文档强调交易被拆成多个层级对象（group/journal/transactions），并提供规则与 recurring 的概念。  
[Firefly III 架构说明](https://docs.firefly-iii.org/explanation/more-information/architecture/)  
此外，Actual Budget 明确定位为“local-first personal finance app”。  
[Actual Budget GitHub](https://github.com/actualbudget/actual)

落到个人数据库 IA 的启示：

- 财务记录建议把“证据（账单/收据/PDF/邮件）”与“结构化条目（交易/订阅/账期/应缴截止日）”分离，并通过 `evidence_refs` 回链。
- recurring/subscription 是一等对象，适合驱动“提醒/任务”派生，而不是靠全文搜索临时发现。

### 1.7 连续流/行为日志：**bucket + events + 心跳合并（segmentation 模板）**

ActivityWatch 的数据模型非常简洁：bucket（数据源容器） + event（timestamp/duration/data），并提供 heartbeat 合并相邻同态事件以减少噪声。  
[ActivityWatch Buckets & Events](https://docs.activitywatch.net/en/latest/buckets-and-events.html)

落到个人数据库 IA 的启示：

- 对未来的“连续流”（可穿戴、音频、屏幕活动、位置）可以统一用：`stream`（相当于 bucket）+ `event`（timestamp+duration+payload）作为底层原子，再派生出更高层的“会话/活动/日历事件”。

### 1.8 记忆系统：**核心记忆 vs 档案记忆（分层）**

Letta（MemGPT 系列）强调记忆分层：核心记忆（始终可见的持久块）与档案记忆（可检索的外部存储）。  
[Letta MemGPT 架构概览](https://docs.letta.com/guides/agents/architectures/memgpt)

落到个人数据库 IA 的启示：

- 个人数据库中“长期有用事实（memories）”应当是可维护的摘要层（少而精），并永远可回溯到证据；大量原始内容留在档案层做检索。

## 2. 对现有“local-first + file-first”方向的强改进点（建议采纳）

下面是针对你列出的 9 个设计关注点，提炼出来的“结构性增强”：

### 2.1 分类/标签体系：从“单一分类”升级为**多维标签向量（稳定）**

建议把“分类”拆成可组合的维度（优先从可自动/可人工共识的维度入手）：

- **domain**：health / finance / legal / relationships / home / travel / work / education / devices / identity …
- **source_category**：email / scan / screenshot / photo / export-json / statement / chat / note …
- **media_type**：image / pdf / text / markdown / json / video（音频后续）
- **semantic_type**（类似 paperless 的 document_type）：invoice / receipt / lab_result / visit_note / prescription / insurance_claim / contract / warranty …
- **counterparty**（类似 paperless 的 correspondent）：person/org/provider（也可落到实体图谱）
- **actionability**：none / task_candidate / event_candidate / followup_required
- **sensitivity/privacy**：public / personal / confidential / regulated(health)（可再细分）
- **temporal**：occurred_at / captured_at / ingested_at（至少三时间）
- **confidence**：0-1（抽取/分类置信度）
- **review_state**：inbox / needs_review / reviewed / disputed
- **retention_class**：ephemeral / standard / long_term / permanent（结合 legal/medical/financial criticality）
- **criticality**：low/medium/high（法律/医疗/财务关键性）
- **sync_permission**：local_only / ok_to_sync_metadata / ok_to_sync_content（为未来多设备/云同步预留）

### 2.2 标注对象：统一“证据→派生→实体图谱”的引用机制

建议统一为一套 sidecar 元数据结构（JSON），最少要包含：

- `id`（稳定、跨移动/重命名仍可追踪）
- `kind`：evidence | asset | chunk | extraction | entity_ref | event_ref | task_ref | memory_ref
- `provenance`：来源（source_category + 原始路径/哈希 + 采集设备/导出工具/邮箱等）
- `timestamps`：occurred/captured/ingested
- `labels`：上述多维标签
- `evidence_refs`：派生对象必须列出其证据引用（文件+偏移/页码/区域/消息 ID 等）

### 2.3 媒体管线：把“sidecar”作为一等公民

建议对照片/截图/扫描件采用“原文件 + sidecar”标准：

- 照片/视频：优先兼容 XMP sidecar（Immich/PhotoPrism 生态已证明可行）。
- 扫描 PDF/截图/导出 JSON：使用 `*.meta.json` sidecar 承载跨域标签、OCR 产物引用、去重信息（sha1/phash）、隐私级别、审阅状态等。

### 2.4 医疗管线：FHIR 命名 + 证据挂载 + 审阅门

- 把“就诊/检验/用药/诊断/保险”等当作可链接实体（Encounter/Observation/Medication/Condition…），每个实体都可挂多份 evidence（PDF、截图、邮件、照片）。
- 医疗域默认更高敏感级别，严格 `sync_permission=local_only` 作为默认。

### 2.5 邮件/生活管理：Notmuch+Paperless 的组合思路

- 邮件证据不可变（消息体+header+附件）；“要不要办/到期日/账单金额”等都作为派生条目写入结构化层，并回链证据。
- `inbox` 作为 review_state，而不是目录；与 paperless 的 INBOX 标签一致。

### 2.6 切段/连续流：预置 ActivityWatch 风格的 event 原子

为未来音频/可穿戴/屏幕活动预留：

- `stream/bucket`（数据源容器）+ `event(timestamp,duration,payload)` 的最小原子；
- heartbeat/merge 作为“降噪”策略之一（合并相邻同态事件）。

## 3. 风险/取舍（需要显式写进规则）

- **sidecar 一致性风险**：若未来引入 DB/索引，必须定义“sidecar 与索引”的同步策略（谁是主、何时回写、冲突如何处理）。Immich 的“写回作业”与 PhotoPrism 的“可导出 sidecar”是两种不同取向，需要在本系统里明确。  
  参考：[Immich XMP Sidecars](https://docs.immich.app/features/xmp-sidecars/) / [PhotoPrism Metadata Support](https://docs.photoprism.app/user-guide/library/metadata/)
- **近似去重误伤**：视觉相似/embedding 去重会误判；必须强制人工审阅，并保留“被丢弃文件的元数据合并/证据保留”策略。  
  参考：[Immich Duplicates Utility](https://docs.immich.app/features/duplicates-utility) / [PhotoPrism Perceptual Hashes](https://docs.photoprism.app/developer-guide/metadata/perceptual-hashes/)
- **医疗/财务的合规与泄露面**：即便 transcript/evidence 加密，派生摘要与索引元数据也可能泄露语义（Omi 的提醒同样适用）。对敏感域默认最小化索引与同步权限。

## 4. 本次 run 的结论（面向结构调整）

推荐的结构性改变（只做文档层面提案，不落代码）：

1) 把“多维标签维度”作为**统一元数据 schema**的核心，而不是单一 category。
2) 明确“证据层不可变 + sidecar 承载可编辑元数据”的长期策略（照片优先兼容 XMP）。
3) 引入 `review_state=inbox` 的统一审阅门（文档/邮件/医疗/财务都适用）。
4) 为未来连续流预留 `stream + event` 原子模型（ActivityWatch 桶/事件/心跳合并作为参考）。

下一步建议（研究方向）：

- 更深入对齐：Paperless 的 workflows（触发器/动作）如何映射为“本地 file-first 管线”的规则系统（仅文档提案，不写执行器）。
- 针对医疗：梳理 Fasten/PHR 的资源粒度与常见视图（Condition-centric timeline、Labs panel），并映射到本系统 entity graph 的最小字段集合。
- 针对照片：对齐 XMP/EXIF/IPTC 的“写回哪些字段”白名单与敏感字段处理策略（例如 GPS/人脸标签默认不写回/不外同步）。

