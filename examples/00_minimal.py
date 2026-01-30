import panel as pn
from pathlib import Path
from panel_model_viewer import ModelViewer

pn.extension()

# Use the local Box.glb (small file)
# This serves to test if small Data URIs work and if the component renders minimally
STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "Box.glb"

viewer = ModelViewer(
    src=STATIC_ASSET,
    alt="A 3D Box",
    auto_rotate=True,
    camera_controls=True,
    style={"background-color": "red", "height": "500px", "width": "500px"} # Explicit size
)

pn.template.FastListTemplate(
    title="Minimal 3D Viewer",
    main=[viewer],
).servable()
