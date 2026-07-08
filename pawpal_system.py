from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    name: str
    category: Literal["walk", "feed", "meds", "groom", "enrichment"]
    duration_min: int
    priority: Literal["high", "medium", "low"] = "medium"
    preferred_time: Literal["morning", "afternoon", "evening", "any"] = "any"
    is_recurring: bool = False
    is_completed: bool = False

    def mark_done(self) -> None:
        pass

    def reset(self) -> None:
        pass

    def to_dict(self) -> dict:
        pass


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age_years: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, _task: Task) -> None:
        pass

    def remove_task(self, _task_name: str) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass

    def get_pending_tasks(self) -> list[Task]:
        pass


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(
        self,
        name: str,
        email: str,
        available_start: str = "00:00",  # "HH:MM" 24-hour
        available_end: str = "23:59",
    ) -> None:
        self.name = name
        self.email = email
        self.available_start = available_start
        self.available_end = available_end
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


# ---------------------------------------------------------------------------
# DailyPlanner
# ---------------------------------------------------------------------------

class DailyPlanner:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.available_minutes: int = 0   # derived from owner's time window
        self.schedule: list[dict] = []

    def generate_schedule(self) -> list[dict]:
        pass

    def sort_tasks(self) -> list[Task]:
        pass

    def filter_by_time_window(self, tasks: list[Task]) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass

    def display_schedule(self) -> str:
        pass
