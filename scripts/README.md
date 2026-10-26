# `scripts/` — thin orchestrators

Four entry points. None of them contain business logic — every one imports a
real function from `src/template_formal/` (or shared `infrastructure/`) and
does path wiring, I/O, and printing only.

| Script | Wires up |
| --- | --- |
| [`00_setup_environment.py`](00_setup_environment.py) | Pre-flight check for manuscript rendering prerequisites. Calls `infrastructure.rendering.preflight.run_manuscript_preflight` — the same helper `template_code_project/scripts/00_preflight.py` reuses — and reports the result. |
| [`02_run_analysis.py`](02_run_analysis.py) | One call into the source-owned analysis service: `template_formal.colony.analysis.run_publication_analysis` runs the deterministic 3-agent/5-tick demo plus the N=40 seeded heterogeneous sweep (the same real harness `tests/colony/test_colony_convergence_statistics.py` uses at N=150), writes the JSON summaries, the figures, and the figure registry, and returns the artifact paths — the script prints those paths for manifest collection. |
| [`zz_generate_cover_art.py`](zz_generate_cover_art.py) | Regenerates the committed title-page cover art (`manuscript/figures/cover_colony.png`) via `template_formal.colony.cover_art.require_cover_art` — a fail-closed wrapper (unwritable destination raises rather than silently exiting) over the deterministic, seeded `generate_cover_art`. Prints the written path for manifest collection. |
| [`check_formal_specs.sh`](check_formal_specs.sh) | Runs the optional Lean 4 build (`lake build` under `formal/lean/`) and the TLA+ TLC model check (`formal/tla/`) and exits non-zero if any check fails. Fetches `tla2tools.jar` on first run from a pinned, dated GitHub release tag and verifies it against a hardcoded SHA-256 before ever invoking it. |

## Thin-orchestrator contract

Verified by reading the four scripts above: `02_run_analysis.py` is path
wiring and a print loop — it resolves the project root, calls
`template_formal.colony.analysis.run_publication_analysis(PROJECT_ROOT)`
once, and prints the artifact paths that call returns (its own docstring:
"Execute the source-owned analysis service"). `colony/demo.py`,
`colony/visualization.py`, and `colony/analysis.py` were
deliberately *moved into* `src/` from `scripts/` for exactly this reason —
see those modules' docstrings. `00_setup_environment.py`,
`zz_generate_cover_art.py` and
`check_formal_specs.sh` are the same pattern in miniature: `00_setup_environment.py`
calls one shared `infrastructure.rendering.preflight` function and reports
its result; `zz_generate_cover_art.py` calls `colony.cover_art.require_cover_art`
and prints the written path; `check_formal_specs.sh` shells out to `lake` and `java -jar
tla2tools.jar` and reports their exit codes — nothing here decides *how* a
Lean proof or a TLA+ spec is checked, only whether the process wiring
succeeded.

Concretely, if you're about to add a `def` with a loop, a conditional beyond
argument validation, or any numeric computation to a file in this directory —
stop, and put it in `src/template_formal/` (with a test) instead. A script
should read as "resolve paths, call one or two `src/` functions, print/write
the result."

## Gated by `check_template_drift.py --strict`

This contract isn't just documented, it's enforced repo-wide:

```bash
cd /path/to/template  # monorepo root
uv run python scripts/audit/check_template_drift.py --strict
```

passes clean for this project (verified this session — `template_drift: no
drift detected.`). The `--strict` flag turns on the `thin_orchestrator` check
among others; a script here that grows real business logic (rather than
calling into `src/template_formal/`) is exactly what that check exists to
catch before it ships.
