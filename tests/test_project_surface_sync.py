import re
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_experiment_plan_figures_are_referenced_by_the_manuscript() -> None:
    plan = yaml.safe_load((PROJECT_ROOT / "experiment_plan.yaml").read_text(encoding="utf-8"))
    expected = set(plan["expected_figures"])
    manuscript = (PROJECT_ROOT / "docs" / "manuscript" / "05_results_discussion.md").read_text(encoding="utf-8")
    referenced = set(re.findall(r"\{#(fig:[^}]+)\}", manuscript))
    assert expected == referenced == {"fig:demo-convergence", "fig:convergence-tick-distribution"}


def test_live_fixture_and_documentation_surfaces_are_synchronized() -> None:
    bad_fixtures = sorted((PROJECT_ROOT / "tests" / "mypy_fixtures").glob("bad_*.py"))
    good_fixtures = sorted((PROJECT_ROOT / "tests" / "mypy_fixtures").glob("good_*.py"))
    assert len(bad_fixtures) == 6
    assert len(good_fixtures) == 3

    abstract = (PROJECT_ROOT / "docs" / "manuscript" / "00_abstract.md").read_text(encoding="utf-8")
    tests_readme = (PROJECT_ROOT / "docs" / "reference" / "tests" / "README.md").read_text(encoding="utf-8")
    results = (PROJECT_ROOT / "docs" / "manuscript" / "05_results_discussion.md").read_text(encoding="utf-8")
    assert "six known-bad" in abstract
    assert "eleven pre-registered analyses" in abstract
    assert "three pre-registered" not in results.lower()

    # Test totals are measured by the native runner and stay out of prose.
    hardcoded_totals = [line for line in tests_readme.splitlines() if re.search(r"\b\d{2,5}\s+tests\b", line)]
    assert not hardcoded_totals, f"Test documentation re-pinned a test total: {hardcoded_totals}"

    src_subpackages = {
        entry.name
        for entry in (PROJECT_ROOT / "src" / "template_formal").iterdir()
        if entry.is_dir() and (entry / "__init__.py").is_file()
    }
    test_subdirs = {
        entry.name
        for entry in (PROJECT_ROOT / "tests").iterdir()
        if entry.is_dir() and entry.name not in {"__pycache__", "mypy_fixtures"}
    }
    assert src_subpackages, "src subpackage probe found nothing — the layout changed"
    # `types/` is the one documented exception: its two leaf modules are covered by
    # top-level test_types_*.py files rather than a test directory of their own.
    assert src_subpackages - test_subdirs == {"types"}
    assert not test_subdirs - src_subpackages
    assert sorted(path.name for path in (PROJECT_ROOT / "tests").glob("test_types_*.py")) == [
        "test_types_ids.py",
        "test_types_result.py",
    ]
    for name in sorted(test_subdirs):
        assert f"[`{name}/`]({name}/README.md)" in tests_readme, name

    root_readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    assert not re.search(r"\b\d{2,3}\.\d{2}%\b", root_readme)


def test_documented_mypy_command_uses_the_project_source_tree() -> None:
    testing_guide = (PROJECT_ROOT / "docs" / "testing_guide.md").read_text(encoding="utf-8")
    assert "MYPYPATH=src uv run --no-sync mypy --strict --explicit-package-bases --namespace-packages src" in testing_guide


def test_documented_project_script_paths_resolve_on_disk() -> None:
    """Every `scripts/<name>.py` a fork-facing surface names must actually exist.

    Regression guard: these surfaces once documented the shared repo-root runner
    `scripts/pipeline/stage_02_analysis.py` as this project's analysis command,
    which does not exist inside the exemplar, so a forker following the README hit
    a missing file. Repo-root runners are addressed as
    `scripts/pipeline/...` with an explicit `--project` flag and are excluded here;
    a bare `scripts/<name>.py` is a claim about THIS project's scripts/ directory.
    """
    surfaces = ("README.md", "AGENTS.md", "docs/rendering.md", "docs/standalone.md", ".agents/skills/template-formal/SKILL.md")
    pattern = re.compile(r"(?<![\w/.])scripts/([A-Za-z0-9_]+\.py)")
    missing: list[str] = []
    checked = 0
    for relative_path in surfaces:
        text = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        for script_name in set(pattern.findall(text)):
            checked += 1
            if not (PROJECT_ROOT / "scripts" / script_name).is_file():
                missing.append(f"{relative_path} -> scripts/{script_name}")
    assert checked > 0, "no project-local script paths found — the pattern stopped matching"
    assert not missing, f"documented project scripts do not exist: {missing}"


def test_generated_figure_registry_is_complete_when_outputs_exist() -> None:
    registry_path = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    if not registry_path.exists():
        return
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    assert set(registry) == {"fig:demo-convergence", "fig:convergence-tick-distribution"}


def test_claim_ledger_rows_have_resolvable_source_and_artifact_paths() -> None:
    ledger = yaml.safe_load((PROJECT_ROOT / "data" / "claim_ledger.yaml").read_text(encoding="utf-8"))
    claims = ledger["claims"]
    assert len(claims) == 101
    assert len({claim["claim_id"] for claim in claims}) == len(claims)
    for claim in claims:
        source_path = claim["source"].split(" ", 1)[0]
        assert (PROJECT_ROOT / source_path).exists(), source_path
        assert claim["artifact_path"] != "output/reports/validation_report.json", claim["claim_id"]
        artifact_parent = (PROJECT_ROOT / claim["artifact_path"]).parent
        if claim["artifact_path"].startswith("output/") and not (PROJECT_ROOT / "output").exists():
            # output/ may be absent after removing the generated snapshot: rows binding to
            # render artifacts are checkable only after a pipeline run, not on
            # a clean checkout.
            continue
        assert artifact_parent.exists(), claim["artifact_path"]
