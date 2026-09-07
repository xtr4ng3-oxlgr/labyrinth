from __future__ import annotations
from pathlib import Path
from .scenario_loader import get_scenario


def get_hint(scenario_id: str, level: int) -> str:
    scenario = get_scenario(scenario_id)
    if not scenario:
        return "Scenario not found."
    if not scenario.hints:
        return "No hints available."
    index = max(1, min(level, len(scenario.hints))) - 1
    return scenario.hints[index]


def get_solution(scenario_id: str) -> str:
    scenario = get_scenario(scenario_id)
    if not scenario:
        return "Scenario not found."
    return scenario.solution
