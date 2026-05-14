# Personal Assistant / Personal Memory Database

一个 local-first 的个人记忆库实验项目。当前重点不是上云、不是复杂多 agent 平台，而是先把个人资料处理的最小闭环跑通：

```text
evidence -> sidecar -> candidate -> audit -> proposal -> review -> work log
```

当前仓库包含两类内容：

- 设计文档：`information-processing/` 和 `docs/`
- 可运行 dry run：`runtime/`

所有示例数据都是 fake data。不要把真实医疗、财务、账号安全、关系、证件或私人文件提交到这个仓库。

## Quick Start

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

## How To Use The Current Runtime

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

## Repository Layout

```text
docs/
  Omi 信息处理分析和外部系统参考

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

## Current Commands

Validate the dry run:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Check repository status:

```powershell
git status -sb
```

No install step is required yet.

## Current Status

Done:

- documentation scaffold
- local runtime folder layout
- fake financial evidence packet
- evidence packet sidecar
- candidate item
- processing/audit/proposal result examples
- domain event summary report
- PS agent work log example
- dry-run validation script

Not done:

- real inbox ingestion
- CLI for creating packets
- SQLite index
- OCR
- web UI
- real agent runner
- sync with Gmail, Google Calendar, Telegram, Hermes, or cloud storage
- Docker Compose

## Roadmap

### Phase 0: Static Dry Run

Status: current.

Goal: make the memory workflow inspectable with fake data only.

Milestones:

- Keep fake evidence packet chain valid
- Keep `validate-dry-run.ps1` passing
- Refine JSON schemas while they are still cheap to change

### Phase 1: Tiny CLI

Goal: stop hand-writing every fake packet.

Planned commands:

```powershell
personal-db new-fake-packet --type bill
personal-db validate
personal-db show-work-log
personal-db list-review-queue
```

First version can be PowerShell or Python. It should still write plain files, not a database-first system.

### Phase 2: SQLite Index

Goal: make lookup and review queue navigation easier without making SQLite the truth layer.

SQLite should index:

- evidence packets
- candidates
- processing/audit/proposal results
- PS work logs
- review queue status

Truth remains the file layer.

### Phase 3: Review Queue

Goal: make human review practical.

Needed behavior:

- list candidates
- show citation refs
- approve / correct / reject / archive
- keep review result traceable
- do not auto-confirm high-risk domains

### Phase 4: Real Ingestion

Goal: import controlled local files after fake flow is boringly reliable.

Possible first ingesters:

- local text file
- local PDF metadata-only packet
- screenshot / image metadata packet
- email export packet

Still no automatic medical, financial, legal, or account-security decisions.

### Phase 5: Local App Or Backend

Goal: add a small local UI or API only after the file workflow is stable.

Possible stack:

- Python FastAPI
- Next.js local dashboard
- SQLite + FTS5
- local filesystem storage

### Phase 6: Docker Compose

Goal: package dependencies only when there is something worth packaging.

Docker becomes useful when we have:

- backend service
- worker process
- OCR dependency
- local search service
- repeatable development environment

Until then, Docker would mostly hide simple file behavior behind container volume permissions.

## Safety Rules

Do not commit real personal data.

Never commit:

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

Recommended local-only folders are ignored by git:

```text
runtime/local/
runtime/private/
runtime/inbox/
```

Use those folders later for real local experiments, but keep them out of GitHub.
