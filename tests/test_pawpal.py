import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, DailyPlanner, ScheduledSlot


def test_mark_done_changes_status():
    """mark_done() should flip is_completed from False to True."""
    task = Task(name="Morning Walk", category="walk", duration_min=20)

    assert task.is_completed is False  # starts incomplete

    task.mark_done()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task count by 1."""
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)

    assert len(pet.get_tasks()) == 0  # starts with no tasks

    pet.add_task(Task(name="Dinner Feeding", category="feed", duration_min=10))

    assert len(pet.get_tasks()) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should order tasks earliest start_time first."""
    tasks = [
        Task(name="Evening Walk",    category="walk", duration_min=30, start_time="17:00"),
        Task(name="Morning Feed",    category="feed", duration_min=10, start_time="07:00"),
        Task(name="Afternoon Meds", category="meds", duration_min=5,  start_time="13:00"),
    ]

    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
    owner.add_pet(pet)
    planner = DailyPlanner(owner)

    result = planner.sort_by_time(tasks)

    assert [t.start_time for t in result] == ["07:00", "13:00", "17:00"]


def test_sort_by_time_unscheduled_tasks_sort_last():
    """Tasks with no start_time (empty string) should appear after all scheduled tasks."""
    tasks = [
        Task(name="Unscheduled Groom", category="groom",       duration_min=20, start_time=""),
        Task(name="Morning Walk",      category="walk",         duration_min=30, start_time="08:00"),
        Task(name="Evening Feed",      category="feed",         duration_min=10, start_time="18:00"),
    ]

    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
    owner.add_pet(pet)
    planner = DailyPlanner(owner)

    result = planner.sort_by_time(tasks)

    assert result[-1].name == "Unscheduled Groom"
    assert result[0].start_time == "08:00"


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_daily_recurrence_spawns_next_day_task():
    """Marking a daily task complete and calling spawn_next() should create a
    task due the following day with is_completed reset to False."""
    task = Task(
        name="Morning Walk",
        category="walk",
        duration_min=30,
        recurrence="daily",
        due_date="2026-07-07",
    )

    task.mark_done()
    next_task = task.spawn_next()

    assert next_task is not None
    assert next_task.due_date == "2026-07-08"
    assert next_task.is_completed is False


def test_spawn_next_preserves_task_fields():
    """The spawned task should carry over all fields from the original."""
    task = Task(
        name="Evening Meds",
        category="meds",
        duration_min=5,
        priority="high",
        preferred_time="evening",
        recurrence="daily",
        due_date="2026-07-07",
        forced_start="19:00",
    )

    next_task = task.spawn_next()

    assert next_task.name == task.name
    assert next_task.priority == task.priority
    assert next_task.preferred_time == task.preferred_time
    assert next_task.forced_start == task.forced_start
    assert next_task.recurrence == "daily"


def test_spawn_next_returns_none_for_non_recurring():
    """spawn_next() must return None when recurrence is 'none'."""
    task = Task(name="One-off Bath", category="groom", duration_min=45, recurrence="none")

    assert task.spawn_next() is None


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_overlapping_slots():
    """Two slots whose time ranges overlap should produce at least one warning."""
    # task_a runs 08:00–09:00; task_b starts at 08:30 — clearly overlaps
    task_a = Task(name="Morning Walk", category="walk", duration_min=60)
    task_b = Task(name="Morning Feed", category="feed", duration_min=30)

    slots = [
        ScheduledSlot(start_time="08:00", task=task_a, pet_name="Biscuit", reason=""),
        ScheduledSlot(start_time="08:30", task=task_b, pet_name="Biscuit", reason=""),
    ]

    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
    owner.add_pet(pet)
    planner = DailyPlanner(owner)

    warnings = planner.detect_conflicts(slots)

    assert len(warnings) > 0
    assert "CONFLICT" in warnings[0]


def test_detect_conflicts_no_warning_for_adjacent_slots():
    """Slots that share an endpoint but do not overlap should not produce a warning."""
    # task_a runs 08:00–08:30; task_b starts at exactly 08:30 — adjacent, not overlapping
    task_a = Task(name="Morning Walk", category="walk", duration_min=30)
    task_b = Task(name="Morning Feed", category="feed", duration_min=20)

    slots = [
        ScheduledSlot(start_time="08:00", task=task_a, pet_name="Biscuit", reason=""),
        ScheduledSlot(start_time="08:30", task=task_b, pet_name="Biscuit", reason=""),
    ]

    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
    owner.add_pet(pet)
    planner = DailyPlanner(owner)

    warnings = planner.detect_conflicts(slots)

    assert warnings == []


def test_detect_conflicts_empty_schedule_returns_no_warnings():
    """An empty slot list should return an empty warnings list without error."""
    owner = Owner(name="Alex", email="alex@example.com")
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
    owner.add_pet(pet)
    planner = DailyPlanner(owner)

    assert planner.detect_conflicts([]) == []
