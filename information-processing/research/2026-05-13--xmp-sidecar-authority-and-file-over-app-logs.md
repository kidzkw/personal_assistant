# 2026-05-13 照片 XMP sidecar 的“字段权威/合并语义”与 File-over-App 变更日志（GitHub/Reddit）

目标：在不写应用代码的前提下，补强“local-first + file-first inbox + 保留原始证据”的长期 IA：把**元数据冲突/合并**与**审计/同步（未来）**这两个容易在 5+ 年里失控的点先文档化。

## 0. 本地现状对齐（本仓库）

已确立的主方向（来自本仓库 `information-processing/*` 与 `docs/omi-information-processing-analysis.md`）：

- 三层分离：**证据层（Evidence）→ 理解层（Understanding）→ 行动/检索层（Action & Retrieval）**
- 统一标签向量（domain/source/media/semantic/...）+ `review_state=inbox` 审阅门
- “证据层不可变 + sidecar 元数据一等公民”（照片优先 XMP，其它 `*.meta.json`）

本次研究重点不是扩展领域清单，而是把 **“谁是字段真相（authority）”** 与 **“多来源如何合并（merge policy）”** 写清楚，以避免未来导入/编辑/同步时出现不可解释的覆盖。

## 1. 关键外部来源（本次新增/加深）

### 1.1 PhotoPrism：XMP 的两条解析路径与 sidecar 读法限制（强信号）

- PhotoPrism「Adobe XMP」（2026-04-27 更新）：https://docs.photoprism.app/developer-guide/metadata/xmp/
  - 重点：**embedded XMP 走 ExifTool（主路径）** vs **`.xmp` sidecar 走内置 reader（PoC）**；两条路径覆盖字段与 fallback 机制不同。

### 1.2 Immich：sidecar 写回是“合并”而非“整文件替换”

- Immich「XMP Sidecars」：https://docs.immich.app/features/xmp-sidecars/
  - 重点：写回会与已有字段合并；对日期/标签等字段有**优先级顺序**；命名规则（`IMG_0001.jpg.xmp` 优先）；DISCOVER/SYNC 作业；外部库只读时写回可能失败。

### 1.3 Receipts Space / Receipts App：文件格式先行的“变更日志 + 资产引用”设计

- Receipts Space 文档（简版）：https://receipts-space.com/en/docs
- Receipts App 文档（详版，含链式校验/可选加密）：https://receipts-app.com/en/docs
  - 重点：`info.json` + `transactions/`（append-only JSON/JSONL log）+ `assets/`（二进制附件）；用 `_v`（Lamport clock）做 LWW；可选 `p` 链式哈希保证篡改可检；资产以 `asset:///...?...` URL 形式携带 checksum/size/mime/name。

### 1.4 Reddit：超大“人生根目录 + Obsidian vault”实践的踩坑点

- r/ObsidianMD（Johnny Decimal + 1TB 根目录 vault）：https://www.reddit.com/r/ObsidianMD/comments/1hydhgz/
  - 重点：**笔记/索引**（高频变更）更适合进 Git；大体量二进制证据不适合进 Git；建议把两类东西物理分离。

### 1.5 Reddit：Immich / Paperless-ngx / Nextcloud “同一底层存储，多应用视图”常见组合

- r/selfhosted：Nextcloud + Immich + Paperless-ngx：https://www.reddit.com/r/selfhosted/comments/1lm0rex/nextcloud_immich_paperlessngx/
- r/selfhosted：“Immich for documents?”（大量讨论 tags vs folders、OCR、落盘策略）：https://www.reddit.com/r/selfhosted/comments/1sdx0jn/is_there_an_immich_for_documents/

## 2. 本次发现的“可落地模式”

### 2.1 照片/媒体：必须显式区分字段的 **来源（origin）**、**权威（authority）**、**合并策略（merge policy）**

PhotoPrism 的 XMP 文档非常关键：它明确指出“XMP 看似一个标准”，但现实中会因为**解析路径不同**导致同一字段是否可用、fallback 是否发生、GPS/时间等是否被正确读取都不同（尤其 `.xmp` sidecar 的内置 reader 仍是 PoC）。这意味着我们在 IA 里不能只写“支持 XMP”，而需要在**元数据层**写清楚：

- **同一个“逻辑字段”可能有多个别名来源**（例如 dc:title vs photoshop:Headline vs IPTC:Headline），必须定义“优先级列表”。
- **同一个逻辑字段会被多个系统写入**（相机嵌入、Lightroom/digiKam sidecar、我们的 sidecar、未来可能的同步器），必须定义“谁赢”。
- 写回（write-back）本质上是一个**冲突系统**：Immich 明确是“合并写回”，而不是覆盖整文件；同时也提示了“只读库”会导致写回失败甚至无提示的风险。

结论：我们应当把“照片 metadata”当成**多来源合并的字段集合**，而不是一个扁平 JSON。

### 2.2 证据/元数据变更：用“append-only 变更日志”把审计与未来同步前置成格式问题

Receipts 的“File Over App”格式给了一个可直接借鉴的模板：

- `info.json` 声明 workspace 版本/类型/创建时间（甚至加密配置）
- `transactions/`：每条变更都是 append-only 的 log entry（JSONL），可加 checksum；可选链式哈希（`p`）做篡改检测
- `assets/`：二进制附件独立存放；引用把 checksum/size/mime/name 编进 URL，从而“引用即校验”

这对个人全生命周期数据库很重要，因为我们未来一定会遇到：

- 多工具写同一份 sidecar 元数据（冲突）
- 离线设备/外部硬盘/同步盘导致的“先后顺序不确定”
- 需要回答“这个字段什么时候被谁改了、依据是什么”

结论：即便当前不做跨设备同步，也值得先在文档里定义**审计日志格式**与**资产引用格式**，让未来的同步/回滚/导出更可控。

### 2.3 结构分层：把“变更频繁的文字索引/规则”与“体量巨大的证据资产”物理分离

Reddit 的 Obsidian + 超大根目录讨论指出：把 1TB+ 的人生文件直接当 vault 会带来版本管理/性能/备份策略的复杂度；更稳的做法是：

- 文字索引/规则/提案：小、可 git、可回滚
- 证据资产（照片/扫描件/附件）：大、不可变、用校验与 sidecar 关联

结论：我们在 IA 上应把“索引层（notes / schemas / proposals）”与“证据层（assets/evidence）”作为**两种不同的存储单元**写清楚（即便都在同一根目录下）。

## 3. 对当前 IA 的具体改动建议（仅文档/结构层面）

### 3.1 分类/标签（对应设计区 1 + 2）

新增/强化三组通用字段（建议纳入 `labels` 或 sidecar 最小 schema）：

- `field_origin`：字段来自哪里（embedded_exif/xmp、sidecar_xmp、sidecar_json、ocr、llm_extract、manual、import_script…）
- `field_authority`：当多来源冲突时谁是“默认真相”（例如 photos: sidecar_xmp > embedded；docs: sidecar_json > pdf_text_ocr）
- `field_merge_policy`：覆盖/合并策略（single_value_lww、multi_set_union、priority_list_first_non_empty、append_only_log…）

并把这些与既有维度绑定：

- `pipeline_stage`（ingest/parse/ocr/extract/review/final）决定字段是否“可依赖”
- `sync_permission` 决定哪些字段允许跨设备/跨应用传播（例如 GPS/人脸/医疗信息默认禁止）

### 3.2 照片/媒体管线（对应设计区 3）

把“XMP 支持”改写成一页**白名单 + 优先级 + 写回策略**：

- 白名单：只写回少数跨工具通用字段（例如 description、rating、tags、datetime、location），其他保持只读或仅存在于 `*.meta.json`
- 优先级：显式列出每个逻辑字段的“别名优先级列表”（参考 Immich 的 prioritized order 与 PhotoPrism 的 alias 概念）
- 写回许可：区分 `writeback_enabled`（能否写 sidecar）与 `index_refresh`（何时重读 sidecar）；并记录写回失败的可观测性（避免 silent fail）

### 3.3 财务/票据与 life admin（对应设计区 5 + 9）

引入 Receipts 模式作为“未来可选的审计/同步层”：

- 为 finance/life-admin 证据定义 `asset://` 引用格式（checksum/size/mime/name 内嵌），确保“引用即校验”
- 为结构化条目（bill/receipt/subscription/deadline）定义 append-only `transactions/`（仅文档约定即可），把“变更历史/纠错/撤销”落在格式层

### 3.4 分割/过渡与检索（对应设计区 6 + 7 + 8）

- 分割（segmentation）时把“字段可用性”作为一等信息：OCR 未完成/EXIF 未提取/sidecar 未同步时，抽取的事实只能处于 `claim_state=candidate`
- 检索时默认“证据回拉”：任何结论都能追溯到 `evidence_ref`（file hash + page/region/message-id），并受 `sync_permission`/`sensitivity` 限制

## 4. 是否建议改动当前结构？

结论：**建议**，但只做“文档约定”层面的增量：

1) 在候选 schema（sidecar/frontmatter）里补齐 `field_origin/authority/merge_policy`  
2) 写一页“照片 XMP 字段白名单 + 优先级 + 写回策略”  
3) 增补一页“append-only 变更日志 + asset 引用格式（Receipts 风格）”作为未来同步/审计的格式预案  

不建议此刻引入真正的同步/加密/执行器实现（保持 research-only）。

## 5. 风险与取舍

- **复杂度上升**：字段级 authority/merge 会让 schema 更复杂；但它能显著降低未来导入/编辑/同步时的不可解释性。
- **隐私泄露面**：metadata（如 GPS、机构名、邮箱、设备名）本身可能比正文更敏感；需要默认最小化 + `sync_permission` 严格限制。
- **加密并非银弹**：Receipts 文档提示“文件名仍可见”；即使加密内容，目录结构/文件名/时间戳也可能泄露，需要在 IA 层把“可见面”写清楚。

## 6. 本次 run 的输出（对 9 个设计区的映射）

- 1）分类 taxonomy：新增 `field_origin/authority/merge_policy`（跨域通用）
- 2）数据 labeling：为每个抽取结果附带字段级 provenance + `claim_state/validity`
- 3）照片管线：从“支持 XMP”升级到“白名单/优先级/写回/失败可观测性”
- 5）email/life admin：借鉴 Receipts 的资产引用与审计日志（先文档化）
- 6/7）分割与过渡：把“字段可用性/阶段”当成结构的一部分
- 8）检索与使用：默认证据回拉 + 权限感知检索
- 9）隐私与耐久：append-only 日志 + checksum/链式校验 + 可选全仓加密（仅规范）

## 7. 下一步值得研究

- 把“照片字段优先级列表”具体化成一张表：逻辑字段 → XMP/EXIF/IPTC 别名优先级 → 写回白名单 → 敏感策略（GPS/人脸）
- 定义通用 `asset://` 引用规范与 `transactions/` 的最小 JSONL 变更记录字段（不实现，只定格式）
- 进一步收集“多工具写 sidecar”时的冲突案例（Lightroom/digiKam/Immich/PhotoPrism 混用），提炼默认 merge 策略

