# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

puls is a "smart find/grep" CLI tool written in Python. It provides two commands:
- `puls [<PATH>]` — recursively list files, skipping common noise (build artifacts, binary files, lock files, etc.)
- When invoked with "grep" in argv[0]: `sgrep <PATTERN>` — grep through non-ignored files

Users can add per-project ignore patterns via a `.puls.ignore` file in the project root.

## Development

Uses `uv` for project management (build backend: `uv_build`). Python >=3.11.

```bash
# Install in development mode
uv pip install -e .

# Lint
uv run ruff check src/
uv run ruff format --check src/

# Type check
uv run mypy src/

# Format
uv run ruff format src/
```

There are no tests yet.

## Architecture

Single-module app in `src/puls/app.py`. Entry point is `main()`, registered as `puls` console script in pyproject.toml.

- `Config` dataclass holds three ignore lists: directories, extensions, files (glob patterns)
- `App` performs file walking (`find`) and content searching (`grep`) using an iterative stack-based directory traversal
- `Configurations.Standard` is the built-in default config with extensive ignore lists
- `main()` dispatches between find and grep mode based on whether "grep" appears in `sys.argv[0]`

## Style

- できる限り、型ヒントを使用すること
- `typing` モジュール (Optional/List/Union など) はなるべく使わず、`str | None` や `int | bool` のように書く
