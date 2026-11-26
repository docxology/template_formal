#!/usr/bin/env python3
"""Pre-flight check for manuscript rendering prerequisites.

Thin orchestrator: all validation logic lives in
``infrastructure.rendering.preflight.run_manuscript_preflight`` (the same
helper `template_code_project/scripts/00_preflight.py` reuses). This script
only resolves paths and reports the result.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
for parent in PROJECT_ROOT.parents:
    if (parent / "infrastructure" / "rendering" / "preflight.py").is_file():
        sys.path.insert(0, str(parent))
        break

from infrastructure.rendering.preflight import run_manuscript_preflight  # noqa: E402


def main() -> int:
    manuscript_dir = PROJECT_ROOT / "docs" / "manuscript"
    ok, message = run_manuscript_preflight(manuscript_dir)
    if ok:
        return 0
    sys.stderr.write(message)
    return 1


if __name__ == "__main__":
    sys.exit(main())
