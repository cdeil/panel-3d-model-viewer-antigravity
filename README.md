# Panel Model Viewer

A [Panel](https://panel.holoviz.org/) component for rendering 3D models using the Google [`<model-viewer>`](https://modelviewer.dev/) web component.

## Features

-   **Wide Format Support**: glTF, GLB.
-   **Interactive**: Orbit controls, zooming.
-   **Customizable**: CSS styling, initial camera position.
-   **Pure Python**: No npm/node.js required for usage.

## Installation

```bash
pip install panel-model-viewer
```

## Usage

```python
import panel as pn
from panel_model_viewer import ModelViewer

pn.extension()

viewer = ModelViewer(
    src="https://modelviewer.dev/shared-assets/models/Astronaut.glb",
    alt="A 3D model of an astronaut",
    auto_rotate=True,
    camera_controls=True,
    height=400,
    sizing_mode="stretch_width"
)

viewer.servable()
```

## Running Examples

You can run the included examples using `panel serve`:

```bash
uv run panel serve examples/01_basic.py --autoreload
```
