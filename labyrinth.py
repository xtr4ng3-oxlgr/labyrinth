from __future__ import annotations
import argparse
import os
from pathlib import Path

try:
    from rich.prompt import Prompt, IntPrompt
    from rich.panel import Panel
    from rich.table import Table
except Exception:
    print("LABYRINTH necesita dependencias.")
    print("Ejecutá INSTALAR_DEPENDENCIAS.bat")
    print("O: python -m pip install rich")
    input("ENTER para salir...")
    raise SystemExit(1)

from src.labyrinth.core.hints import get_hint, get_solution
from src.labyrinth.core.lab_engine import create_lab, export_lab, list_labs, load_lab_case
from src.labyrinth.core.scenario_loader import get_scenario, load_scenarios
from src.labyrinth.reports.reporting import write_html_lab_report, write_json_report
from src.labyrinth.ui.console import boot, header, lab_created_panel, make_console, scenario_table


console = make_console()
LAST_LAB: Path | None = None


def show_scenarios():
    header(console)
    scenarios = load_scenarios()
    if not scenarios:
        console.print("[yellow]No scenarios found.[/yellow]")
        return
    scenario_table(console, scenarios)


def create_lab_interactive():
    global LAST_LAB
    header(console)
    scenarios = load_scenarios()
    scenario_table(console, scenarios)
    scenario_id = Prompt.ask("Scenario ID")
    scenario = get_scenario(scenario_id)
    if not scenario:
        console.print("[bold red]Scenario not found.[/bold red]")
        return
    case = create_lab(scenario)
    LAST_LAB = Path(case.path)
    header(console)
    lab_created_panel(console, case)


def create_lab_cli(scenario_id: str):
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise SystemExit(f"Scenario not found: {scenario_id}")
    case = create_lab(scenario)
    print(case.path)


def select_lab() -> Path | None:
    labs = list_labs()
    if not labs:
        console.print("[yellow]No labs created yet.[/yellow]")
        return None
    table = Table(title="Local Labs")
    table.add_column("#", justify="right")
    table.add_column("Lab")
    table.add_column("Path")
    for i, p in enumerate(labs, start=1):
        table.add_row(str(i), p.name, str(p))
    console.print(table)
    idx = IntPrompt.ask("Select lab", default=1)
    if idx < 1 or idx > len(labs):
        return None
    return labs[idx - 1]


def show_lab_dashboard(lab_path: Path | None = None):
    global LAST_LAB
    header(console)
    lab_path = lab_path or LAST_LAB or select_lab()
    if not lab_path:
        return
    LAST_LAB = lab_path
    data = load_lab_case(lab_path)
    artifacts = sorted([p for p in lab_path.rglob("*") if p.is_file() and "answer" not in p.parts])
    panel = (
        f"[white]Lab ID[/white]   [cyan]{data.get('lab_id')}[/cyan]\\n"
        f"[white]Scenario[/white] {data.get('scenario_id')}\\n"
        f"[white]Name[/white]     {data.get('name')}\\n"
        f"[white]Path[/white]     [cyan]{lab_path}[/cyan]\\n"
        f"[white]Objective[/white] {data.get('objective')}\\n"
        f"[white]Difficulty[/white] {data.get('difficulty')}\\n"
        f"[white]Category[/white] {data.get('category')}"
    )
    console.print(Panel(panel, title="CASE DASHBOARD", border_style="red"))

    table = Table(title="Artifacts")
    table.add_column("#", justify="right")
    table.add_column("Relative Path")
    for i, p in enumerate(artifacts, start=1):
        table.add_row(str(i), str(p.relative_to(lab_path)))
    console.print(table)


def show_hint(lab_path: Path | None = None, level: int | None = None):
    global LAST_LAB
    header(console)
    lab_path = lab_path or LAST_LAB or select_lab()
    if not lab_path:
        return
    LAST_LAB = lab_path
    data = load_lab_case(lab_path)
    lvl = level or IntPrompt.ask("Hint level", default=1)
    hint = get_hint(data["scenario_id"], lvl)
    console.print(Panel(hint, title=f"HINT {lvl}", border_style="cyan"))


def reveal_solution(lab_path: Path | None = None):
    global LAST_LAB
    header(console)
    lab_path = lab_path or LAST_LAB or select_lab()
    if not lab_path:
        return
    LAST_LAB = lab_path
    data = load_lab_case(lab_path)
    sol = get_solution(data["scenario_id"])
    console.print(Panel(sol, title="SOLUTION", border_style="green"))


def generate_report(lab_path: Path | None = None):
    global LAST_LAB
    header(console)
    lab_path = lab_path or LAST_LAB or select_lab()
    if not lab_path:
        return
    LAST_LAB = lab_path
    data = load_lab_case(lab_path)
    artifacts = [str(p.relative_to(lab_path)) for p in lab_path.rglob("*") if p.is_file()]
    data["artifacts"] = artifacts
    html = write_html_lab_report(data["lab_id"], data, notes="Generated locally by LABYRINTH.")
    js = write_json_report(data["lab_id"], data)
    console.print(Panel(f"HTML: [cyan]{html}[/cyan]\\nJSON: [cyan]{js}[/cyan]", title="REPORT GENERATED", border_style="green"))


def export_current_lab(lab_path: Path | None = None):
    global LAST_LAB
    header(console)
    lab_path = lab_path or LAST_LAB or select_lab()
    if not lab_path:
        return
    LAST_LAB = lab_path
    out = export_lab(lab_path)
    console.print(Panel(f"Archive: [cyan]{out}[/cyan]", title="LAB EXPORTED", border_style="green"))


def tour():
    header(console)
    console.print(Panel("""
LABYRINTH creates local training cases with safe synthetic artifacts.

Recommended flow:
1. Create a lab.
2. Read case/brief.md.
3. Inspect artifacts manually.
4. Request hints only when needed.
5. Reveal solution.
6. Generate report.
7. Export the lab if you want to share the exercise.

No real system changes are required.
No external targets are used.
""", title="OPERATOR GUIDE", border_style="red"))


def menu():
    boot(console)
    while True:
        header(console)
        console.print(Panel("""
[1] Create training lab
[2] List scenario matrix
[3] Open local lab dashboard
[4] Request hint
[5] Reveal solution
[6] Generate lab report
[7] Export lab archive
[8] Guided overview
[0] Exit
""", title="MISSION CONTROL", border_style="red"))
        choice = Prompt.ask("Select", default="1")
        if choice == "1":
            create_lab_interactive()
            Prompt.ask("ENTER", default="")
        elif choice == "2":
            show_scenarios()
            Prompt.ask("ENTER", default="")
        elif choice == "3":
            show_lab_dashboard()
            Prompt.ask("ENTER", default="")
        elif choice == "4":
            show_hint()
            Prompt.ask("ENTER", default="")
        elif choice == "5":
            reveal_solution()
            Prompt.ask("ENTER", default="")
        elif choice == "6":
            generate_report()
            Prompt.ask("ENTER", default="")
        elif choice == "7":
            export_current_lab()
            Prompt.ask("ENTER", default="")
        elif choice == "8":
            tour()
            Prompt.ask("ENTER", default="")
        elif choice == "0":
            break


def cli():
    parser = argparse.ArgumentParser(prog="labyrinth", description="Local defensive training lab generator.")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list")
    c = sub.add_parser("create")
    c.add_argument("scenario_id")
    d = sub.add_parser("dashboard")
    d.add_argument("lab_path")
    h = sub.add_parser("hint")
    h.add_argument("lab_path")
    h.add_argument("--level", type=int, default=1)
    s = sub.add_parser("solution")
    s.add_argument("lab_path")
    r = sub.add_parser("report")
    r.add_argument("lab_path")
    e = sub.add_parser("export")
    e.add_argument("lab_path")

    args = parser.parse_args()

    if not args.cmd:
        menu()
    elif args.cmd == "list":
        show_scenarios()
    elif args.cmd == "create":
        create_lab_cli(args.scenario_id)
    elif args.cmd == "dashboard":
        show_lab_dashboard(Path(args.lab_path))
    elif args.cmd == "hint":
        show_hint(Path(args.lab_path), args.level)
    elif args.cmd == "solution":
        reveal_solution(Path(args.lab_path))
    elif args.cmd == "report":
        generate_report(Path(args.lab_path))
    elif args.cmd == "export":
        export_current_lab(Path(args.lab_path))


if __name__ == "__main__":
    cli()
