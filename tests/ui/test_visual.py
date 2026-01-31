import sys
import time
import pytest
from pathlib import Path
from playwright.sync_api import expect
from PIL import Image
import numpy as np
from panel.tests.util import run_panel_serve, wait_for_port

# Define artifacts directory
ARTIFACTS_DIR = Path(__file__).parent / "visual_regression"
ARTIFACTS_DIR.mkdir(exist_ok=True)

def check_image_not_blank(image_path):
    """
    Checks if the image at image_path is not a single solid color (e.g. valid render).
    Raises AssertionError if image is blank/solid color.
    """
    with Image.open(image_path) as img:
        # Convert to RGB to ignore alpha if present, or handle RGBA
        img = img.convert("RGB")
        data = np.array(img)
        
        # Check standard deviation of pixels
        # If std is 0, all pixels are identical (blank)
        std = data.std()
        print(f"Image {image_path.name} pixel std dev: {std}")
        
        if std < 1.0: # Allow tiny noise, but effectively blank
            # Verify if it's pure grey/white/black
            mean_color = data.mean(axis=(0,1))
            raise AssertionError(f"Image {image_path.name} appears to be blank/solid color. Mean RGB: {mean_color}, Std Dev: {std}")

def wait_for_model_load(page, timeout=15000):
    """
    Waits for the model-viewer to fire the 'load' event.
    """
    # Check if already loaded or wait for event
    page.evaluate("""
        const viewer = document.querySelector('model-viewer');
        if (viewer) {
            if (viewer.loaded) {
                window._modelLoaded = true;
            } else {
                window._modelLoaded = false;
                viewer.addEventListener('load', () => { window._modelLoaded = true; });
            }
        }
    """)
    try:
        page.wait_for_function("window._modelLoaded === true", timeout=timeout)
    except Exception as e:
        print(f"Wait for load failed: {e}")
        # Identify if viewer exists
        is_present = page.evaluate("!!document.querySelector('model-viewer')")
        print(f"Model viewer present: {is_present}")
        raise e

@pytest.mark.ui
def test_fox_visual(page):
    """
    Test the Fox example with the bundled Fox.glb file (standard sample model).
    """
    script = Path("examples/06_fox.py").absolute()
    screenshot_path = ARTIFACTS_DIR / "example_06_fox.png"
    
    with run_panel_serve(["--port", "0", script]) as p:
        port = wait_for_port(p.stdout)
        url = f"http://localhost:{port}/06_fox"
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.type}: {msg.text}"))

        page.goto(url)
        locator = page.locator("model-viewer")
        expect(locator).to_be_visible(timeout=10000)
        
        # Wait for model to load
        wait_for_model_load(page, timeout=20000)
        
        # Additional wait for render
        page.wait_for_timeout(1000)
        
        # Capture screenshot
        page.screenshot(path=screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        # Verify
        check_image_not_blank(screenshot_path)

@pytest.mark.ui
def test_minimal_visual(page):
    """
    Test the minimal example with a local small GLB file (Box.glb).
    """
    script = Path("examples/00_minimal.py").absolute()
    screenshot_path = ARTIFACTS_DIR / "example_00_minimal.png"
    
    with run_panel_serve(["--port", "0", script]) as p:
        port = wait_for_port(p.stdout)
        url = f"http://localhost:{port}/00_minimal"
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.type}: {msg.text}"))

        # Go to page
        page.goto(url)
        
        # Wait for model-viewer to be present and loaded
        # We can check for the 'model-visibility' attribute or just wait
        locator = page.locator("model-viewer")
        expect(locator).to_be_visible(timeout=10000)
        
        # Wait for model to load
        wait_for_model_load(page)
        
        # Give it time to render the 3D scene
        page.wait_for_timeout(1000) 
        
        # Capture screenshot
        page.screenshot(path=screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        # Verify
        check_image_not_blank(screenshot_path)

@pytest.mark.ui
def test_basic_visual(page):
    """
    Test the basic example with the local Box.glb file.
    """
    script = Path("examples/01_basic.py").absolute()
    screenshot_path = ARTIFACTS_DIR / "example_01_basic.png"
    
    with run_panel_serve(["--port", "0", script]) as p:
        port = wait_for_port(p.stdout)
        url = f"http://localhost:{port}/01_basic"
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.type}: {msg.text}"))

        page.goto(url)
        locator = page.locator("model-viewer")
        expect(locator).to_be_visible(timeout=15000)
        
        # Wait for model to load
        wait_for_model_load(page, timeout=20000)
        
        # Wait longer for remote asset render
        page.wait_for_timeout(1000)
        
        # Capture screenshot
        page.screenshot(path=screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        # Verify
        check_image_not_blank(screenshot_path)
