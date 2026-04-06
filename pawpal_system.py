from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    task_type: str
    duration: int           # in minutes
    priority: int           # 1 (low) to 5 (high)
    pet_name: str = ""      # name of the pet this task belongs to
    scheduled_time: str = ""  # expected format: "HH:MM"
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_complete = True

    def is_overdue(self) -> bool:
        """Return True if the task missed its scheduled time.

        Compares scheduled_time (HH:MM) against the current time.
        Returns False if scheduled_time is not set.
        """
        if not self.scheduled_time:
            return False
        try:
            task_time = datetime.strptime(self.scheduled_time, "%H:%M").time()
            return datetime.now().time() > task_time and not self.is_complete
        except ValueError:
            return False

    def reschedule(self, new_time: str) -> None:
        """Update the scheduled time for this task. Expected format: 'HH:MM'."""
        self.scheduled_time = new_time

    def to_dict(self) -> dict:
        """Convert task to a dictionary (useful for Streamlit display)."""
        return {
            "task_type": self.task_type,
            "duration": self.duration,
            "priority": self.priority,
            "pet_name": self.pet_name,
            "scheduled_time": self.scheduled_time,
            "is_complete": self.is_complete,
        }


@dataclass
class Pet:
    name: str
    species: str
    age: int
    medications: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet. Sets task.pet_name to this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_summary(self) -> str:
        """Return a readable summary of this pet's info and tasks."""
        meds = ", ".join(self.medications) if self.medications else "none"
        task_lines = "\n".join(
            f"  - [{t.priority}] {t.task_type} ({t.duration} min) @ {t.scheduled_time or 'unscheduled'}"
            for t in self.tasks
        )
        summary = (
            f"{self.name} ({self.species}, {self.age}yr old)\n"
            f"  Medications: {meds}\n"
        )
        if task_lines:
            summary += f"  Tasks:\n{task_lines}"
        else:
            summary += "  Tasks: none"
        return summary


@dataclass
class Owner:
    name: str
    available_time: int     # total minutes available today
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all pets, preserving pet_name on each task."""
        return [task for pet in self.pets for task in pet.get_tasks()]

    def set_availability(self, minutes: int) -> None:
        """Update how much time the owner has today."""
        self.available_time = minutes

    def get_preferences(self) -> dict:
        """Return the owner's scheduling preferences."""
        return self.preferences


@dataclass
class Conflict:
    task_a: Task
    task_b: Task
    reason: str


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        # available_time and tasks read directly from owner to avoid stale copies
        self.generated_plan: list[Task] = []
        self.reasoning: str = ""

    @property
    def available_time(self) -> int:
        """Always reflects the owner's current availability."""
        return self.owner.available_time

    @property
    def tasks(self) -> list[Task]:
        """Always reflects the current tasks across all owner's pets."""
        return self.owner.get_all_tasks()

    def sort_tasks(self) -> list[Task]:
        """Sort tasks by priority (high first), then duration (short first)."""
        return sorted(self.tasks, key=lambda t: (-t.priority, t.duration))

    def check_conflicts(self) -> list[Conflict]:
        """Detect scheduling conflicts between tasks.

        Two tasks conflict when both have a scheduled_time and their time
        windows overlap: [start, start + duration) overlaps for both.
        Returns a list of Conflict(task_a, task_b, reason).
        """
        conflicts: list[Conflict] = []
        timed = [t for t in self.tasks if t.scheduled_time]

        for i in range(len(timed)):
            for j in range(i + 1, len(timed)):
                a, b = timed[i], timed[j]
                try:
                    a_start = datetime.strptime(a.scheduled_time, "%H:%M")
                    b_start = datetime.strptime(b.scheduled_time, "%H:%M")
                except ValueError:
                    continue

                def to_minutes(dt: datetime) -> int:
                    return dt.hour * 60 + dt.minute

                a_start_m = to_minutes(a_start)
                b_start_m = to_minutes(b_start)
                a_end_m = a_start_m + a.duration
                b_end_m = b_start_m + b.duration

                if a_start_m < b_end_m and b_start_m < a_end_m:
                    reason = (
                        f"{a.task_type} for {a.pet_name} ({a.scheduled_time}, "
                        f"{a.duration} min) overlaps with "
                        f"{b.task_type} for {b.pet_name} ({b.scheduled_time}, "
                        f"{b.duration} min)"
                    )
                    conflicts.append(Conflict(task_a=a, task_b=b, reason=reason))

        return conflicts

    def generate_plan(self) -> list[Task]:
        """Build a daily plan that fits within available time.

        Tasks are sorted by priority (high first), then duration (short first).
        Tasks are added greedily until available_time is exhausted.
        Skipped tasks are noted in self.reasoning.
        Scheduled tasks have their times written back via reschedule() so that
        Pet task lists stay up to date.
        """
        sorted_tasks = self.sort_tasks()
        plan: list[Task] = []
        time_used = 0
        included: list[str] = []
        skipped: list[str] = []

        # Assign slots starting at 08:00 for tasks without a scheduled_time
        slot_hour = 8
        slot_minute = 0

        for task in sorted_tasks:
            if time_used + task.duration <= self.available_time:
                if not task.scheduled_time:
                    new_time = f"{slot_hour:02d}:{slot_minute:02d}"
                    task.reschedule(new_time)
                    slot_minute += task.duration
                    slot_hour += slot_minute // 60
                    slot_minute = slot_minute % 60

                plan.append(task)
                time_used += task.duration
                included.append(
                    f"  + [{task.priority}] {task.task_type} for {task.pet_name} "
                    f"@ {task.scheduled_time} ({task.duration} min)"
                )
            else:
                skipped.append(
                    f"  - [{task.priority}] {task.task_type} for {task.pet_name} "
                    f"({task.duration} min) — not enough time remaining "
                    f"({self.available_time - time_used} min left)"
                )

        self.generated_plan = plan

        reason_parts = [f"Available time: {self.available_time} min. Tasks sorted by priority (high first), then duration (short first)."]
        if included:
            reason_parts.append("Scheduled:\n" + "\n".join(included))
        if skipped:
            reason_parts.append("Skipped:\n" + "\n".join(skipped))
        reason_parts.append(f"Total time used: {time_used}/{self.available_time} min.")
        self.reasoning = "\n\n".join(reason_parts)

        return self.generated_plan
