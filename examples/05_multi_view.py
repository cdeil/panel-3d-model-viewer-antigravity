from pathlib import Path

import panel as pn

from panel_model_viewer import ModelViewer

pn.extension()

STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "astronaut.glb"
src = (
    STATIC_ASSET
    if STATIC_ASSET.exists()
    else "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
)

viewers = [
    ModelViewer(
        src=src,
        auto_rotate=True,
        height=300,
        sizing_mode="stretch_width",
        style={"background-color": "#e0f7fa"},
    ),
    ModelViewer(
        src=src,
        auto_rotate=False,
        height=300,
        sizing_mode="stretch_width",
        style={"background-color": "#ffe0b2"},
    ),
    ModelViewer(
        src=src,
        auto_rotate=True,
        height=300,
        sizing_mode="stretch_width",
        style={"background-color": "#f3e5f5"},
    ),
]

grid = pn.GridBox(*viewers, ncols=3, sizing_mode="stretch_width")

pn.template.FastListTemplate(
    title="Multi-View Gallery", main=[pn.pane.Markdown("# Multiple Independent Viewers"), grid]
).servable()
