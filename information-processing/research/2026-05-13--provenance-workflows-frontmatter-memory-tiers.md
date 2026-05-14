# 2026-05-13 结构优化补充：溯源（PROV/FHIR）、工作流（Paperless）、Frontmatter（SilverBullet）、记忆条目生命周期（Mem0）

目标：在“local-first + file-first inbox + 原始证据不可变”的方向不变前提下，补强 5+ 年可持续的**溯源/审计**、**规则化管线**、**可渐进结构化的文本载体**、以及**长期记忆条目的更新/冲突/过期管理**。

---

## 1) 本次查阅的高价值来源（按主题）

### 1.1 文档/生活管理管线（触发器/动作）

- Paperless-ngx 使用说明（Workflows：trigger + action；顺序执行；覆盖/合并语义；触发器类型与可用字段差异）  
  https://docs.paperless-ngx.com/usage/
- Paperless-ngx issue：触发器在 OCR/自动匹配之前执行导致“内容匹配/高级过滤”不可用（强调“管线阶段”很关键）  
  https://github.com/paperless-ngx/paperless-ngx/issues/12117

### 1.2 溯源/审计（Provenance）

- W3C PROV-JSON：PROV 数据模型的 JSON 表达（Entity/Activity/Agent 与关系）  
  https://www.w3.org/submissions/prov-json/
- FHIR DocumentReference（v5）：明确区分“被引用文档”的溯源与“引用记录本身”的溯源  
  https://fhir.hl7.org/fhir/documentreference.html
- FHIR DocumentReference（build 版，内容一致但更“最新草案”）：  
  https://build.fhir.org/documentreference.html

### 1.3 媒体 sidecar（照片/视频等）

- Immich：XMP sidecar 命名规则、sidecar 优先级、以及 DISCOVER/SYNC 两类作业（发现 vs 全量重扫同步）  
  https://pr-17863.preview.immich.app/docs/features/xmp-sidecars/
- ExifTool：sidecar 文件（XMP/EXV/MIE…）的官方说明（强调 sidecar 可“从零创建”，适合原件不可变策略）  
  https://exiftool.org/metafiles.html

### 1.4 连续流事件原子（为音频/可穿戴/屏幕活动预留）

- ActivityWatch：bucket + event(timestamp,duration,data)；heartbeats 的相邻合并（省 IO/降噪）；“每 bucket 单一来源”的推荐  
  https://docs.activitywatch.net/en/latest/buckets-and-events.html

### 1.5 文本/Markdown 的渐进结构化（Frontmatter/对象索引）

- SilverBullet：YAML frontmatter 作为页面元数据载体（支持嵌套键的点写法），以及“对象索引”（page/table/task 等对象可被查询）  
  https://v1.silverbullet.md/Frontmatter  
  https://v1.silverbullet.md/Objects

### 1.6 记忆条目长期管理（提炼/合并/检索）

- Mem0（仓库 + 论文引用）：强调“动态抽取→整合→检索”的长期记忆流水线与多层记忆概念  
  https://github.com/mem0ai/mem0  
  https://huggingface.co/papers/2504.19413

---

## 2) 发现的可迁移模式（对本仓库 IA 的直接启发）

### 2.1 “规则化管线”：用 Paperless 的 Workflows 思路描述 file-first 流程（但不实现执行器）

**模式**：将“文件进入系统后的处理”写成**可读、可审计、可排序**的规则集：

- 触发器（Trigger）：消费开始/记录新增/记录更新/定时（Paperless 的四类触发器）
- 过滤器（Filter）：按 source、文件名/路径、已有标签、内容匹配（注意：内容匹配依赖 OCR/解析阶段）
- 动作（Action）：赋值/移除（标签、类型、对应方、权限/所有者、字段），以及“发出通知/提醒/导出建议”
- 顺序语义：按 sort order 顺序执行；单值字段后写覆盖；多值字段合并（Paperless 的覆盖/合并语义）

**关键补充**：Paperless 的 issue 说明，**同一个 trigger 名称不等于同一阶段的数据可用性**。因此，本系统的规则说明必须显式写出“阶段（stage）”，例如：

- `stage=ingest`：仅有文件名/路径/hash/采集时间/source 等
- `stage=parse`：可用基础元数据（EXIF/PDF 元信息）
- `stage=ocr`：可用 OCR/文本块
- `stage=extract`：可用抽取候选（task/event/fact/amount/date）
- `stage=review`：可人工确认、固化到长期记忆/关键索引

这解决“为什么这条规则匹配不到”的长期维护问题，也为未来自动化留出可解释空间。

### 2.2 “溯源一等公民”：从 PROV 与 FHIR DocumentReference 借鉴“文档 vs 记录”的双溯源

**模式**：任何派生结论都必须能回溯证据；而且要区分两类溯源：

1) **证据（document/asset）的溯源**：这个文件/图片/邮件附件从哪来？是否被改动？采集链路如何？
2) **引用记录（record/extraction）的溯源**：谁在何时用什么工具/模型从证据中产生了这条“引用/抽取/结论”？是否被人工确认？是否被更新/撤销？

FHIR DocumentReference 明确指出“document 的 provenance”和“document reference 的 provenance”是两套信息；PROV 则给出 entity/activity/agent 的最小模型。

对个人全生命周期数据库来说，这是医疗/法律/财务场景“可解释与可纠错”的地基：你永远需要回答“这条信息怎么来的”与“我为什么相信它”。

### 2.3 “可渐进结构化的文本载体”：Frontmatter 让 Markdown 既可读又可被索引/过滤

**模式**：SilverBullet 的 frontmatter 让“文件=页面”同时承载机器可读元数据（tags/aliases/status…），并支持把结构逐步加上去。

对本系统的建议不是引入 SilverBullet，而是把 frontmatter 作为“文本类派生记录（note/summary/report）”的**默认结构容器**，并与 `*.meta.json` sidecar 并行存在：

- `evidence/*`：不可变，优先 sidecar（JSON/XMP）
- `derived/*.md`：可编辑，使用 YAML frontmatter 承载 labels/timestamps/provenance/evidence_refs

这样既满足“文件优先/可移植”，也避免“证据原件被不断改写”。

### 2.4 “长期记忆条目生命周期”：从 Mem0 借鉴“抽取→整合→更新/冲突”的元模型

**模式**：长期记忆不是“写入一次就永远正确”。应该支持：

- 合并/去重：多次抽取到同一偏好/事实时合并，而不是堆叠
- 更新与过期：事实可能变化（住址、偏好、药物用量、订阅价格）
- 冲突与争议：不同证据给出相反结论时标注冲突状态，并要求 review

这对“5+ 年仍有用”的 IA 极关键：否则记忆会逐年变得不可信、不可用。

---

## 3) 推荐的分类/标签变更（新增/强化项）

在既有多维标签向量基础上，建议新增或强化这些维度/字段（更偏“可维护性/可解释性”）：

1) `pipeline_stage`（或 `processing_stage`）：ingest/parse/ocr/extract/review/final（用于规则、审计与调试）
2) `provenance`：采用 PROV 思路的最小三元组
   - `entity`：证据对象（file hash / message-id / uri）
   - `activity`：ingest/ocr/extract/dedupe/merge/review（带时间与参数摘要）
   - `agent`：human/tool/model（例如“人工确认”“OCR 引擎”“抽取模型版本”）
3) `claim_state`（面向“抽取出来的事实/记忆/金额/诊断”等结论类条目）：
   - candidate / confirmed / disputed / superseded / retracted
4) `validity`（适用于偏好/账户信息/药物用量等会变化的条目）：
   - `valid_from` / `valid_to` / `last_confirmed_at`
5) `evidence_priority`（用于检索与冲突解决）：
   - primary（原件/官方文件） / secondary（截图/转述） / derived（摘要/抽取）

---

## 4) 对当前结构的“提案级”schema 影响（不落地代码）

建议在 `*.meta.json`（以及 Markdown frontmatter）里统一最小字段集合，并明确“证据溯源 vs 抽取溯源”：

### 4.1 统一最小元数据（建议）

- `id`：稳定 ID（与路径解耦）
- `kind`：evidence | asset | chunk | extraction | entity_ref | event_ref | task_ref | memory_ref
- `timestamps`：`occurred_at` / `captured_at` / `ingested_at`（至少 3 时间）
- `labels`：多维标签向量（domain/source/media/semantic/...）
- `provenance.document`：证据文件的来源链（PROV entity 角度）
- `provenance.record`：本条记录/抽取的生成链（PROV activity+agent 角度）
- `evidence_refs`：引用的证据位置（文件 hash + page/offset/region/message-id…）
- `review_state`：inbox/needs_review/reviewed（与 claim_state 配合）

### 4.2 规则/工作流“只写说明书”（建议）

新增一份（或一组）规则说明文档，描述：

- triggers/filters/actions
- 每条规则的 stage 与可用字段
- 合并/覆盖语义（单值覆盖、多值合并）
- 审计/回放：规则命中后写入哪些元数据变更（以便未来实现时有据可依）

---

## 5) 风险与取舍

1) **元数据复杂度上升**：需要默认值与渐进补全策略，否则人工维护成本会很高（INBOX 审阅门仍是关键）。
2) **溯源信息的敏感性**：provenance 里可能包含设备名、路径、邮箱地址、就诊机构等；必须受 `sensitivity/sync_permission` 约束。
3) **规则阶段的学习成本**：但长期看能显著降低“为什么没命中/为什么变了”的调试成本。

---

## 6) 本次 run 结论（必须输出项）

### 推荐的 category/label 变化

- 新增：`pipeline_stage`、`provenance.(document|record)`、`claim_state`、`validity`、`evidence_priority`

### 可能的 schema 影响（提案级）

- sidecar/frontmatter 的最小字段集中引入双溯源（document vs record）与 claim 生命周期字段（candidate/confirmed/superseded…）

### 置信度

- **中高**：这些模式在 Paperless/FHIR/PROV/ActivityWatch 等成熟系统中反复出现，属于“可维护性/可解释性”的基础设施级设计。

### 隐私/安全注意事项

- provenance 与 rule audit 可能泄露敏感元数据；默认 `sync_permission=local_only`，并对医疗/财务域默认最小化索引/对外导出。

### 下一步建议调查

1) Paperless workflows 的“覆盖/合并语义”如何映射到你的 `labels`（单值 vs 多值维度的明确列表）
2) FHIR 中除了 DocumentReference，还应最小化采用哪些资源名（Encounter/Observation/Medication/Condition…）作为**命名与视图**约定（仅文档）
3) 对照片：制定“写回白名单/敏感字段策略”（例如 GPS、人脸相关字段的默认处理与导出策略）

