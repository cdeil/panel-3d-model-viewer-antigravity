# Project Overview for Agents

**Project**: `panel-model-viewer`
**Goal**: A Python Panel component wrapping the `<model-viewer>` web component.

## Key Files
- `README.md`: User-facing docs (installation, usage).
- `DEV.md`: Developer docs (setup, testing).
- `panel_model_viewer/viewer.py`: Core logic. Implements `ModelViewer` via `JSComponent`.
- `examples/`: Usage scripts. RUn via `uv run panel serve examples/XX.py`.
- `tests/`: Pytest suite (Unit + Playwright UI).

## Architecture
- **Tech Stack**: Python 3.12+, Panel, Hatchling, UV.
- **Component**: `JSComponent` with bundled `model-viewer.min.js`.
- **Assets**: Handles `src` as URL or `Path`/`bytes` (converts to Data URI).

## Commands
- **Sync**: `uv sync`
- **Test**: `uv run pytest`
- **Lint**: `uv run ruff check .`
- **Type**: `uv run ty check`
