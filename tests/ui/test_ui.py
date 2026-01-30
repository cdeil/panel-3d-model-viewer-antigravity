import time
from contextlib import contextmanager
from pathlib import Path

import panel as pn
import pytest
from playwright.sync_api import expect

from panel_model_viewer import ModelViewer

PORT = 8123

@contextmanager
def run_server(app_func, port):
    server = pn.serve(app_func, port=port, threaded=True, show=False)
    time.sleep(1) # Wait for startup
    try:
        yield
    finally:
        server.stop()

def get_local_model():
    p = Path("panel_model_viewer/static/astronaut.glb").absolute()
    if not p.exists():
        # Fallback if running from wrong dir?
        # Assuming run from root
        pass
    return p

def create_app():
    return ModelViewer(
        src=get_local_model(),
        auto_rotate=True,
        height=500,
        width=500,
        sizing_mode="fixed",
    )

@pytest.mark.ui
def test_model_viewer_renders(page):
    with run_server(create_app, PORT):
        page.goto(f"http://localhost:{PORT}")
        
        # Check if model-viewer tag exists
        viewer = page.locator("model-viewer")
        expect(viewer).to_be_visible(timeout=10000)
        
        # Check attributes
        expect(viewer).to_have_attribute("auto-rotate", "")

@pytest.mark.ui
def test_lifecycle_add_remove(page):
    # Dynamic add/remove test
    def app():
        col = pn.Column()
        btn_add = pn.widgets.Button(name="Add")
        btn_remove = pn.widgets.Button(name="Remove")
        
        def add(e):
            col[:] = [
                ModelViewer(
                    src=get_local_model(),
                    height=500,
                    width=500,
                    sizing_mode="fixed",
                )
            ]
        
        def remove(e):
            col[:] = []

        btn_add.on_click(add)
        btn_remove.on_click(remove)
        
        return pn.Row(pn.Column(btn_add, btn_remove), col)

    with run_server(app, PORT+1):
        page.goto(f"http://localhost:{PORT+1}")
        
        viewer = page.locator("model-viewer")
        expect(viewer).not_to_be_attached(timeout=5000)
        
        page.get_by_role("button", name="Add").click()
        expect(viewer).to_be_visible(timeout=5000)
        
        page.get_by_role("button", name="Remove").click()
        expect(viewer).not_to_be_attached(timeout=5000)
