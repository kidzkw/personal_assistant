# 2026-05-13 -- Claude / DeepSeek 信息抽象模式研究

运行时间：2026-05-13T12:00:24-04:00

## 本轮研究问题

用户要求在 GitHub 中研究 Claude 如何 abstract 信息，同时也看看 DeepSeek。目标不是实现 Claude/DeepSeek，而是提炼对 whole-life personal database 有用的信息架构模式。

本轮重点问题：

- Claude/Claude Code 生态如何处理长上下文、memory、compaction、context retrieval、handoff。
- DeepSeek 开源 repo 中的信息压缩、稀疏注意力、推理反思模式能否转译为 personal DB 结构。
- 这些模式是否应该改变当前 workflow：`file-first inbox -> immutable evidence -> sidecar/provenance -> parse/chunk -> candidate -> review -> graph/index -> retrieval/action`。

## 1. Claude：不要把 memory 做成单个大文件，而是“slim index + topic files + semantic search”

来源：

- https://github.com/anthropics/claude-code/issues/27298
- https://github.com/unclesvf/claude-memory （由上方 issue 指向的 reference implementation）

发现：

Claude Code 社区 issue 提出 layered memory：不是每次都加载完整 `MEMORY.md` / `CLAUDE.md`，而是：

- Layer 1：常驻 slim keyword index，约几十行，包含项目/主题、状态、关键词、指向 detail files 的路径。
- Layer 2：按需 topic files，用户 prompt 触发 hook 搜索 index，只加载最相关的 1-3 个 topic files。
- Layer 3：可选 semantic search，用 vector store 捕捉关键词匹配不到的相关记忆。

为什么重要：

这正好对应 personal database 的长期检索问题：不能把所有记忆、关系、医疗、财务、照片摘要都常驻给 assistant。应该常驻“索引和路标”，真正细节按需加载。

对当前结构的建议：

新增一个 `context_routing_index` 层：

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
```

它不是用户事实本身，而是帮助 assistant 决定“下一步该读哪些 topic/entity/domain 文件”的路由层。

风险/取舍：

- Index 摘要太粗会漏召回；太细又变成另一个膨胀的 memory 文件。
- 高敏感 topic 的 index 本身也可能泄露隐私，例如“oncology_visit_2026”或“divorce_lawyer”。因此 index 条目也要有 sensitivity 和 redacted title。

## 2. Claude：compaction 前需要 checkpoint，session 之间需要 handoff/event log

来源：

- https://github.com/anthropics/claude-code/issues/34556
- https://github.com/anthropics/claude-code/issues/11629
- https://github.com/anthropics/cwc-long-running-agents
- https://github.com/mkreyman/mcp-memory-keeper

发现：

Claude Code 长会话社区反复遇到 context compaction 丢细节的问题。几个反复出现的模式：

- pre-compaction / stop hook：在压缩或会话结束前保存当前发现、决策、状态变化。
- append-only changelog：每个 session 写事件流，下一 session 启动时先读。
- structured `PROGRESS.md` / handoff file：记录当前任务、已完成、待办、证据、风险。
- checkpoints：保存完整上下文快照或 priority-aware summary，可跨 session 恢复。
- parallel sessions：多个 Claude session 通过共享 memory board 交换发现。

为什么重要：

这说明 “AI working context” 本身应该被当作一种 evidence / process record，而不是临时聊天历史。对 personal database 来说，assistant 做过的抽取、判断、修正、用户反馈，也都应该进入 append-only audit/handoff 层。

对当前结构的建议：

在现有 append-only audit log 基础上，明确增加：

```yaml
assistant_handoff:
  id:
  session_id:
  created_at:
  trigger: stop | pre_compact | manual_checkpoint | scheduled_digest
  working_goal:
  decisions:
  open_questions:
  files_touched:
  evidence_seen:
  candidate_objects_created:
  review_items_pending:
  next_actions:
  confidence:

context_event_log:
  id:
  session_id:
  event_type:
  object_refs:
  summary:
  evidence_refs:
  timestamp:
```

风险/取舍：

- 如果每次 AI 操作都写日志，日志会暴涨。需要区分 `debug_trace`、`audit_event`、`handoff_summary`。
- Handoff 不能替代 evidence。它只记录工作状态，不是事实真相。

## 3. Claude：Contextual Retrieval = 给 chunk 加“所在上下文”

来源：

- https://github.com/anthropics/anthropic-cookbook
- https://github.com/anthropics/claude-cookbooks/blob/main/registry.yaml
- https://www.anthropic.com/research/contextual-retrieval
- https://www.anthropic.com/news/contextual-retrieval

发现：

Anthropic 的 contextual retrieval 模式不是只 embed 原始 chunk，而是在 chunk 前加一小段由 Claude 生成的 context，说明这个 chunk 在整篇文档里的位置和意义。Anthropic 同时建议结合 contextual embeddings、contextual BM25、reranking。其公开材料报告：加入 context、BM25、reranking 后，top-20 检索失败率明显下降。

为什么重要：

我们当前已有 chunk，但还缺一个明确的 `chunk_context` 字段。对于医疗 PDF、保险文档、银行账单、聊天导出、长邮件 thread，单个 chunk 被切出来后会失去“这是哪份文件、哪个章节、哪次就诊、哪个账期”的背景。

对当前结构的建议：

每个 chunk 旁边增加检索专用的上下文化摘要：

```yaml
content_chunk:
  id:
  parent_evidence_id:
  scope:
  aggregation_level:
  raw_text_ref:
  contextual_prefix:
  document_outline_ref:
  entity_refs:
  date_refs:
  section_path:
  page_or_region:
  embedding_policy:
  bm25_text:
```

`contextual_prefix` 是检索提示，不是事实层；必须可重新生成，并带 `generated_by` / `generated_at` / `source_prompt_version`。

风险/取舍：

- LLM 生成的 contextual prefix 可能引入解释偏差。它不能覆盖 raw chunk。
- 对高度敏感文档，不应把 prefix 送到外部 embedding；可以只做本地 BM25 或 redacted prefix。

## 4. Claude：Skills / tool-use 是“按需加载说明书”，不是常驻全局 prompt

来源：

- https://github.com/anthropics/skills/blob/main/skills/claude-api/shared/tool-use-concepts.md
- https://github.com/anthropics/claude-cookbooks/blob/main/registry.yaml

发现：

Anthropic skills 模式把任务专用说明打包在 `SKILL.md` 中，只在相关任务触发时读取全文；平时只保留短 description 在上下文中。Cookbook registry 也按 topic/path/description/category 组织教程。

为什么重要：

对 personal database，领域规则不应该全部常驻。例如医疗抽取规则、税务归档规则、关系图谱安全规则、照片 XMP 写回规则都应该是 domain playbook，按需加载。

对当前结构的建议：

新增 `domain_playbook` / `extraction_skill` 目录或对象：

```yaml
domain_playbook:
  id:
  domain:
  short_description:
  trigger_keywords:
  applies_to_scopes:
  rules_ref:
  schema_refs:
  privacy_policy_ref:
  last_reviewed_at:
```

风险/取舍：

- Playbook 过多会变成维护负担。
- 需要和 `pipeline_stage` 绑定：ingest、parse、ocr、extract、review、final 各阶段可用字段不同。

## 5. DeepSeek：MLA / compressed KV cache 启发“检索时保留 latent summary + precise evidence pullback”

来源：

- https://github.com/deepseek-ai/DeepSeek-V3
- https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py
- https://github.com/deepseek-ai/FlashMLA

发现：

DeepSeek-V3 采用 Multi-head Latent Attention（MLA）和 MoE 架构提高训练/推理效率。开源推理代码里，非 naive attention 分支不是缓存完整 per-head K/V，而是保存压缩 latent KV cache 与位置编码 cache，再在计算时恢复/组合。FlashMLA 进一步包含 dense/sparse attention kernels 和 FP8 KV cache。

这不是直接的个人数据库方案，但有一个可转译的架构启发：

- 常驻层保存“压缩的、可路由的 latent summary”。
- 需要精确回答时再回拉原始 evidence。
- 不要把完整原文常驻或全量 embed 当作默认。

对当前结构的建议：

把 retrieval index 明确分成三种 representation：

```yaml
retrieval_representation:
  exact_ref: raw evidence / chunk / page / message id
  latent_summary: short routing summary / contextual prefix / memory_observation
  sparse_keys: keywords / entities / dates / amounts / codes
```

也就是说：

```text
latent summary 负责召回
sparse keys 负责过滤
exact_ref 负责证据回拉
```

风险/取舍：

- 类比不能过度。DeepSeek MLA 是模型内部 attention 结构，不等于数据库 schema。
- 但“压缩表示不替代原始证据”这个原则非常贴合当前系统。

## 6. DeepSeek：Sparse Attention 启发“按 top-k token/object 取证，不全量上下文灌入”

来源：

- https://github.com/deepseek-ai/FlashMLA
- https://github.com/deepseek-ai/awesome-deepseek-agent

发现：

DeepSeek 的 FlashMLA repo 包含 token-level sparse attention kernels；awesome-deepseek-agent 列出了大量 agent/coding harness 集成，包括 Claude Code、Codex、Hermes、nanobot、Reasonix、DeepSeek-TUI 等。这些不是统一 memory 架构，但方向很一致：agent 框架需要模型、工具、memory、MCP、cache-first loop、skills 等组件解耦。

对当前结构的建议：

Personal DB 检索应支持 sparse evidence pullback：

```text
query
 -> route to domain/index
 -> retrieve top-k objects
 -> expand only selected evidence refs
 -> optionally expand parent/thread/session
 -> answer with citations/evidence links
```

新增字段：

```yaml
evidence_ref:
  id:
  evidence_id:
  locator_type: page | region | timestamp | message_id | attachment | line_range | photo_region
  locator:
  expansion_policy: none | parent_chunk | full_page | thread | session | document
```

风险/取舍：

- sparse pullback 可能漏上下文，所以必须允许 parent expansion。
- 医疗/财务/法律问题默认扩大到 parent page/thread/document，再回答。

## 7. DeepSeek-R1：self-verification / reflection 启发“抽取结果要有验证阶段”

来源：

- https://github.com/deepseek-ai/DeepSeek-R1

发现：

DeepSeek-R1 README 强调 RL 促发了 self-verification、reflection、long CoT 等推理能力，并通过 R1 distillation 把大型模型推理模式迁移到小模型。这里的重点不是暴露推理链，而是“模型先生成、再自检/反思”的流程。

对当前结构的建议：

在 candidate extraction 后增加一个轻量 `verification_pass`，尤其用于高风险领域：

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

这不是自动确认，而是让 review gate 更聪明：把“证据不足、冲突、低置信”的候选优先送人看。

风险/取舍：

- 自检仍然可能错，不能替代人工确认。
- 不记录隐藏推理链，只记录结构化 verification outcome。

## 推荐 category / label 变化

新增标签维度：

- `abstraction_level`: `raw | chunk | contextualized_chunk | observation | topic_summary | routing_index | domain_playbook | handoff | audit_event`
- `context_role`: `always_loaded | route_on_demand | retrieve_on_demand | evidence_pullback | archive_only`
- `compression_state`: `raw | summarized | contextualized | compacted | checkpointed | superseded`
- `retrieval_representation`: `exact_ref | sparse_keys | latent_summary | vector_embedding`
- `verification_state`: `unverified | self_checked | evidence_checked | human_confirmed | disputed`
- `expansion_policy`: `none | parent_chunk | full_page | thread | session | document`

## Proposed Schema Impact

建议新增或明确这些对象：

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

assistant_handoff:
  id:
  session_id:
  trigger:
  working_goal:
  decisions:
  open_questions:
  evidence_seen:
  candidate_objects_created:
  review_items_pending:
  next_actions:

candidate_verification:
  candidate_id:
  checked_against_evidence_refs:
  contradiction_found:
  missing_evidence:
  confidence_delta:
  recommended_review_state:

evidence_ref:
  evidence_id:
  locator_type:
  locator:
  expansion_policy:
```

## 是否改变当前 global workflow

建议小幅修改，不推翻现有结构：

当前：

```text
parse / OCR / chunk / segment
 -> scope-aware candidate extraction
 -> review gate
```

建议变为：

```text
parse / OCR / chunk / segment
 -> contextualize chunks + build routing index
 -> scope-aware candidate extraction
 -> candidate verification
 -> review gate
```

另一个横切层：

```text
assistant sessions
 -> assistant_handoff + context_event_log
 -> audit/change log
```

## 隐私 / 安全考虑

- `context_routing_index` 也可能泄露敏感主题，必须支持 redacted title 和 local_only。
- `contextual_prefix` 是 LLM 生成的检索辅助文本，不能作为事实真相，也不能覆盖 raw chunk。
- 高敏感文件默认不做外部 embedding；优先 local BM25 / exact search。
- Assistant handoff 可能记录用户偏好、项目状态和敏感文件路径，需要纳入 audit sensitivity。
- verification outcome 可以保存；不应保存完整隐藏推理链。

## 置信度

中高。

Claude 相关模式来自 Anthropic 官方 cookbook/skills repo、Claude Code issues、Anthropic long-running agents 示例和 MCP memory tools，工程模式非常贴合本项目。DeepSeek 相关模式主要是架构类比：MLA/sparse attention/self-verification 对 personal DB 有启发，但不能直接等同数据库 schema，因此作为 P1/P2 级设计启发更稳。

## 下一步调查

- 把 `06-global-workflow.md` 中 parse/chunk 与 candidate extraction 之间补上 `contextualize chunks + routing index`。
- 在 candidate proposals 中新增“context routing index”和“candidate verification pass”。
- 后续研究具体 `contextual_prefix` 的生成策略：按 document outline、email thread、medical encounter、finance statement、photo event 分别写模板。
