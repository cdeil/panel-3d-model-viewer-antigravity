from pathlib import Path

import panel as pn

from panel_model_viewer import ModelViewer

pn.extension()

# Note: For local files, it's recommended to serve them as static assets
# rather than embedding them as large Data URIs, to avoid WebSocket limits.
# STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "astronaut.glb"
# if STATIC_ASSET.exists():
#    src = STATIC_ASSET
# else:
# Use a local file (small enough to be safe with default WebSocket limits)
# This avoids external network dependency and demonstrates local file loading.
# Ensure 'panel_model_viewer/static/Box.glb' exists (downloaded via scripts or manually).
STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "Box.glb"

viewer = ModelViewer(
    src=STATIC_ASSET,
    alt="A 3D Box",
    auto_rotate=True,
    camera_controls=True,
    height=500,
    sizing_mode="stretch_width",
)

pn.template.FastListTemplate(title="Basic 3D Viewer", main=[viewer]).servable()
