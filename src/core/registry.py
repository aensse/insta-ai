import importlib
import pkgutil
import typer
from typing import Callable


_registry: list[tuple[str, Callable[..., None]]] = []


def register_command(name: str):
    def decorator(func: Callable[..., None]):
        _registry.append((name, func))
        return func
    return decorator


def load_commands() -> None:
    import src.commands

    for _, module_name, _ in pkgutil.iter_modules(src.commands.__path__):
        importlib.import_module(f"src.commands.{module_name}")


def register_with_typer(app: typer.Typer) -> typer.Typer:
    group_apps: dict[str, typer.Typer] = {}

    for group, func in get_registry():
        if group not in group_apps:
            group_apps[group] = typer.Typer()
            app.add_typer(group_apps[group], name=group)
        group_apps[group].command(group)(func)
    return app


def get_registry() -> list[tuple[str, Callable[..., None]]]:
    return _registry.copy()