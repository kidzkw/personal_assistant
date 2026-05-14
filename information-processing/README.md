# Information Processing Folder

这个文件夹记录两层内容：

1. Omi 的 information processing 机制：信息如何进入、如何切分、如何打标签、如何转入数据库。
2. 在多轮研究后，面向 whole-life personal database / local-first personal assistant 的更新版全局 workflow。

Omi 分析对象：`https://github.com/BasedHardware/omi`

本地参考版本：`d2a8ea8`

## 文件结构

- `01-information-inflow.md`
  - 信息从设备、手机、桌面、第三方集成进入 Omi 的方式。
- `02-segmentation.md`
  - 音频、transcript segment、conversation、derived object 的切分逻辑。
- `03-data-labeling.md`
  - Omi 使用哪些系统标签、语义标签、speaker 标签、memory 标签和 vector metadata。
- `04-transition-to-db.md`
  - conversation、memory、action item 如何写入 Firestore 和 Pinecone。
- `05-end-to-end-map.md`
  - 把 inflow、segmentation、labeling、DB transition 串成一张完整流程图。
- `06-global-workflow.md`
  - 多轮研究后更新的 whole-life personal database 全局 workflow：file-first inbox、不可变证据、sidecar/provenance、scope-aware extraction、review gate、domain objects、entity graph、permission-aware retrieval、controlled sync/actions。
- `research/`
  - 每轮结构研究笔记、外部来源、候选提案和下一步调查方向。

## Omi 的核心判断

Omi 不是把“一天”作为原始数据库单位，而是把信息流切成多个 `conversation`。

每个 `conversation` 之后再派生出：

- `structured`：标题、摘要、类别、事件、行动项。
- `memories`：长期有用的事实或偏好。
- `action_items`：可被查询、完成、同步的任务。
- `vectors`：用于语义搜索的向量索引。

因此它的基础链路是：

```text
audio/text input
 -> transcript_segments
 -> conversation
 -> structured labels
 -> memories / action_items / events
 -> Firestore + vector DB
```

## 当前 personal database 的更新方向

多轮研究后，当前方向已经从 Omi 的 conversation-first 流程扩展为证据优先、文件优先、审阅优先的 whole-life database。

最新全局链路见 `06-global-workflow.md`：

```text
file-first inbox
 -> immutable evidence/assets
 -> sidecar metadata + provenance
 -> parse / OCR / chunk / segment
 -> scope-aware candidate extraction
 -> review gate
 -> confirmed domain objects
 -> entity graph + timelines + indexes
 -> permission-aware retrieval
 -> controlled sync/actions/export
```

当前最重要的 P0 方向：

- 统一元数据为多维标签向量，而不是单一 category。
- 证据层不可变，sidecar 元数据为一等公民。
- 全域 `review_state=inbox` 审阅门。
- provenance / audit 为一等字段。
- 字段级 authority / merge policy 显式化。
- 标签显式声明 `scope` 与 `aggregation_level`。
- 长期记忆采用 atomic `memory_observation` + typed `entity_relation` + version history。

## 个人记忆库精简入口

在用户明确补充“目标是个人记忆库，不是复杂企业级系统”之后，当前优先参考：

- `07-personal-memory-minimal-workflow.md`

这份文档把研究版 workflow 压缩成个人可维护的主干：该记哪些信息点、每类信息最低字段是什么、信息如何从 inbox 变成 evidence/candidate/memory，以及 FHIR、Perkeep claims、source snapshot、data warehouse view 等复杂模式应如何降级为个人版最小结构。
