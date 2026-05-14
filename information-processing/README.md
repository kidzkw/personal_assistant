# Echo Information Processing Folder

This folder records Echo's personal memory database workflow.

Echo is designed as a local-first personal assistant. It preserves evidence, creates reviewable candidates, keeps high-risk data local, and requires every confirmed memory to point back to source material.

## File Structure

- `01-information-inflow.md`
  - How Echo receives local files, fake packets, and future controlled imports.
- `02-segmentation.md`
  - How Echo splits evidence into packets, chunks, messages, candidates, and projections.
- `03-data-labeling.md`
  - Echo's label vector, source membership model, review labels, and citation refs.
- `04-transition-to-db.md`
  - How Echo moves from evidence to candidates, agent results, review, and confirmed objects.
- `05-end-to-end-map.md`
  - The end-to-end workflow map for the current Echo design.
- `06-global-workflow.md`
  - The broader whole-life personal database workflow.
- `07-personal-memory-minimal-workflow.md`
  - The lightweight personal-memory version that should guide near-term implementation.
- `research/`
  - Research notes, candidate proposals, and schema ideas.

## Current Mainline

```text
file-first inbox
 -> immutable evidence/assets
 -> sidecar metadata + provenance
 -> evidence packet
 -> scope-aware candidate extraction
 -> processing/audit/proposal chain
 -> review gate
 -> confirmed domain objects
 -> entity graph + timelines + indexes
 -> permission-aware retrieval
 -> controlled sync/actions/export
```

## Current P0 Direction

- Keep raw evidence immutable.
- Treat sidecars as first-class metadata.
- Use review gates across all high-risk domains.
- Require provenance, evidence refs, and citation refs.
- Separate source membership from personal semantic labels.
- Keep timeline and daily logs as projections, not truth.
- Use `ps_agent_work_log` so the orchestrator can explain every agent-produced update.
- Keep short-lived processing/audit/proposal agents from writing confirmed truth directly.

## Runtime Entry

The current runnable scaffold lives in:

```text
runtime/
```

Validate it from the repository root:

```powershell
.\runtime\scripts\validate-dry-run.ps1
```

Expected output:

```text
DRY_RUN_OK
```
