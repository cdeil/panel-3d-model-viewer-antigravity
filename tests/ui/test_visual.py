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

def verify_assets_present():
    """
    Debug: Verify if static assets exist.
    """
    import panel_model_viewer
    module_dir = Path(panel_model_viewer.__file__).parent
    static_file = module_dir / "static" / "model-viewer.min.js"
    print(f"Checking for static asset at: {static_file}")
    if static_file.exists():
        print(f"Static asset found. Size: {static_file.stat().st_size} bytes")
    else:
        print("ERROR: Static asset NOT FOUND!")
        # List contents of static dir if it exists
        static_dir = module_dir / "static"
        if static_dir.exists():
            print(f"Static dir contents: {list(static_dir.iterdir())}")
        else:
            print("Static dir does not exist.")

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

def wait_for_model_load(page, locator=None, timeout=15000):
    """
    Waits for the model-viewer to fire the 'load' event.
    """
    if locator is None:
        locator = page.locator("model-viewer").first

    # Check if already loaded or wait for event
    # We use locator.evaluate to ensure we get the element even if in Shadow DOM
    # Check if already loaded or wait for event
    # We use locator.evaluate to ensure we get the element even if in Shadow DOM
    locator.evaluate("""
        (viewer) => {
            console.log('Viewer found. Constructor:', viewer.constructor.name);
            console.log('modelIsVisible:', viewer.modelIsVisible);
            console.log('CustomElement registry:', customElements.get('model-viewer'));
            console.log('Scripts:', Array.from(document.querySelectorAll('script')).map(s => s.src));
            
            // Check if model is visible (loaded and rendered)
            if (viewer.modelIsVisible) {
                window._modelLoaded = true;
            } else {
                window._modelLoaded = false;
                window._modelError = null;
                
                // Add listeners
                viewer.addEventListener('load', () => { 
                    console.log('Model loaded event fired');
                    window._modelLoaded = true; 
                });
                
                // Also listen for poster-dismissed? No, load is better.
                
                viewer.addEventListener('error', (e) => {
                    console.error('Model load error:', e);
                    window._modelError = e.detail || 'Unknown error';
                });
            }
        }
    """)
    try:
        # Wait for either success or error
        page.wait_for_function("window._modelLoaded === true || window._modelError", timeout=timeout)
        
        # Check for error
        error = page.evaluate("window._modelError")
        if error:
            raise RuntimeError(f"Model load failed with error: {error}")
            
    except Exception as e:
        print(f"Wait for load failed: {e}")
        # Identify if viewer exists
        is_visible = locator.is_visible()
        print(f"Model viewer visible: {is_visible}")
        raise e

@pytest.mark.ui
def test_fox_visual(page):
    """
    Test the Fox example with the bundled Fox.glb file (standard sample model).
    """
    verify_assets_present()
    script = Path("examples/06_fox.py").absolute()
    screenshot_path = ARTIFACTS_DIR / "example_06_fox.png"
    
    with run_panel_serve(["--port", "0", "--log-level", "debug", script]) as p:
        port = wait_for_port(p.stdout)
        url = f"http://localhost:{port}/06_fox"
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.type}: {msg.text}"))

        page.goto(url)
        locator = page.locator("model-viewer")
        expect(locator).to_be_visible(timeout=10000)
        
        # Wait for model to load
        wait_for_model_load(page, locator=locator, timeout=20000)
        
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
    
    with run_panel_serve(["--port", "0", "--log-level", "debug", script]) as p:
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
        wait_for_model_load(page, locator=locator)
        
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
    
    with run_panel_serve(["--port", "0", "--log-level", "debug", script]) as p:
        port = wait_for_port(p.stdout)
        url = f"http://localhost:{port}/01_basic"
        
        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.type}: {msg.text}"))

        page.goto(url)
        locator = page.locator("model-viewer")
        expect(locator).to_be_visible(timeout=15000)
        
        # Wait for model to load
        wait_for_model_load(page, locator=locator, timeout=20000)
        
        # Wait longer for remote asset render
        page.wait_for_timeout(1000)
        
        # Capture screenshot
        page.screenshot(path=screenshot_path)
        print(f"Saved screenshot to {screenshot_path}")
        
        # Verify
        check_image_not_blank(screenshot_path)
