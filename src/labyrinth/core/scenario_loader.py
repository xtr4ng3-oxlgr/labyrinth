from __future__ import annotations
import json
from pathlib import Path
from .models import Scenario
from .paths import scenarios_dir


def load_scenarios() -> list[Scenario]:
    scenarios: list[Scenario] = []
    root = scenarios_dir()
    if not root.exists():
        return scenarios
    for path in sorted(root.glob("*/scenario.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            scenarios.append(Scenario(
                id=data["id"],
                name=data["name"],
                difficulty=data.get("difficulty", "standard"),
                category=data.get("category", "general"),
                objective=data.get("objective", ""),
                brief=data.get("brief", ""),
                artifacts=data.get("artifacts", []),
                hints=data.get("hints", []),
                solution=data.get("solution", ""),
                success_criteria=data.get("success_criteria", []),
            ))
        except Exception:
            continue
    return scenarios


def get_scenario(scenario_id: str) -> Scenario | None:
    for s in load_scenarios():
        if s.id == scenario_id:
            return s
    return None
