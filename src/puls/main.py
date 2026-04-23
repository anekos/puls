import click

from puls.app import App
from puls.config import DEFAULT_CONFIG, config_path, config_to_toml, load_config


def generate_config() -> None:
    p = config_path()
    if p.exists():
        click.echo(f"Config file already exists: {p}", err=True)
        raise SystemExit(1)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(config_to_toml(DEFAULT_CONFIG), encoding="utf-8")
    click.echo(f"Generated: {p}")


@click.command()
@click.argument("path", default=".")
@click.option(
    "--generate-config",
    "do_generate_config",
    is_flag=True,
    help="Generate default config file.",
)
def main(path: str, do_generate_config: bool) -> None:
    if do_generate_config:
        generate_config()
        return

    config = load_config()
    app = App(config)

    try:
        app.find(path, lambda file: print(file))
    except (BrokenPipeError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
