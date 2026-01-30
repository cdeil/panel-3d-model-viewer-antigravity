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

viewer = ModelViewer(
    src=src,
    alt="Astronaut",
    auto_rotate=False,
    camera_controls=True,
    style={
        "background-color": "#444444",
        "--poster-color": "#ff0000",
        "border-radius": "20px",
        "border": "5px solid hotpink",
    },
    height=500,
    sizing_mode="stretch_width",
)

pn.template.FastListTemplate(
    title="Styled 3D Viewer", main=[pn.pane.Markdown("# Custom CSS Styling"), viewer]
).servable()
