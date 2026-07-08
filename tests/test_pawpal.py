import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


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
