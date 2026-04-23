import tomllib
from dataclasses import dataclass
from pathlib import Path

import platformdirs


@dataclass
class Config:
    ignore_directories: list[str]
    ignore_extensions: list[str]
    ignore_files: list[str]


DEFAULT_CONFIG = Config(
    ignore_directories=[
        "*.egg-info",
        ".IdeaIC11",
        ".IdeaIC12",
        ".IdeaIC13",
        ".activator",
        ".aws-sam",
        ".build",
        ".bundle",
        ".cabal-sandbox",
        ".cabal-sandox",
        ".cache",
        ".class",
        ".coverage",
        ".dart_tool",
        ".eggs",
        ".env",
        ".git",
        ".idea",
        ".mypy_cache",
        ".next",
        ".parcel-cache",
        ".pytest_cache",
        ".ruff_cache",
        ".sass-cache",
        ".stack-work",
        ".tmpBin",
        ".tox",
        ".vagrant",
        ".venv",
        "__pycache__",
        "_darcs",
        "android",
        "bower_components",
        "build",
        "dist",
        "elm-stuff",
        "ios",
        "maven_repository",
        "node_modules",
        "storybook-static",
        "target",
        "vendor",
    ],
    ignore_extensions=[
        "bak",
        "bin",
        "class",
        "dll",
        "dylib",
        "dyn_c",
        "dyn_hi",
        "exe",
        "fasl",
        "hi",
        "jar",
        "jpeg",
        "jpg",
        "lib",
        "lock",
        "log",
        "o",
        "obj",
        "pdb",
        "png",
        "pyc",
        "retry",
        "so",
        "swp",
        "temp",
        "tmp",
    ],
    ignore_files=[
        "*.bak",
        "*.bundle.*",
        "*.chunk.*",
        "*.crt",
        "*.csr",
        "*.db",
        "*.dmp",
        "*.key",
        "*.lock",
        "*.log",
        "*.map",
        "*.min.css",
        "*.min.js",
        "*.orig",
        "*.p12",
        "*.pem",
        "*.pfx",
        "*.pid",
        "*.rej",
        "*.sqlite",
        "*.swo",
        "*.swp",
        "*.temp",
        "*.tmp",
        "*~",
        ".DS_Store",
        ".aider.*",
        ".env.*",
        "Cargo.lock",
        "Pipfile.lock",
        "Thumbs.db",
        "core.*",
        "desktop.ini",
        "package-lock.json",
        "pnpm-lock.yaml",
        "poetry.lock",
        "requirements*.txt",
        "vgcore.*",
        "yarn.lock",
    ],
)


def load_config() -> Config:
    config_path = Path(platformdirs.user_config_dir("puls")) / "config.toml"

    if not config_path.exists():
        return DEFAULT_CONFIG

    try:
        with config_path.open("rb") as f:
            data = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return DEFAULT_CONFIG

    ignore = data.get("ignore", {})
    return Config(
        ignore_directories=ignore.get("directories", DEFAULT_CONFIG.ignore_directories),
        ignore_extensions=ignore.get("extensions", DEFAULT_CONFIG.ignore_extensions),
        ignore_files=ignore.get("files", DEFAULT_CONFIG.ignore_files),
    )
