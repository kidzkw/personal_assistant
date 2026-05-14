# Echo Personal Assistant / 个人记忆库

Echo 是一个 local-first 的个人助理和个人记忆库实验项目。当前重点不是上云，也不是复杂多 agent 平台，而是先把个人资料处理的最小闭环跑通：

```text
evidence -> sidecar -> candidate -> audit -> proposal -> review -> work log
```

当前仓库包含两类内容：

- 设计文档：`information-processing/` 和 `docs/`
- 可运行 dry run：`runtime/`

所有示例数据都是 fake data。不要把真实医疗、财务、账号安全、关系、证件或私人文件提交到这个仓库。

## 快速开始

Clone 后进入仓库根目录：

```powershell
git clone https://github.com/kidzkw/personal_assistant.git
cd personal_assistant
```

运行当前 dry run：

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

预期输出：

```text
DRY_RUN_OK
```

这说明当前 fake packet 的引用链是完整的：

- evidence packet 能找到原始 fake evidence
- candidate 保持在 reviewable 状态
- processing result 指向 candidate
- audit result 对 financial 类型要求 human review
- proposal result 没有直接写 confirmed truth
- `ps_agent_work_log.next_spawn_allowed=false`，直到 review 完成

## 本地 Docker Server

仓库现在包含一个最小 Docker server，用来在本机通过 HTTP 验证当前 dry-run workflow。它不会导入真实个人数据，也不会运行自治 agent。

在仓库根目录启动：

```powershell
docker compose up --build
```

然后检查：

```powershell
curl.exe http://localhost:8080/health
curl.exe http://localhost:8080/dry-run
```

也可以直接打开浏览器 dashboard：

```text
http://localhost:8080/
```

要把信息发给 Echo，可以用 dashboard 里的 "Inbox Dropbox" 区域。你可以拖文件、选择文件、粘贴截图/照片，也可以输入文本。文本会写入 `runtime/inbox/text/`；文件和照片会写入 `runtime/inbox/files/`。状态保持为 `review_state=inbox`；这还不是 confirmed memory。

文本 API 示例：

```powershell
$body = @{
  title = "Test note"
  text = "Remember to review the fake bill workflow."
  sensitivity = "personal"
} | ConvertTo-Json -Compress

Invoke-RestMethod `
  -Uri http://localhost:8080/inbox/text `
  -Method Post `
  -ContentType "application/json; charset=utf-8" `
  -Body $body
```

列出收到的 inbox items：

```powershell
curl.exe http://localhost:8080/inbox
```

文件和照片建议直接用浏览器 dashboard，因为它会帮你处理本地文件读取。

`/dry-run` 的预期响应包含：

```json
{
  "status": "ok",
  "message": "DRY_RUN_OK"
}
```

停止服务：

```powershell
docker compose down
```

不用 Docker Compose 也可以：

```powershell
docker build -t echo-personal-assistant:local .
docker run --rm -p 8080:8080 echo-personal-assistant:local
```

## 如何使用当前 Runtime

当前 runtime 还不是完整应用，而是一个文件式 dry-run scaffold。它用纯文本和 JSON 模拟第一条个人记忆处理链路。

主要入口：

```text
runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt
runtime/truth/sidecars/ep_fake_bill_001.meta.json
runtime/working/review_queue/candidate_bill_fake_001.json
runtime/working/agent_work_log/pswl_fake_finance_001.json
runtime/scripts/validate-dry-run.ps1
```

读链路时按这个顺序看：

```text
1. raw evidence
   runtime/truth/raw_evidence/ev_fake_credit_card_bill_2026_05.txt

2. evidence packet sidecar
   runtime/truth/sidecars/ep_fake_bill_001.meta.json

3. reviewable candidate
   runtime/working/review_queue/candidate_bill_fake_001.json

4. processing result
   runtime/working/agent_work_log/processing_result_fake_001.json

5. audit result
   runtime/working/agent_work_log/audit_result_fake_001.json

6. proposal result
   runtime/working/agent_work_log/proposal_result_fake_001.json

7. domain event summary report
   runtime/working/domain_reports/domain_event_summary_report_fake_001.json

8. PS work log
   runtime/working/agent_work_log/pswl_fake_finance_001.json
```

目前新增 fake packet 的方式是手动复制这些 JSON 形状。下一步会做 CLI，把这个过程变成命令。

## Agent Chain

当前 agent flow 是串行的，不允许短生命周期 agent 自己乱跑。

```text
总管 / orchestrator
  -> 分派 work item 给小秘

小秘 / secretary_agent
  -> 启动一条 active processing/audit/proposal chain

processing_agent
  -> 只处理一个小 evidence packet
  -> 输出 processing_result

audit_agent
  -> 检查 processing_result、citation、scope boundary、risk flags
  -> 输出 audit_result

proposal_agent
  -> 根据 processing_result + audit_result 生成
     review_result / update_proposal / no_action
  -> 输出 proposal_result

小秘 / secretary_agent
  -> 生成 domain_event_summary_report
  -> report 给总管

总管 / orchestrator
  -> 更新 ps_agent_work_log
  -> 决定 next_spawn_allowed
```

重要边界：

- `processing_agent` 不写 truth layer
- `audit_agent` 不做最终业务判断
- `proposal_agent` 不直接写 confirmed memory
- 小秘负责领域汇总
- 总管负责全局 work log 和下一步解锁
- 医疗、财务、法律、账号安全、关系信息默认 `local_only` + `review_required`

## 仓库结构

```text
docs/
  Echo 信息处理设计笔记和参考材料

information-processing/
  个人记忆库 workflow、candidate proposals、research notes

runtime/
  当前可运行 dry-run scaffold
```

Runtime 目录：

```text
runtime/
  truth/
    raw_evidence/        # 原始证据或 fake evidence
    sidecars/            # evidence packet / metadata
    confirmed_objects/   # 未来 confirmed memory objects
  working/
    review_queue/        # candidates waiting for review
    agent_work_log/      # processing/audit/proposal/work log
    domain_reports/      # 小秘给总管的 summary report
  cache/
    ocr/                 # 可重建 OCR cache
    fts/                 # 可重建 search cache
  export/                # 未来导出层
  scripts/               # local commands
```

## 当前命令

验证 dry run：

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

检查仓库状态：

```powershell
git status -sb
```

当前不需要安装步骤。

## 当前状态

已完成：

- 文档骨架
- local runtime 文件夹结构
- fake financial evidence packet
- evidence packet sidecar
- candidate item
- processing / audit / proposal result 示例
- domain event summary report
- PS agent work log 示例
- dry-run validation script
- 带 `/health` 和 `/dry-run` 的最小 Docker server
- `POST /inbox/text` 本地文本 inbox endpoint
- `POST /inbox/file` 本地文件 / 照片 inbox endpoint

未完成：

- 文件 / 邮件 / 图片等真实 inbox ingestion
- 创建 packet 的 CLI
- SQLite index
- OCR
- web UI
- 真实 agent runner
- Gmail、Google Calendar、Telegram、Hermes 或 cloud storage 同步
- 带真实 worker / OCR 依赖的生产级 Docker packaging

## 路线图

### Phase 0: Static Dry Run

状态：当前阶段。

目标：只用 fake data，让记忆处理 workflow 可以被检查。

里程碑：

- 保持 fake evidence packet chain 有效
- 保持 `validate-dry-run.ps1` 通过
- 在 schema 还便宜的时候继续调整 JSON 形状

### Phase 1: Tiny CLI

目标：停止手写每个 fake packet。

计划命令：

```powershell
personal-db new-fake-packet --type bill
personal-db validate
personal-db show-work-log
personal-db list-review-queue
```

第一版可以用 PowerShell 或 Python。它仍然应该写 plain files，不要一上来变成 database-first system。

### Phase 2: SQLite Index

目标：让 lookup 和 review queue navigation 更轻松，但不让 SQLite 变成 truth layer。

SQLite 应该索引：

- evidence packets
- candidates
- processing / audit / proposal results
- PS work logs
- review queue status

Truth 仍然是文件层。

### Phase 3: Review Queue

目标：让 human review 可操作。

需要支持：

- 列出 candidates
- 显示 citation refs
- approve / correct / reject / archive
- 保持 review result 可追溯
- 不自动确认高风险领域

### Phase 4: Real Ingestion

目标：fake flow 稳定到无聊之后，再导入受控本地文件。

可能的第一批 ingester：

- local text file
- local PDF metadata-only packet
- screenshot / image metadata packet
- email export packet

仍然不做自动医疗、财务、法律或账号安全决策。

### Phase 5: Local App Or Backend

目标：文件 workflow 稳定后，再加一个小型 local UI 或 API。

可能技术栈：

- Python FastAPI
- Next.js local dashboard
- SQLite + FTS5
- local filesystem storage

### Phase 6: Docker Compose

状态：已经有最小本地 server scaffold。

目标：只有当项目真的有更重的依赖时，再做更完整的 Docker packaging。

Docker 在这些东西出现后会更有价值：

- backend service
- worker process
- OCR dependency
- local search service
- repeatable development environment

在那之前，Docker 主要只是把简单文件行为藏进 container volume 权限里。

## 安全规则

不要提交真实个人数据。

绝对不要 commit：

- medical records
- financial statements
- legal documents
- credentials
- account-security notices
- private relationship notes
- identity documents
- real email exports
- real chat exports
- real photos with GPS/person metadata

推荐把未来真实本地实验放在这些已被 git ignore 的目录：

```text
runtime/local/
runtime/private/
runtime/inbox/
```

这些目录可以以后用于真实本地实验，但不要进入 GitHub。
