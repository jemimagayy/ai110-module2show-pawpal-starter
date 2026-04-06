import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_task_mark_complete():
    task = Task(task_type="Walk", duration=30, priority=3)
    task.mark_complete()
    assert task.is_complete is True


def test_pet_add_task():
    pet = Pet(name="Bella", species="Dog", age=4)
    task = Task(task_type="Feeding", duration=10, priority=4)
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1
