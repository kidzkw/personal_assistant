from __future__ import annotations

import sys
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME_ROOT))

from lib.dry_run_validator import DryRunValidationError, validate_dry_run  # noqa: E402


def main() -> int:
    try:
        result = validate_dry_run(RUNTIME_ROOT)
    except DryRunValidationError as exc:
        print(f"DRY_RUN_FAILED: {exc}", file=sys.stderr)
        return 1

    print(result["message"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
