from pathlib import Path

import panel as pn

from panel_model_viewer import ModelViewer

pn.extension()

STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "astronaut.glb"
src = STATIC_ASSET if STATIC_ASSET.exists() else "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

viewer = ModelViewer(
    src=src,
    alt="Click me",
    camera_controls=True,
    height=400,
    sizing_mode="stretch_width"
)

logger = pn.widgets.TextAreaInput(
    name="Event Log", height=200, sizing_mode="stretch_width", disabled=True
)

def handle_click(event):
    logger.value = f"Click Detected: {event.new}\n" + logger.value

# Watch the 'clicked' param
viewer.param.watch(handle_click, 'clicked')

pn.template.FastListTemplate(
    title="Interaction Viewer",
    main=[
        pn.pane.Markdown("## Click on the 3D model to see events below"),
        viewer,
        logger
    ]
).servable()
