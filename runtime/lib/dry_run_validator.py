from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DryRunValidationError(RuntimeError):
    """Raised when the fake dry-run packet chain is internally inconsistent."""


def _read_json(root: Path, relative_path: str) -> dict[str, Any]:
    path = root / relative_path
    if not path.is_file():
        raise DryRunValidationError(f"Missing file: {relative_path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _assert_ref_exists(root: Path, relative_path: str) -> None:
    path = root / relative_path
    if not path.is_file():
        raise DryRunValidationError(f"Broken ref: {relative_path}")


def validate_dry_run(runtime_root: Path | str) -> dict[str, Any]:
    root = Path(runtime_root).resolve()

    packet = _read_json(root, "truth/sidecars/ep_fake_bill_001.meta.json")
    candidate = _read_json(root, "working/review_queue/candidate_bill_fake_001.json")
    processing = _read_json(root, "working/agent_work_log/processing_result_fake_001.json")
    audit = _read_json(root, "working/agent_work_log/audit_result_fake_001.json")
    proposal = _read_json(root, "working/agent_work_log/proposal_result_fake_001.json")
    report = _read_json(root, "working/domain_reports/domain_event_summary_report_fake_001.json")
    work_log = _read_json(root, "working/agent_work_log/pswl_fake_finance_001.json")

    evidence_packet = packet["evidence_packet"]
    candidate_item = candidate["candidate_item"]
    processing_result = processing["processing_result"]
    audit_result = audit["audit_result"]
    proposal_result = proposal["proposal_result"]
    domain_report = report["domain_event_summary_report"]
    ps_work_log = work_log["ps_agent_work_log"]

    _assert_ref_exists(root, evidence_packet["original_ref"])
    _assert_ref_exists(root, processing_result["structured_output_ref"])
    _assert_ref_exists(root, proposal_result["processing_result_ref"])
    _assert_ref_exists(root, proposal_result["audit_result_ref"])
    _assert_ref_exists(root, domain_report["processing_result_ref"])
    _assert_ref_exists(root, domain_report["audit_result_ref"])
    _assert_ref_exists(root, domain_report["proposal_result_ref"])
    _assert_ref_exists(root, ps_work_log["processing_result_ref"])
    _assert_ref_exists(root, ps_work_log["audit_result_ref"])
    _assert_ref_exists(root, ps_work_log["proposal_ref"])
    _assert_ref_exists(root, ps_work_log["domain_event_summary_report_ref"])

    if evidence_packet["packet_id"] != "ep_fake_bill_001":
        raise DryRunValidationError("Unexpected packet id")

    if candidate_item["review_state"] != "candidate":
        raise DryRunValidationError("Candidate should remain candidate during dry run")

    if audit_result["audit_decision"] != "human_review":
        raise DryRunValidationError("Financial dry run should require human_review")

    if ps_work_log["next_spawn_allowed"] is not False:
        raise DryRunValidationError("next_spawn_allowed must remain false until human review")

    if ps_work_log["current_status"] != "secretary_reported":
        raise DryRunValidationError("Expected work log status secretary_reported")

    return {
        "status": "ok",
        "message": "DRY_RUN_OK",
        "runtime_root": str(root),
        "packet_id": evidence_packet["packet_id"],
        "candidate_id": candidate_item["candidate_id"],
        "audit_decision": audit_result["audit_decision"],
        "current_status": ps_work_log["current_status"],
        "next_spawn_allowed": ps_work_log["next_spawn_allowed"],
    }
