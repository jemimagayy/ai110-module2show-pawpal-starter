# PawPal+ Project Reflection

## 1. System Design
**Core Actions**
- Enter owner + pet info into system
- Add/edit tasks
- Generate a daily plan

**Building Blocks**
- Classes: Owner, Pet, Task, Scheduler
***Attributes***
- Pet: name, species, age, medications
- Task: task_type, scheduled_time, is_complete
- Owner: name, age, gender, height, weight
- Scheduler: reference to owner, tasks, available_time, generated_plan, reasoning
***Methods**
- Pet: add_task(), get_tasks()
- Scheduler: sort_tasks(), check_conflicts()
- Task: mark_complete(), is_overdue(), reschedule(new_time), to_dict()
- Owner: add_pet(pet), get_all_tasks(), set_availability(minutes), get_preferences()

**a. Initial design**

![UML Diagram](image-1.png)

- Owner holds the user's info and their list of pets. It is the entry point — the Scheduler reads from it to   understand time constraints and preferences.
- Pet represents an individual animal. It owns a list of Tasks and knows its own medications and details.
- Task is a single care item with a type, duration, and priority. It knows its own state (complete or not) and can reschedule itself.
- Scheduler is the brain. It takes all tasks from the Owner's pets and produces an ordered daily plan that fits within available time, noting why it made each decision.

**b. Design changes**

Several structural changes were made to the skeleton after design review:

1. **Added `pet_name` field to `Task`** — the original design had no back-reference from a task to its pet. Once tasks are collected into a flat list (e.g. via `Owner.get_all_tasks()`), there was no way to tell which pet each task belonged to. Adding `pet_name` preserves that context for display and scheduling decisions.

2. **Removed duplicate `available_time` and `tasks` from `Scheduler`** — the original skeleton stored copies of both in the `Scheduler`, separate from the `Owner`. If `Owner.set_availability()` was called after the `Scheduler` was created, the scheduler's copy would go stale. Replacing them with `@property` accessors that delegate directly to `owner` means there is a single source of truth.

3. **Introduced a `Conflict` dataclass** — `check_conflicts()` originally returned `list[tuple]` with no documented structure. An untyped tuple forces the caller to guess what each position means. A `Conflict(task_a, task_b, reason)` dataclass makes the relationship explicit and easier to use in `generate_plan()` and in the UI.

4. **Standardised `scheduled_time` format to `"HH:MM"`** — `is_overdue()` needs to compare times, but a plain unformatted string makes that impossible reliably. Documenting the expected format is the minimum needed before the method can be implemented correctly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
