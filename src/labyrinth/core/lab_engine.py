from __future__ import annotations
import datetime as dt
import json
import random
import re
import shutil
from pathlib import Path

from .models import LabCase, Scenario
from .paths import labs_dir


def slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "lab"


def render_template(text: str, lab_id: str, scenario: Scenario) -> str:
    now = dt.datetime.now().isoformat(timespec="seconds")
    fake_token = "sk_live_FAKE_" + "".join(random.choice("ABCDEF0123456789") for _ in range(24))
    fake_case = "".join(random.choice("0123456789abcdef") for _ in range(10))
    return (
        text.replace("{{LAB_ID}}", lab_id)
            .replace("{{SCENARIO_ID}}", scenario.id)
            .replace("{{SCENARIO_NAME}}", scenario.name)
            .replace("{{CREATED_AT}}", now)
            .replace("{{FAKE_TOKEN}}", fake_token)
            .replace("{{CASE_HASH}}", fake_case)
    )


def create_lab(scenario: Scenario, base_dir: Path | None = None) -> LabCase:
    base = base_dir or labs_dir()
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    lab_id = f"{slug(scenario.id)}-{stamp}"
    lab_path = base / lab_id
    lab_path.mkdir(parents=True, exist_ok=True)

    for item in scenario.artifacts:
        rel = item.get("path", "artifact.txt")
        content = render_template(item.get("content", ""), lab_id, scenario)
        target = lab_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    (lab_path / "case").mkdir(exist_ok=True)
    (lab_path / "answer").mkdir(exist_ok=True)

    case = LabCase(
        lab_id=lab_id,
        scenario_id=scenario.id,
        name=scenario.name,
        path=str(lab_path),
        created_at=dt.datetime.now().isoformat(timespec="seconds"),
        objective=scenario.objective,
        difficulty=scenario.difficulty,
        category=scenario.category,
        hints_total=len(scenario.hints),
    )

    (lab_path / "case" / "case.json").write_text(json.dumps(case.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    (lab_path / "case" / "brief.md").write_text(
        f"# {scenario.name}\n\n## Objective\n\n{scenario.objective}\n\n## Brief\n\n{scenario.brief}\n\n## Success criteria\n\n" +
        "\n".join(f"- {x}" for x in scenario.success_criteria) + "\n",
        encoding="utf-8"
    )
    (lab_path / "answer" / "solution.md").write_text(f"# Solution\n\n{scenario.solution}\n", encoding="utf-8")
    (lab_path / "answer" / "hints.md").write_text("\n\n".join(f"## Hint {i+1}\n\n{h}" for i, h in enumerate(scenario.hints)), encoding="utf-8")

    return case


def list_labs() -> list[Path]:
    root = labs_dir()
    return sorted([p for p in root.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)


def load_lab_case(lab_path: Path) -> dict:
    case_path = Path(lab_path) / "case" / "case.json"
    if not case_path.exists():
        raise FileNotFoundError(f"Missing case file: {case_path}")
    return json.loads(case_path.read_text(encoding="utf-8"))


def export_lab(lab_path: Path) -> Path:
    lab_path = Path(lab_path)
    out = lab_path.with_suffix(".zip")
    if out.exists():
        out.unlink()
    shutil.make_archive(str(lab_path), "zip", root_dir=lab_path.parent, base_dir=lab_path.name)
    return out
