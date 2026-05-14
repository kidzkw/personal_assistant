# Echo Information Processing

这个文件夹记录 Echo 的个人记忆库信息处理设计：信息如何进入、如何被切成可审阅对象、如何保留证据引用、如何通过 agent 链生成候选更新，以及最终如何进入个人记忆库。

目标不是做企业级多 agent 平台，而是做一个 local-first、file-first、可解释、可回源的个人 assistant workflow。

## 文件结构

- `01-information-inflow.md`
  - Echo 如何接收 manual note、local file、email export、image/screenshot、未来 audio 等输入。
- `02-segmentation.md`
  - Echo 如何把输入拆成 evidence packet、candidate、object brief 和 projection。
- `03-data-labeling.md`
  - Echo 的最小标签、source membership、citation refs、review labels 和安全标签。
- `04-transition-to-db.md`
  - Echo 如何从 evidence 过渡到 candidate、processing/audit/proposal、review gate 和 confirmed memory。
- `05-end-to-end-map.md`
  - Echo 的端到端信息处理图。
- `06-global-workflow.md`
  - 多轮研究后的 whole-life personal database 全局 workflow。
- `07-personal-memory-minimal-workflow.md`
  - 当前最优先的个人版最小 workflow。
- `research/`
  - 每轮结构研究笔记、外部来源、候选提案和下一步调查方向。

## 当前主干

Echo 的核心链路是：

```text
inbox
 -> raw evidence / asset
 -> evidence packet sidecar
 -> reviewable candidate
 -> processing_result
 -> audit_result
 -> proposal_result
 -> domain_event_summary_report
 -> ps_agent_work_log
 -> human review
 -> confirmed memory object
```

最重要的边界：

- raw evidence 不被覆盖。
- sidecar 和 citation refs 是一等对象。
- working layer 里的 summary、timeline、index、agent output 都不是 truth。
- confirmed memory 必须能回到 evidence refs / citation refs。
- 医疗、财务、法律、账号安全、关系信息默认 `local_only` + `review_required`。
- 短生命周期 agent 不直接写 confirmed truth。

## Agent Flow

当前 agent flow 是串行的：

```text
总管 / orchestrator
  -> 分派 work item 给小秘 / secretary_agent

小秘 / secretary_agent
  -> 启动一条 active processing/audit/proposal chain

processing_agent
  -> 只处理一个小 evidence packet
  -> 输出 processing_result

audit_agent
  -> 审查 processing_result、citation refs、scope boundary、risk flags
  -> 输出 audit_result

proposal_agent
  -> 根据 audit_result 生成 review_result / update_proposal / no_action
  -> 输出 proposal_result

小秘 / secretary_agent
  -> 生成 domain_event_summary_report 给总管

总管 / orchestrator
  -> 更新 ps_agent_work_log
  -> 决定 next_spawn_allowed
```

这个结构的目的不是让 agent 自治，而是让每一步处理都能解释：谁处理了什么证据、生成了什么候选、谁审查过、为什么允许或不允许进入下一步。
