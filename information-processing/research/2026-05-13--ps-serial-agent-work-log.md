# 2026-05-13 17:49 EDT - PS 总管串行 agent work log

本轮问题：总管如何维护一个串行 agent work log，使每个小秘在上一条 processing/audit/proposal chain 被记录和跟踪之前，不会启动下一条 chain？

## 本轮读取的本地上下文

- `information-processing/07-personal-memory-minimal-workflow.md`
- `information-processing/06-global-workflow.md`
- `information-processing/research/candidate-proposals.md`
- 最近 research notes：
  - `2026-05-13--raw-samples-vs-semantic-activity-projections.md`
  - `2026-05-13--timeline-projections-and-temporal-uncertainty.md`
  - `2026-05-13--canonical-membership-and-citation-packets.md`
  - `2026-05-13--local-archive-index-cache-and-medical-citation-loop.md`
- automation memory：`$CODEX_HOME/automations/personal-db-structure-scout/memory.md`

## 当前缺口

现有主干已经有 review gate、candidate verification、assistant handoff/context log、evidence packet/citation、truth/working/cache/export 分层。但 agent workflow 还缺一个明确的“串行门闩”：

- 总管已经被设想为唯一总调度层，但还没有最小字段约束说明它如何持有全局 work log。
- 小秘被设想为长期 domain steward，但还没有明确记录 `active_chain_id` 或 `next_spawn_allowed`。
- 短生命周期 agent 需要拆成 processing / audit / proposal 三个角色，否则“处理、审计、生成提案”的职责会糊在一起。
- 如果没有这个约束，小秘可能在上一条 chain 尚未审查、写 log、排 next step 之前继续 spawn，导致候选项重复、引用丢失、冲突无法解释。

## 个人版最小结构

不要做企业级任务队列、分布式锁、多 agent 平台。个人记忆库只需要一个由总管维护的 append-only `ps_agent_work_log`，加上小秘的单个 active chain 指针。

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
  next_spawn_allowed: false
  processing_result_ref:
  audit_result_ref:
  proposal_ref:
  baton_ref:
  domain_event_summary_report_ref:
  recommended_next_step:
  risk_level:
  sensitivity:
```

长期 agent 只需要维护一个很小的 domain queue：

```yaml
domain_agent_queue:
  secretary_agent:
  active_chain_id:
  active_work_log_id:
  queued_work_item_refs:
  blocked_reason:
  next_spawn_allowed:
```

短生命周期 agent 的返回结果必须能直接被小秘串接、审查并交还总管：

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

## 串行门闩规则

同一个小秘同一时间只能有一条 active processing/audit/proposal chain。解锁下一次 spawn 必须满足四个条件：

1. processing agent 已返回 `processing_result`。
2. audit agent 已返回 `audit_result`，明确 citation、scope boundary、risk flags 是否通过。
3. proposal agent 已返回 `proposal_result`，小秘已生成 `domain_event_summary_report` 并 report 给总管。
4. 总管把 `ps_agent_work_log.current_status` 更新为 `secretary_reported` 或 `closed`，并显式把该小秘的 `next_spawn_allowed` 设为 `true`。

如果 processing/audit/proposal 任一环失败、证据不足或越界，也不能静默继续。必须写：

```yaml
current_status: blocked
blocked_reason:
recommended_next_step: retry_with_smaller_packet | request_human_review | archive_no_action | create_update_proposal
```

## 推荐进入候选提案

### P0：`ps_agent_work_log` + `domain_agent_queue` 串行门闩

这是 P0，不是因为它复杂，而是因为它保护个人记忆库的可解释性。任何小秘只要能连续 spawn 短生命周期 agent chain 而不先记录结果，就会破坏“为什么这条记忆被写入/更新”的基本要求。

### P1：统一 `processing_result / audit_result / proposal_result` 最小输出 schema

这是 P1。它重要，但可以先作为约定存在，不需要实现 runner。第一版只要求 processing、audit、proposal 三类中间结果有 refs、citation、decision 和 recommended_next_step。

### P2：复杂调度、并行队列、跨 agent 优先级优化

暂不进入个人版主干。PS 总管可以人工/半自动排队，不需要做企业级 scheduler。

## 和当前主干的关系

- 不改变 truth layer：短生命周期 agent 输出不是 truth，只能生成 processing_result、audit_result、proposal_result。
- 不改变 review gate：医疗、财务、法律、账号安全、关系信息仍默认 review_required / local_only。
- 不保存短生命周期 agent 长上下文：只保存结构化结果、citation_refs、baton 和 work log 状态。
- current view/history 仍由 confirmed object 与 update_proposal/change_log 维护，agent work log 只解释处理过程。

## 下一轮建议

下一轮可以继续细化 `update_proposal`：把 `add_detail / correct_detail / reschedule / cancel / complete / split / merge / supersede / retract` 的适用条件、review gate 和 current view/history 影响写成一张个人版决策表。
