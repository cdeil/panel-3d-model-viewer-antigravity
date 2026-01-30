from pathlib import Path

import panel as pn

from panel_model_viewer import ModelViewer

pn.extension(template="material")

STATIC_ASSET = Path(__file__).parent.parent / "panel_model_viewer" / "static" / "astronaut.glb"
src = STATIC_ASSET if STATIC_ASSET.exists() else "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

viewer = ModelViewer(
    src=src,
    alt="Astronaut",
    auto_rotate=True,
    camera_controls=True,
    sizing_mode="stretch_both",
    style={"background-color": "#eee"}
)

sidebar = pn.Column(
    pn.pane.Markdown("## Controls"),
    pn.widgets.Checkbox.from_param(viewer.param.auto_rotate, name="Auto Rotate"),
    pn.widgets.Checkbox.from_param(viewer.param.camera_controls, name="Camera Controls"),
    pn.widgets.ColorPicker(name="Background Color", value="#eeeeee"),
)

def update_bg(event):
    viewer.style = {**viewer.style, "background-color": event.new}

sidebar[3].param.watch(update_bg, 'value')

pn.template.MaterialTemplate(
    title="3D Model Dashboard",
    sidebar=[sidebar],
    main=[
        pn.Card(viewer, title="3D Viewer", height=600, sizing_mode="stretch_width")
    ]
).servable()
