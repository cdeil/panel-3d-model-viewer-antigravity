# Developer Guide

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1.  **Install uv**:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Sync Dependencies**:
    ```bash
    uv sync
    ```

3.  **Download Assets**:
    ```bash
    uv run python scripts/download_assets.py
    ```

4.  **Install Playwright Browsers**:
    ```bash
    uv run playwright install
    ```

## Running Tests

Run all tests:
```bash
uv run pytest
```

## Linting & Typing

Run ruff:
```bash
uv run ruff check
```

Run typing checks:
```bash
uv run ty check
```
