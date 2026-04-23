import fnmatch
import re
from pathlib import Path

from puls.config import Config


class App:
    def __init__(self, config: Config):
        self.ignore_directories = config.ignore_directories
        self.ignore_extensions = self._build_ext(config.ignore_extensions)
        self.ignore_files = config.ignore_files

    @staticmethod
    def load_ignore_file(ignore_file_path: Path | None = None) -> list[str]:
        if ignore_file_path is None:
            ignore_file_path = Path.cwd() / ".puls.ignore"

        if not ignore_file_path.exists():
            return []

        try:
            with ignore_file_path.open("r", encoding="utf-8") as f:
                return [
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
        except (OSError, UnicodeDecodeError):
            return []

    def find(self, root: str, callback) -> None:
        root_path = Path(root).resolve()

        # Load additional ignore patterns from .puls.ignore
        additional_ignore = self.load_ignore_file(root_path / ".puls.ignore")
        all_ignore_files = self.ignore_files + additional_ignore

        found_files: list[str] = []

        def should_ignore_dir(dir_name: str) -> bool:
            return any(
                fnmatch.fnmatch(dir_name, pattern)
                for pattern in self.ignore_directories
            )

        stack = [root_path]

        while stack:
            dir_path = stack.pop()

            try:
                for item in dir_path.iterdir():
                    if item.is_dir():
                        if not should_ignore_dir(item.name):
                            stack.append(item)
                    elif item.is_file():
                        relative_path = item.relative_to(root_path)
                        str_path = str(relative_path)

                        if self.ignore_extensions.search(str_path):
                            continue
                        if any(
                            fnmatch.fnmatch(str_path, pattern)
                            for pattern in all_ignore_files
                        ):
                            continue

                        found_files.append(str_path)
            except (PermissionError, OSError, ValueError):
                continue

        for file in sorted(found_files):
            callback(file)

    def _build_ext(self, patterns: list[str]) -> re.Pattern[str]:
        escaped_patterns = [re.escape(pattern) for pattern in patterns]
        return re.compile(r"\.(" + "|".join(escaped_patterns) + r")\Z")
