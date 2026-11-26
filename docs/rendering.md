# Generate evidence and render the manuscript

## Generate the analysis artifacts

From the standalone project root, run:

```sh
uv sync --locked --python 3.14 --extra dev
MPLBACKEND=Agg uv run --no-sync python scripts/02_run_analysis.py
```

The analysis writes demo and sweep summaries, the demo agents' SQLite
files, and the sweep databases to `output/data/`. It writes two PNGs and
their figure registry to `output/figures/`. The
[claim ledger](../data/claim_ledger.yaml) connects claims to evidence.
The committed title-page illustration can be regenerated separately with
`uv run --no-sync python scripts/zz_generate_cover_art.py`.

## Run the pinned renderer

Install Git, uv, Pandoc, XeLaTeX, BibTeX, and the TeX packages listed in
the [template run guide](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md).
Install [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref/releases/tag/v0.3.17.0c)
for the matching version of Pandoc. The linked release matches Pandoc 3.1.11.1.
The manuscript bundles two architecture diagrams as PNGs alongside their
[Mermaid sources](manuscript/figures/README.md). The analysis command
copies these assets to `output/figures/` for the PDF and HTML renderers.

From the standalone project root after generating the analysis:

```sh
formal_checkout="$PWD"
git clone https://github.com/docxology/template.git ../formal-renderer
cd ../formal-renderer
git checkout --detach 87704feae0a4490ef7dad9c931d268e8c30273c2
uv sync --locked --no-dev
mkdir -p projects/working
ln -s "$formal_checkout" "projects/working/$(basename "$formal_checkout")"
formal_project="working/$(basename "$formal_checkout")"

PYTHONPATH="$PWD" uv run --no-sync python "$formal_checkout/scripts/00_setup_environment.py"
uv run --no-sync python scripts/pipeline/stage_03_render.py --project "$formal_project"
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project "$formal_project"
```

The pipeline finds the source, [metadata](manuscript/config.yaml),
[LaTeX preamble](manuscript/preamble.md), bibliography, and cover under
`docs/manuscript/`. Register the manuscript paths in Git's index before
running Stage 04 so provenance can include them. If the project already
lives inside the template checkout, use its existing project selector.

The standalone project receives the combined PDF in `output/pdf/`,
combined HTML in `output/web/index.html`, and section slide decks in
`output/slides/`. Stage 04 writes `validation_report.json` and
`rendered_provenance.json` in `output/reports/`. Check the combined
editions for the ordered sections, bibliography, embedded analysis
figures, and the two architecture diagrams. Regeneration may update the committed
`output/` snapshot.
