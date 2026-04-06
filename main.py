from pawpal_system import Task, Pet, Owner, Scheduler


def main():
    # --- Owner ---
    owner = Owner(name="Jamie", available_time=120)

    # --- Pets ---
    bella = Pet(name="Bella", species="Dog", age=4, medications=["Flea tablet"])
    mochi = Pet(name="Mochi", species="Cat", age=2)

    owner.add_pet(bella)
    owner.add_pet(mochi)

    # --- Tasks ---
    walk = Task(task_type="Walk", duration=30, priority=5, scheduled_time="08:00")
    feed_bella = Task(task_type="Feeding", duration=10, priority=4, scheduled_time="08:30")
    groom = Task(task_type="Grooming", duration=20, priority=2, scheduled_time="09:00")
    feed_mochi = Task(task_type="Feeding", duration=10, priority=4, scheduled_time="08:35")
    medication = Task(task_type="Medication", duration=5, priority=5, scheduled_time="09:30")

    bella.add_task(walk)
    bella.add_task(feed_bella)
    bella.add_task(groom)
    mochi.add_task(feed_mochi)
    mochi.add_task(medication)

    # --- Schedule ---
    scheduler = Scheduler(owner)

    conflicts = scheduler.check_conflicts()
    if conflicts:
        print("Conflicts detected before scheduling:")
        for c in conflicts:
            print(f"  ! {c.reason}")
        print()

    scheduler.generate_plan()

    # --- Print Today's Schedule ---
    print("=" * 50)
    print("       Today's Schedule for", owner.name)
    print("=" * 50)

    if not scheduler.generated_plan:
        print("No tasks could be scheduled.")
    else:
        for task in sorted(scheduler.generated_plan, key=lambda t: t.scheduled_time):
            status = "[DONE]" if task.is_complete else "[    ]"
            print(
                f"{status}  {task.scheduled_time}  |  {task.task_type:<12}  "
                f"({task.duration:>3} min)  |  Priority {task.priority}  |  {task.pet_name}"
            )

    print()
    print("--- Scheduler Reasoning ---")
    print(scheduler.reasoning)
    print("=" * 50)


if __name__ == "__main__":
    main()
