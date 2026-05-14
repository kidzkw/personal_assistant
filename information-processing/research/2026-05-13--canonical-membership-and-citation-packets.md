# 2026-05-13 15:26 EDT - Canonical Membership and Citation Packets

本轮目标：继续优化 local-first / file-first / whole-life personal database 的信息架构，但保持“个人记忆库最小可维护结构”，不引入企业级复杂度。

## 本轮读过的本地上下文

- `information-processing/README.md`
- `information-processing/06-global-workflow.md`
- `information-processing/07-personal-memory-minimal-workflow.md`
- `information-processing/03-data-labeling.md`
- `information-processing/04-transition-to-db.md`
- `information-processing/research/candidate-proposals.md`
- 自动化记忆：`$CODEX_HOME/automations/personal-db-structure-scout/memory.md`

当前方向保持不变：原始证据优先、文件优先、AI 只生成候选、高风险领域必须可回到来源、复杂标准降级为个人版最小结构。

## 外部来源

### 1. SwarmVault：raw / wiki / state 三层

来源：

- https://github.com/swarmclawai/swarmvault

发现：

- SwarmVault 在磁盘上明确拆为 `raw/`、`wiki/`、`state/`：
  - `raw/` 保存不可变来源；
  - `wiki/` 保存 LLM 生成与人工编辑的 Markdown、实体页、概念页、输出；
  - `state/` 保存 graph/retrieval/embeddings/sessions/approvals。
- 它也把新概念放入候选区，边关系标为 extracted/inferred/ambiguous，并提供 approval / conflict lint。

为什么重要：

- 上一轮已经提出 `truth/cache/export`，但个人版 `07` 还没有把这件事写进主干。
- 对个人数据库来说，最实用的降级版本不是“完整数据平台”，而是：
  - `truth`：原件、sidecar、confirmed memory objects；
  - `working`：可读的 wiki/brief/summary，用于人工浏览和纠错；
  - `cache`：FTS、OCR、thumbnail、embedding，可删除重建。

建议是否改变当前结构：

- 应改变 `07-personal-memory-minimal-workflow.md`：把“真相层 / 工作整理层 / 缓存层 / 导出层”写成个人版原则。
- 不需要现在新增应用代码或索引实现。

风险 / tradeoff：

- 如果 `wiki/brief` 被误认为真相，会让 LLM 总结污染长期记忆。
- 需要强制每个整理页标注 `built_from_refs`、`generated_at`、`review_state`，并保持 evidence pullback。

### 2. Engram：Markdown 是 source of truth，索引可重建

来源：

- https://engram-kb.org/

发现：

- Engram 使用 Markdown + YAML frontmatter 作为人类可读真相层。
- 搜索索引只是 Xapian 或 SQLite FTS5 cache，可以删除并重建。
- Typed relation 直接用 `kb://uuid#type` 这种轻量链接表达，不必先上图数据库。

为什么重要：

- 对个人记忆库，typed relation 不一定需要完整 graph DB。
- 第一版可以把 `entity_refs` / `related_refs` 写在 Markdown/frontmatter 或 sidecar 里，用本地索引生成 graph view。

建议是否改变当前结构：

- 不新增 P0 schema 大项，但强化：`entity_refs` 和 `related_refs` 可以先是轻量链接，不必强制关系表。
- 适合写入个人版最小字段说明。

风险 / tradeoff：

- Markdown 链接太自由会变乱；需要少量允许的 relation type，例如 `about_person`、`from_evidence`、`mentions_account`、`same_event_as`、`supersedes`。

### 3. Birdclaw：canonical object + account-scoped collection edges

来源：

- https://github.com/steipete/birdclaw

发现：

- Birdclaw 对 Twitter/X 归档采用本地 SQLite，保留 canonical tweets/profiles，同时用 account-scoped timeline/collection edges 表示 likes、bookmarks、mentions、DM 等集合关系。
- 它把 media/avatar 放在本地 cache root，并提供 canonical JSONL text backup。
- live 读取需要显式 `--refresh`，重复 agent 查询默认读本地 cache；actions 也有本地优先和测试禁写策略。

为什么重要：

- 这对 old/new email、聊天、照片相册、云盘文件夹、社交平台导出都非常关键：同一封邮件、同一张照片、同一个人、同一条消息，可能同时出现在多个账户、文件夹、标签、相册、导出批次里。
- 如果把“来源文件夹/相册/Gmail label/收藏夹”直接写成对象真相，会污染个人语义标签。

建议是否改变当前结构：

- 新增候选提案：`source_membership` / `collection_membership` 边。
- 这应是 P0，因为它能长期避免重复导入和标签污染。

个人版最小字段：

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
```

风险 / tradeoff：

- 多一张边表或 sidecar 数组，但比把所有来源标签混进 `tags` 更简单。
- 来源容器名可能泄露隐私，例如邮箱文件夹、聊天群名、相册名；默认继承对象敏感度，外部导出要红线裁剪。

### 4. Discrawl：通信归档的 SQLite/FTS、附件外置、Git snapshot 白名单

来源：

- https://discrawl.sh/
- https://discrawl.sh/guides/data-storage.html
- https://discrawl.sh/guides/git-snapshots.html
- https://discrawl.sh/guides/search-modes.html

发现：

- Discrawl 将 messages、attachments metadata、mentions、FTS5 放在本地 SQLite；附件二进制不放进 SQLite，只存 metadata/filename/可选 extracted text。
- 它可以把非 DM 表发布成 sharded NDJSON Git snapshots；DM 和 local-only desktop rows 不发布。
- FTS 默认可用；semantic/hybrid 需要 embedding provider/model/input_version 身份匹配。

为什么重要：

- 个人数据库也需要“发布/共享/同步白名单”：不是所有归档都能进入 export。
- 对未来 Telegram/Hermes 或家庭共享，`publish_policy` 不应只看对象类型，还应看 membership/source 容器和敏感字段。
- embedding cache 必须记录 `provider/model/input_version`，避免不同模型向量混用。

建议是否改变当前结构：

- 深化 P0-13：cache object 增加 `input_version` / `model_version`。
- 深化 source_membership：增加 publish/export policy，尤其 DM、医疗、财务、关系默认不出共享 snapshot。

风险 / tradeoff：

- 过早设计共享协议会变重；当前只需要文档约定：export 默认白名单，不共享 local_only membership。

### 5. Reddit 医疗 Obsidian/LLM wiki 讨论：引用源文件仍是最大痛点

来源：

- https://www.reddit.com/r/ObsidianMD/comments/1slqg1y/obsidian_as_a_better_personal_health_repository/

发现：

- 用户用 Obsidian + Markdown + OCR 管理复杂医疗记录时，核心痛点不是“有没有 summary”，而是：
  - OCR/解析失败；
  - LLM 不可靠地跳过文件；
  - 回到源 PDF 很麻烦；
  - 医疗隐私与云模型风险；
  - 不知道问题答案时难以验证。
- 帖子里也出现了实际目录：`wiki/` 放整理页，`raw/assets` 放源文档，`raw/assets/text` 放文本提取。

为什么重要：

- 这直接支持上一轮的 `citation_refs` 和 `evidence_packet`，但需要更个人版：
  - 不是所有 evidence 都要做复杂 packet；
  - 医疗/财务/法律/账号安全/关系类必须至少能指向 file/page/message。

建议是否改变当前结构：

- 新增候选提案：`evidence_packet` 的个人版最小字段约定。
- 把 `citation_refs` 从“高风险候选字段”扩展为“高风险 confirmed object 的准入条件”。

个人版最小字段：

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

风险 / tradeoff：

- 维护成本上升；第一版只对高风险和高价值文档强制。
- `excerpt` 本身可能包含敏感内容，必须继承原件敏感度。

## 本轮推荐的 category / label 调整

新增或强化以下标签/字段：

```yaml
storage_layer: truth | working | cache | export
artifact_role: original | sidecar | extracted_text | ocr | preview | redacted | index_record | embedding | wiki_brief
source_membership_type: source_folder | source_label | album | mailbox_folder | thread | timeline | collection | export_batch
publish_policy: local_only | private_export_ok | redacted_export_ok | share_ok
cache_identity:
  provider:
  model:
  input_version:
  generated_at:
```

已有标签应继续保留：

- `domain`
- `media_type`
- `semantic_type`
- `sensitivity`
- `review_state`
- `sync_permission`
- `occurred_at`
- `ingested_at`
- `confidence`

## Proposed schema impact

建议新增两个候选对象：

```text
source_membership
evidence_packet
```

建议扩展两个已有概念：

```text
citation_refs
cache/export metadata
```

个人版主干影响：

- `raw_evidence` / `media_asset` / `email_message` 不直接承载所有来源标签；它们连接多个 `source_membership`。
- `evidence_packet` 只用于高价值证据，不要求所有照片/文件都 packet 化。
- `working wiki/brief` 是可读整理层，不是 confirmed truth。
- embedding / FTS / OCR / thumbnail 都是 cache，要能记录生成来源并可重建。

## 隐私 / 安全考虑

- `source_membership` 可能暴露邮箱文件夹、相册名、聊天群、社交收藏、私密 DM；默认继承对象最高 sensitivity。
- Git/export/snapshot 必须使用字段白名单；DM、医疗、财务、关系、账号安全默认不发布。
- `citation_ref.excerpt` 可能复制高敏文本；外部回答只应引用必要片段，且遵守权限。
- embedding cache 必须区分 local provider 与 remote provider；远程 embedding 意味着文本或查询会出本机。
- wiki/brief 层可能含 LLM 错误，必须保留 `review_state` 和 `built_from_refs`。

## 结论

本轮有强改进：

1. 把来源容器/标签/相册/文件夹从对象标签中拆出来，建模为 `source_membership`。这能长期解决旧邮箱、新邮箱、聊天、照片相册、云盘目录和社交平台导出之间的重复与语义污染。
2. 把高价值证据组织成轻量 `evidence_packet`，让原件、OCR、预览、脱敏副本、引用定位保持在一起。
3. 把 `truth / working / cache / export` 写入个人版主干，避免 wiki、索引、embedding 或导出文件被误当成真相。

信心等级：高。来源来自近似系统的实际架构文档和 Reddit 真实痛点，且能降级为少量个人版字段。

## 下一步建议调查

- 为 `source_membership` 写 4 个示例：Gmail label、Apple Photos album、旧硬盘 folder、Telegram/Hermes thread。
- 为 `evidence_packet` 写 3 个示例：医疗 PDF、信用卡账单 PDF、截图/OCR。
- 把 `truth / working / cache / export` 的字段白名单写入 `07-personal-memory-minimal-workflow.md` 的 P0/P1 字段表。
