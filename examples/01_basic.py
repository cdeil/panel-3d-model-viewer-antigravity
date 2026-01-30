import panel as pn
from panel_model_viewer import ModelViewer
from pathlib import Path

pn.extension()

# Load specific static file or URL
# For this example we use the bundled one if available, else a URL
STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "astronaut.glb"
if STATIC_ASSET.exists():
    src = STATIC_ASSET
else:
    src = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

viewer = ModelViewer(
    src=src,
    alt="A 3D Astronaut",
    auto_rotate=True,
    camera_controls=True,
    height=500,
    sizing_mode="stretch_width"
)

template = pn.template.FastListTemplate(
    title="Basic 3D Viewer",
    main=[viewer]
)
template.servable()

if __name__ == "__main__":
    pn.serve(template, port=5006, show=True)
