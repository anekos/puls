import re
import sys
from pathlib import Path

from puls.app import App
from puls.config import load_config


def main() -> None:
    config = load_config()
    app = App(config)

    try:
        if "grep" in Path(sys.argv[0]).name:
            if not sys.argv[1:]:
                app.usage()
            pattern = re.compile(sys.argv[1])
            app.grep(".", pattern)
        else:
            root = sys.argv[1] if len(sys.argv) > 1 else "."
            app.find(root, lambda file: print(file))
    except (BrokenPipeError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
