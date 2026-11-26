# Illegal States, Mostly Unrepresentable

The numbered files render in order. The manuscript studies the guarantees of
a typed ant-robot colony simulation and ties quantitative claims to
[source-owned evidence](../../data/claim_ledger.yaml) and the
[verification trail](../ISA.md#verification).
Follow the [rendering guide](../rendering.md) to build it.

## File inventory

| File | Section | Role |
| --- | --- | --- |
| [`00_abstract.md`](00_abstract.md) | Abstract (`{#sec:abstract}`) | One-paragraph summary of the typed surface, the decentralization claim, and the honest mypy-vs-runtime scoping. |
| [`01_introduction.md`](01_introduction.md) | Introduction (`{#sec:introduction}`) | Why ant robots; frames the decentralized-multiagent research gap this exemplar fills. |
| [`02_type_architecture.md`](02_type_architecture.md) | Type Architecture (`{#sec:type-architecture}`) | Module layout of the typed surface — `Result`, `NewType` IDs, session types, affine handles. |
| [`03_storage_as_functor.md`](03_storage_as_functor.md) | Storage as a Functor (`{#sec:storage-functor}`) | Frames `storage/schema.py`'s agent-local SQLite schema as a functor `Schema -> Set`. |
| [`04_active_inference.md`](04_active_inference.md) | The Active Inference Framing of the Decision Loop (`{#sec:active-inference}`) | Reads `agent/agent.py`'s `Agent.decide` as an expected-free-energy minimization (Friston 2005). |
| [`05_results_discussion.md`](05_results_discussion.md) | Results and Discussion (`{#sec:results-discussion}`) | The evidentiary core — mypy-as-oracle proof-of-detection, fault-injected negative controls, colony convergence statistics, eleven pre-registered analyses across three experiment families, the formal side-spec status, and threats to the claims. By far the largest file; read its own headings before editing (`grep -n '^##' 05_results_discussion.md`). |
| [`99_references.md`](99_references.md) | References (`{#sec:references}`) | Explains the Pandoc/`natbib` bibliography wiring; the actual entries live in `references.bib`. |
| [`config.yaml`](config.yaml) | — | Real, committed paper metadata (title, authors, publication identifiers, render-format toggles, steganography profile). Loaded via `yaml.safe_load` by `infrastructure/rendering/_pdf_combined_renderer.py`. |
| [`config.yaml.example`](config.yaml.example) | — | Fill-in-the-blank template for a new project copying this exemplar; diff it against `config.yaml` to see exactly which fields are project-specific. |
| [`preamble.md`](preamble.md) | — | LaTeX packages injected before Pandoc compilation — `algorithm2e` for session-type pseudocode, `fontspec`/`unicode-math` with a JuliaMono/Latin-Modern-Math fallback path for the Greek/math glyphs the code listings and equations use. |
| [`references.bib`](references.bib) | — | Bibliographic sources for the type-theory, distributed-systems, and Active Inference claims. |

The two analysis figures in [Results and Discussion](05_results_discussion.md)
are generated in `output/figures/`. The architecture section includes two
[diagrams with Mermaid sources](figures/README.md). The [cover art](figures/README.md) is a committed
presentation asset.
