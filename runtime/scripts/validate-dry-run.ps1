$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

function Read-JsonFile($relativePath) {
  $path = Join-Path $root $relativePath
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Missing file: $relativePath"
  }
  return Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
}

function Assert-RefExists($relativePath) {
  $path = Join-Path $root $relativePath
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Broken ref: $relativePath"
  }
}

$packet = Read-JsonFile "truth/sidecars/ep_fake_bill_001.meta.json"
$candidate = Read-JsonFile "working/review_queue/candidate_bill_fake_001.json"
$processing = Read-JsonFile "working/agent_work_log/processing_result_fake_001.json"
$audit = Read-JsonFile "working/agent_work_log/audit_result_fake_001.json"
$proposal = Read-JsonFile "working/agent_work_log/proposal_result_fake_001.json"
$report = Read-JsonFile "working/domain_reports/domain_event_summary_report_fake_001.json"
$workLog = Read-JsonFile "working/agent_work_log/pswl_fake_finance_001.json"

Assert-RefExists $packet.evidence_packet.original_ref
Assert-RefExists $processing.processing_result.structured_output_ref
Assert-RefExists $proposal.proposal_result.processing_result_ref
Assert-RefExists $proposal.proposal_result.audit_result_ref
Assert-RefExists $report.domain_event_summary_report.processing_result_ref
Assert-RefExists $report.domain_event_summary_report.audit_result_ref
Assert-RefExists $report.domain_event_summary_report.proposal_result_ref
Assert-RefExists $workLog.ps_agent_work_log.processing_result_ref
Assert-RefExists $workLog.ps_agent_work_log.audit_result_ref
Assert-RefExists $workLog.ps_agent_work_log.proposal_ref
Assert-RefExists $workLog.ps_agent_work_log.domain_event_summary_report_ref

if ($packet.evidence_packet.packet_id -ne "ep_fake_bill_001") {
  throw "Unexpected packet id"
}

if ($candidate.candidate_item.review_state -ne "candidate") {
  throw "Candidate should remain candidate during dry run"
}

if ($audit.audit_result.audit_decision -ne "human_review") {
  throw "Financial dry run should require human_review"
}

if ($workLog.ps_agent_work_log.next_spawn_allowed -ne $false) {
  throw "next_spawn_allowed must remain false until human review"
}

if ($workLog.ps_agent_work_log.current_status -ne "secretary_reported") {
  throw "Expected work log status secretary_reported"
}

"DRY_RUN_OK"
