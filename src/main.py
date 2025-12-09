import typer

from src.core.registry import load_commands, register_with_typer
from src.core.logger import setup_logging
from src.core.config import load_config


def callback():
    config_dict["config"] = load_config()


bot = typer.Typer(callback=callback)


config_dict: dict | None = {}


def main() -> None:
    setup_logging()
    load_commands()
    app = register_with_typer(bot)
    app()