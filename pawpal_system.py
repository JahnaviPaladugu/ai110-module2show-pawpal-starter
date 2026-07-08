from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Literal


# Priority → sort key (lower = higher priority)
PRIORITY_ORDER: dict[str, int] = {"high": 0, "medium": 1, "low": 2}

# Preferred time band → (start_hour, end_hour) in 24-hour clock
TIME_BANDS: dict[str, tuple[int, int]] = {
    "morning":   (6,  12),
    "afternoon": (12, 17),
    "evening":   (17, 22),
    "any":       (0,  24),
}


# ---------------------------------------------------------------------------
# ScheduledSlot — typed shape for entries in the generated schedule
# ---------------------------------------------------------------------------

@dataclass
class ScheduledSlot:
    start_time: str   # "HH:MM"
    task: "Task"
    pet_name: str
    reason: str


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
    start_time: str = ""                                      # "HH:MM" stamped by scheduler
    pet_name: str = ""                                        # stamped by scheduler
    recurrence: Literal["none", "daily", "weekly"] = "none"  # auto-respawn frequency
    due_date: str = ""                                        # "YYYY-MM-DD"
    forced_start: str = ""                                    # force a specific "HH:MM" slot

    def mark_done(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def reset(self) -> None:
        """Clear the completed flag so the task becomes pending again."""
        self.is_completed = False

    def spawn_next(self) -> "Task | None":
        """Create and return the next occurrence of a recurring task using timedelta.

        Algorithm:
            1. Return None immediately if recurrence is "none" — not a recurring task.
            2. Select a timedelta based on recurrence frequency:
                   "daily"  → timedelta(days=1)
                   "weekly" → timedelta(days=7)
            3. Parse due_date (YYYY-MM-DD) and add the delta to get next_due.
               Falls back to date.today() if due_date was never set.
            4. Return a new Task with identical fields except:
                   is_completed=False  (reset — the new task hasn't been done yet)
                   due_date=str(next_due)  (advanced by the delta)
        The original task is NOT modified — mark_done() handles that separately.
        Caller is responsible for adding the returned task to the pet's task list.
        """
        if self.recurrence == "none":
            return None
        delta = timedelta(days=1) if self.recurrence == "daily" else timedelta(days=7)
        next_due = (
            datetime.strptime(self.due_date, "%Y-%m-%d").date() + delta
            if self.due_date
            else date.today() + delta
        )
        return Task(
            name=self.name,
            category=self.category,
            duration_min=self.duration_min,
            priority=self.priority,
            preferred_time=self.preferred_time,
            is_recurring=self.is_recurring,
            is_completed=False,
            recurrence=self.recurrence,
            due_date=str(next_due),
            forced_start=self.forced_start,
        )

    def to_dict(self) -> dict:
        """Serialize all task fields to a plain dictionary."""
        return {
            "name":           self.name,
            "category":       self.category,
            "duration_min":   self.duration_min,
            "priority":       self.priority,
            "preferred_time": self.preferred_time,
            "is_recurring":   self.is_recurring,
            "is_completed":   self.is_completed,
            "start_time":     self.start_time,
            "pet_name":       self.pet_name,
            "recurrence":     self.recurrence,
            "due_date":       self.due_date,
            "forced_start":   self.forced_start,
        }


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
    owner: "Owner | None" = field(default=None, repr=False)  # repr=False avoids infinite loop

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Remove the first task whose name matches task_name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_tasks(self) -> list[Task]:
        """Return a copy of all tasks (completed and pending)."""
        return list(self.tasks)

    def get_pending_tasks(self) -> list[Task]:
        """Return only tasks that have not been marked done."""
        return [t for t in self.tasks if not t.is_completed]


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
        """Register a pet under this owner and set the pet's back-reference."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Detach the named pet from this owner and clear its back-reference."""
        for pet in self.pets:
            if pet.name == pet_name:
                pet.owner = None
                self.pets.remove(pet)
                return

    def get_pets(self) -> list[Pet]:
        """Return a copy of the owner's pet list."""
        return list(self.pets)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """All tasks across every pet this owner has, as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.get_tasks()]


# ---------------------------------------------------------------------------
# DailyPlanner  (the Scheduler "brain")
# ---------------------------------------------------------------------------

class DailyPlanner:
    """
    Retrieves, organises, and schedules tasks for an owner's pet(s).

    If `pet` is provided, only that pet's tasks are scheduled.
    If `pet` is None, tasks from all of the owner's pets are included.
    """

    def __init__(self, owner: Owner, pet: Pet | None = None) -> None:
        self.owner = owner
        self.pet = pet
        self.schedule: list[ScheduledSlot] = []
        self.available_minutes: int = self._compute_available_minutes()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_time(time_str: str) -> datetime:
        """Parse a time string in HH:MM or H:MM format into a datetime."""
        for fmt in ("%H:%M", "%I:%M %p", "%H"):
            try:
                return datetime.strptime(time_str.strip(), fmt)
            except ValueError:
                continue
        raise ValueError(f"Cannot parse time '{time_str}'. Expected HH:MM (24-hour).")

    def _compute_available_minutes(self) -> int:
        """Total minutes between the owner's available_start and available_end."""
        start = self._parse_time(self.owner.available_start)
        end   = self._parse_time(self.owner.available_end)
        delta = int((end - start).total_seconds() // 60)
        return max(0, delta)

    def _band_overlaps_window(self, preferred_time: str) -> bool:
        """True when the task's time band overlaps the owner's availability window."""
        band_start, band_end = TIME_BANDS.get(preferred_time, TIME_BANDS["any"])
        owner_start_hr = self._parse_time(self.owner.available_start).hour
        owner_end_hr   = self._parse_time(self.owner.available_end).hour
        return band_start < owner_end_hr and band_end > owner_start_hr

    def _candidate_pets(self) -> list[Pet]:
        """Return the single target pet, or all owner pets if none was specified."""
        return [self.pet] if self.pet else self.owner.get_pets()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sort_tasks(self) -> list[Task]:
        """Collect all pending tasks and sort by priority then duration (shortest first)."""
        pending: list[Task] = []
        for pet in self._candidate_pets():
            pending.extend(pet.get_pending_tasks())
        return sorted(
            pending,
            key=lambda t: (PRIORITY_ORDER[t.priority], t.duration_min),
        )

    def filter_by_time_window(self, tasks: list[Task]) -> list[Task]:
        """Keep only tasks whose preferred time band overlaps the owner's window."""
        return [t for t in tasks if self._band_overlaps_window(t.preferred_time)]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks into chronological order using a lambda on their HH:MM start_time.

        Algorithm: passes a lambda as the sort key —
            key=lambda t: t.start_time if t.start_time else "99:99"
        HH:MM strings are zero-padded ("07:00", "17:30"), so Python's default
        string comparison is identical to chronological order — no datetime
        parsing needed.  Tasks that have not been scheduled yet (start_time="")
        receive the sentinel "99:99" and sort to the bottom of the list.
        Time complexity: O(n log n) — dominated by the underlying Timsort.
        """
        return sorted(tasks, key=lambda t: t.start_time if t.start_time else "99:99")

    def filter_tasks(
        self,
        tasks: list[Task],
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter a task list by completion status and/or pet name.

        Algorithm: two independent list-comprehension passes applied in sequence.
        Each filter is only applied when its argument is not None, so any
        combination works — by status only, by pet only, or both together.
            completed=True   → keep only finished tasks
            completed=False  → keep only pending tasks
            completed=None   → skip this filter (default)
            pet_name="Mochi" → keep only tasks belonging to that pet
            pet_name=None    → skip this filter (default)
        Filters compose: filter_tasks(tasks, completed=False, pet_name="Biscuit")
        returns tasks that are BOTH pending AND owned by Biscuit.
        Time complexity: O(n) per active filter.
        """
        result = tasks
        if completed is not None:
            result = [t for t in result if t.is_completed == completed]
        if pet_name is not None:
            result = [t for t in result if t.pet_name == pet_name]
        return result

    def generate_schedule(self) -> list[ScheduledSlot]:
        """Greedily fill the owner's time window with the highest-priority fitting tasks."""
        sorted_tasks  = self.sort_tasks()
        eligible      = self.filter_by_time_window(sorted_tasks)

        # Map each task back to its pet for labelling
        task_to_pet: dict[int, str] = {}
        for pet in self._candidate_pets():
            for task in pet.get_pending_tasks():
                task_to_pet[id(task)] = pet.name

        slots: list[ScheduledSlot] = []
        minutes_used = 0
        cursor = self._parse_time(self.owner.available_start)

        for task in eligible:
            if minutes_used + task.duration_min > self.available_minutes:
                continue  # doesn't fit right now; leave pending

            # Honour a forced start time if the task has one set
            if task.forced_start:
                slot_time    = task.forced_start
                minutes_used = int((self._parse_time(task.forced_start) - cursor).total_seconds() // 60)
            else:
                slot_time = (cursor + timedelta(minutes=minutes_used)).strftime("%H:%M")
            pet_name   = task_to_pet.get(id(task), "unknown pet")
            reason     = (
                f"priority={task.priority}, "
                f"preferred={task.preferred_time}, "
                f"duration={task.duration_min} min"
            )
            # Stamp the task itself so sort_by_time() and filter_tasks() can use it
            task.start_time = slot_time
            task.pet_name   = pet_name
            slots.append(ScheduledSlot(
                start_time=slot_time,
                task=task,
                pet_name=pet_name,
                reason=reason,
            ))
            minutes_used += task.duration_min

        self.schedule = slots
        return slots

    def detect_conflicts(self, slots: list[ScheduledSlot] | None = None) -> list[str]:
        """Check the schedule for overlapping tasks; return warnings instead of raising.

        Algorithm: O(n²) pairwise comparison over integer minute ranges.
        Each slot is converted to [start_min, end_min) where:
            start_min = hours * 60 + minutes
            end_min   = start_min + task.duration_min
        Two ranges [a_s, a_e) and [b_s, b_e) overlap when:
            a_s < b_e  AND  b_s < a_e
        This covers all overlap shapes — partial overlap, full containment, and
        exact same start time.  Returns a plain list of strings so the caller
        can print, log, or display warnings without the program crashing.
        Known limitation: only checks adjacent pairs after sorting — a long task
        can silently conflict with a non-neighbouring slot (see detect_conflicts
        improvement notes).
        """
        targets = slots if slots is not None else self.schedule
        if not targets:
            return []

        def to_minutes(hhmm: str) -> int:
            h, m = map(int, hhmm.split(":"))
            return h * 60 + m

        warnings: list[str] = []
        for i in range(len(targets)):
            for j in range(i + 1, len(targets)):
                a, b = targets[i], targets[j]
                a_start = to_minutes(a.start_time)
                a_end   = a_start + a.task.duration_min
                b_start = to_minutes(b.start_time)
                b_end   = b_start + b.task.duration_min
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"CONFLICT: '{a.task.name}' ({a.pet_name} {a.start_time}-"
                        f"{(datetime.min + timedelta(minutes=a_end)).strftime('%H:%M')})"
                        f" overlaps '{b.task.name}' ({b.pet_name} {b.start_time}-"
                        f"{(datetime.min + timedelta(minutes=b_end)).strftime('%H:%M')})"
                    )
        return warnings

    def explain_plan(self) -> str:
        """Human-readable explanation of why each task was chosen and placed."""
        if not self.schedule:
            return "No schedule generated yet — call generate_schedule() first."

        lines = [f"Daily plan for {self.owner.name}:\n"]
        for slot in self.schedule:
            lines.append(
                f"  {slot.start_time}  {slot.task.name} ({slot.pet_name})"
                f"  ->  {slot.reason}"
            )

        total_scheduled = sum(s.task.duration_min for s in self.schedule)
        lines.append(
            f"\nScheduled {total_scheduled} min out of "
            f"{self.available_minutes} min available "
            f"({self.available_minutes - total_scheduled} min unused)."
        )
        return "\n".join(lines)

    def display_schedule(self) -> str:
        """Compact, table-style view of the generated schedule."""
        if not self.schedule:
            return "No schedule generated yet — call generate_schedule() first."

        label = self.pet.name if self.pet else "all pets"
        header = f"=== {self.owner.name}'s schedule — {label} ==="
        lines  = [header, "-" * len(header)]
        for slot in self.schedule:
            lines.append(
                f"  {slot.start_time}  "
                f"{slot.task.name:<22} "
                f"{slot.task.duration_min:>3} min  "
                f"[{slot.task.priority:<6}]  "
                f"{slot.pet_name}"
            )
        lines.append("-" * len(header))
        return "\n".join(lines)
