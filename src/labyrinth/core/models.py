from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any


@dataclass
class Scenario:
    id: str
    name: str
    difficulty: str
    category: str
    objective: str
    brief: str
    artifacts: list[dict[str, str]]
    hints: list[str]
    solution: str
    success_criteria: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LabCase:
    lab_id: str
    scenario_id: str
    name: str
    path: str
    created_at: str
    objective: str
    difficulty: str
    category: str
    hints_total: int
    status: str = "created"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
