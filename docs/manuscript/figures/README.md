# `docs/manuscript/figures/`

Project-specific manuscript figures live here. `cover_colony.png` is generated
from the project figure tooling and referenced by manuscript configuration and
rendering outputs.

Do not hand-edit raster outputs. Regenerate figures from the project scripts
or source modules, then rerun manuscript validation.

The type architecture section uses [module_layout.png](module_layout.png)
and [session_phases.png](session_phases.png). Their editable Mermaid sources
are [module_layout.mmd](module_layout.mmd) and
[session_phases.mmd](session_phases.mmd). Update the PNGs with Mermaid CLI
12.2.0 and its Chrome Headless Shell when a diagram changes:

```sh
cd docs/manuscript/figures
mmdc --input module_layout.mmd --output module_layout.png
mmdc --input session_phases.mmd --output session_phases.png
```

Run the [analysis command](../../rendering.md#generate-the-analysis-artifacts)
to publish the two diagrams alongside the analysis figures.
