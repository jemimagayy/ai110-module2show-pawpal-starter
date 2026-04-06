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

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
