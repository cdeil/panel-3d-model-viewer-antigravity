import urllib.request
from pathlib import Path


def download_file(url: str, dest: Path):
    print(f"Downloading {url} to {dest}...")
    with urllib.request.urlopen(url) as response:
        dest.write_bytes(response.read())
    print("Done.")


def main():
    static_dir = Path("panel_model_viewer/static")
    static_dir.mkdir(parents=True, exist_ok=True)

    # Assets to download
    assets = {
        "model-viewer.min.js": "https://unpkg.com/@google/model-viewer@3.4.0/dist/model-viewer.min.js",
        # Example model (Astronaut)
        "astronaut.glb": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
    }

    for filename, url in assets.items():
        dest = static_dir / filename
        if not dest.exists():
            download_file(url, dest)
        else:
            print(f"{filename} already exists. Skipping.")


if __name__ == "__main__":
    main()
