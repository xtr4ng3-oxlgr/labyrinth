from __future__ import annotations
import os
import time

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
except Exception:
    Console = None
    Panel = None
    Table = None
    box = None
    Text = None
    Progress = None

from .banner import BANNER, COMPACT
from .. import APP_NAME, APP_VERSION, AUTHOR, TAGLINE


def make_console():
    if Console is None:
        return None
    return Console()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def boot(console):
    clear()
    if console is None:
        print(BANNER)
        return
    console.print(f"[bold red]{BANNER}[/bold red]")
    console.print(f"[dim]{APP_NAME} v{APP_VERSION} // {TAGLINE} // {AUTHOR}[/dim]")
    steps = [
        "loading scenario engine",
        "mounting local lab workspace",
        "preparing artifact generator",
        "arming hint system",
        "loading report renderer",
        "ready",
    ]
    with Progress(SpinnerColumn(), TextColumn("[bold red]{task.description}"), BarColumn(), transient=True, console=console) as progress:
        task = progress.add_task("initializing", total=len(steps))
        for s in steps:
            progress.update(task, description=s)
            time.sleep(0.12)
            progress.advance(task)
    console.print("[bold green]LABYRINTH ONLINE[/bold green]")


def header(console):
    clear()
    if console:
        console.print(f"[bold red]{COMPACT}[/bold red]")
        console.print(f"[dim]{APP_NAME} v{APP_VERSION} // {TAGLINE} // {AUTHOR}[/dim]")
    else:
        print(COMPACT)


def scenario_table(console, scenarios):
    table = Table(title="Scenario Matrix", box=box.HEAVY_HEAD)
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Category")
    table.add_column("Difficulty")
    table.add_column("Objective")
    for s in scenarios:
        table.add_row(s.id, s.name, s.category, s.difficulty, s.objective[:80])
    console.print(table)


def lab_created_panel(console, case):
    console.print(Panel(
        f"[white]Lab ID[/white]   [cyan]{case.lab_id}[/cyan]\n"
        f"[white]Name[/white]     {case.name}\n"
        f"[white]Path[/white]     [cyan]{case.path}[/cyan]\n"
        f"[white]Objective[/white] {case.objective}\n"
        f"[white]Hints[/white]    {case.hints_total}",
        title="LAB CREATED",
        border_style="red"
    ))
