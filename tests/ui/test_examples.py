import re
import subprocess
import sys
import time

import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_example_01_basic(page):
    # Launch the example as a separate process
    cmd = [sys.executable, "-m", "panel", "serve", "examples/01_basic.py", "--port", "5011"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for server to start
        time.sleep(5)

        page.goto("http://localhost:5011/01_basic")

        viewer = page.locator("model-viewer")
        expect(viewer).to_be_visible(timeout=10000)

        # Check if src is set/loaded (Data URI or HTTP URL)
        expect(viewer).to_have_attribute("src", re.compile(r"^(data:|http)"))

        # Check sizing
        box = viewer.bounding_box()
        assert box["width"] > 0
        assert box["height"] > 0

    finally:
        proc.terminate()
        proc.wait()
