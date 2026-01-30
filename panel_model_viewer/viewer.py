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

    _esm = """
    export function render({ model, el }) {
      const viewer = document.createElement("model-viewer");
      viewer.style.display = "block";
      viewer.style.width = "100%";
      viewer.style.height = "100%";
      
      // Bind attributes
      viewer.alt = model.alt;
      if (model.src) viewer.setAttribute("src", model.src);
      if (model.poster) viewer.setAttribute("poster", model.poster);
      
      if (model.auto_rotate) viewer.setAttribute("auto-rotate", "");
      if (model.camera_controls) viewer.setAttribute("camera-controls", "");

      // Apply usage css
      for (const [key, value] of Object.entries(model.style)) {
        viewer.style[key] = value;
      }

      el.appendChild(viewer);

      // Model <-> View Syncing
      // Observe changes from Python
      model.on('src', () => { 
        if (model.src) viewer.setAttribute("src", model.src); 
        else viewer.removeAttribute("src");
      });
      model.on('alt', () => { viewer.alt = model.alt; });
      model.on('auto_rotate', () => { 
        if (model.auto_rotate) viewer.setAttribute("auto-rotate", "");
        else viewer.removeAttribute("auto-rotate");
      });
      model.on('camera_controls', () => {
        if (model.camera_controls) viewer.setAttribute("camera-controls", "");
        else viewer.removeAttribute("camera-controls");
      });
      model.on('poster', () => { 
        if (model.poster) viewer.setAttribute("poster", model.poster);
        else viewer.removeAttribute("poster");
      });
       model.on('style', () => {
        for (const [key, value] of Object.entries(model.style)) {
            viewer.style[key] = value;
        }
      });

      // Events back to Python
      viewer.addEventListener('camera-change', (event) => {
        // Example: throttle this if exposing camera state
      });
      
      
      viewer.addEventListener('click', (event) => {
         model.send_event('click', {
            clientX: event.clientX,
            clientY: event.clientY,
            target: event.target.tagName
         });
      });
    }
    """

    clicked = param.Dict(default={}, doc="Last click event data.")

    def _handle_click(self, event):
        """
        Handle click event sent from JS.
        """
        self.clicked = event.data

    def __init__(self, **params):
        super().__init__(**params)
        # Handle src processing if needed (e.g. bytes to data URL)
        # For simplicity, we assume URLs or handle bytes -> datauri in frontend or helper
        # Real implementation might need _process_src logic here.
        if isinstance(self.src, (bytes, Path)):
            self.src = self._process_blob(self.src)

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
        return {"js": {"model-viewer": "static/model-viewer.min.js"}}
