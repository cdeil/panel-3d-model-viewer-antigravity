import base64
from pathlib import Path

import param
from panel.custom import JSComponent


class ModelViewer(JSComponent):
    """
    A Panel component for displaying 3D models using <model-viewer>.
    """

    src = param.ClassSelector(
        class_=(str, bytes, Path),
        doc="""
        Source of the 3D model. Can be a URL (str), a local path (str/Path),
        or raw bytes.""",
    )

    alt = param.String(default="A 3D model", doc="Alternative text.")

    auto_rotate = param.Boolean(default=False, doc="Enable auto-rotation.")

    camera_controls = param.Boolean(default=True, doc="Enable camera controls.")

    poster = param.String(default=None, doc="URL or path to poster image.")

    style = param.Dict(default={}, doc="CSS styles to apply to the component.")
    
    html_attrs = param.Dict(default={}, doc="HTML attributes to apply to the model-viewer tag.")

    _esm = Path(__file__).parent / "viewer.js"

    clicked = param.Dict(default={}, doc="Last click event data.")

    def _handle_click(self, event):
        """
        Handle click event sent from JS.
        """
        self.clicked = event.data

    def __init__(self, **params):
        if 'src' in params and isinstance(params['src'], (bytes, Path)):
            params['src'] = self._process_blob(params['src'])
        
        super().__init__(**params)

    def _process_blob(self, data):
        # Very basic data URI implementation for bytes/path
        # In a real app, might want to serve via invalidation handler or similar
        mime = "model/gltf-binary"  # Default assumption
        if isinstance(data, Path):
            data = data.read_bytes()

        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    def _get_resources(self):
        # Serve local assets
        print("_get_resources called")
        # return {"js": {"model-viewer": "static/model-viewer.min.js"}}
        return {"js": {"model-viewer": "https://unpkg.com/@google/model-viewer@3.4.0/dist/model-viewer.min.js"}}
