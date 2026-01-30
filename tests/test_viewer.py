from panel_model_viewer import ModelViewer


def test_model_viewer_init():
    viewer = ModelViewer(src="https://example.com/model.glb")
    assert viewer.src == "https://example.com/model.glb"
    assert viewer.auto_rotate is False
    assert viewer.camera_controls is True


def test_src_path_handling(tmp_path):
    # Create valid dummy file
    d = tmp_path / "test.glb"
    d.write_bytes(b"glTF")

    viewer = ModelViewer(src=d)
    assert viewer.src.startswith("data:model/gltf-binary;base64,")
    # b"glTF" -> Z2xURg==
    assert "Z2xURg==" in viewer.src


def test_click_handling():
    viewer = ModelViewer()

    # Mock event from generic standard mechanisms
    class MockEvent:
        data = {"clientX": 100, "clientY": 200, "target": "MODEL-VIEWER"}

    viewer._handle_click(MockEvent())

    assert viewer.clicked["clientX"] == 100
