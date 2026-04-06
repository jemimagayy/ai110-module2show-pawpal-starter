from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    task_type: str
    duration: int           # in minutes
    priority: int           # 1 (low) to 5 (high)
    scheduled_time: str = ""
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def is_overdue(self) -> bool:
        """Return True if the task missed its scheduled time."""
        pass

    def reschedule(self, new_time: str) -> None:
        """Update the scheduled time for this task."""
        pass

    def to_dict(self) -> dict:
        """Convert task to a dictionary (useful for Streamlit display)."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    medications: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass

    def get_summary(self) -> str:
        """Return a readable summary of this pet's info and tasks."""
        pass


@dataclass
class Owner:
    name: str
    available_time: int     # total minutes available today
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        pass

    def set_availability(self, minutes: int) -> None:
        """Update how much time the owner has today."""
        pass

    def get_preferences(self) -> dict:
        """Return the owner's scheduling preferences."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.tasks: list[Task] = []
        self.available_time: int = owner.available_time
        self.generated_plan: list[Task] = []
        self.reasoning: str = ""

    def sort_tasks(self) -> list[Task]:
        """Sort tasks by priority and duration."""
        pass

    def check_conflicts(self) -> list[tuple]:
        """Detect scheduling conflicts between tasks."""
        pass

    def generate_plan(self) -> list[Task]:
        """Build a daily plan that fits within available time."""
        pass