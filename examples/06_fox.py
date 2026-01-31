import panel as pn
from pathlib import Path
from panel_model_viewer import ModelViewer

pn.extension()

# Load the local Fox model (bundled test asset)
STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "Fox.glb"

viewer = ModelViewer(
    src=STATIC_ASSET,
    alt="A 3D Fox",
    auto_rotate=True,
    camera_controls=True,
    html_attrs={
        "shadow-intensity": "1",
    },
    height=500,
    sizing_mode="stretch_width",
    style={
        "background-color": "#444"
    }
)

pn.Column(
    "# 3D Fox Model",
    viewer,
).servable()
