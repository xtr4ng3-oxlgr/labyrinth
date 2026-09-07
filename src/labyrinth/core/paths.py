from __future__ import annotations
import sys
from pathlib import Path


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[3]


def resource_root() -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return project_root()


def scenarios_dir() -> Path:
    root = resource_root()
    candidates = [
        root / "scenarios",
        project_root() / "scenarios",
    ]
    for c in candidates:
        if c.exists():
            return c
    return project_root() / "scenarios"


def labs_dir() -> Path:
    p = project_root() / "labs"
    p.mkdir(exist_ok=True)
    return p


def reports_dir() -> Path:
    p = project_root() / "reports"
    p.mkdir(exist_ok=True)
    return p
