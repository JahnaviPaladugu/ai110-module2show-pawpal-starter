# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Sample Output : 
====================================================
  PAWPAL+  --  TODAY'S SCHEDULE
====================================================

  Owner : Alex Rivera  (alex@example.com)
  Window: 17:00 - 21:00  (240 min available)
  Pets  : Biscuit, Mochi

====================================================
  SCHEDULE
====================================================
  TIME   TASK                    DURATIONPRIORITY PET           
  --------------------------------------------------------------
  17:00  Heartworm Med           5 min   high     Biscuit       
  17:05  Wet Food Feeding        5 min   high     Mochi         
  17:10  Flea Treatment          5 min   high     Mochi         
  17:15  Dinner Feeding          10 min  high     Biscuit       
  17:25  Evening Walk            30 min  high     Biscuit       
  17:55  Puzzle Feeder           15 min  medium   Mochi         
  18:10  Fetch Play              20 min  medium   Biscuit       
  18:30  Brush Coat              15 min  low      Biscuit       
  --------------------------------------------------------------
  Total: 105 min scheduled  |  135 min unused


====================================================
  REASONING
====================================================
Daily plan for Alex Rivera:

  17:00  Heartworm Med (Biscuit)  ->  priority=high, preferred=any, duration=5 min
  17:05  Wet Food Feeding (Mochi)  ->  priority=high, preferred=evening, duration=5 min
  17:10  Flea Treatment (Mochi)  ->  priority=high, preferred=any, duration=5 min
  17:15  Dinner Feeding (Biscuit)  ->  priority=high, preferred=evening, duration=10 min
  17:25  Evening Walk (Biscuit)  ->  priority=high, preferred=evening, duration=30 min
  17:55  Puzzle Feeder (Mochi)  ->  priority=medium, preferred=evening, duration=15 min
  18:10  Fetch Play (Biscuit)  ->  priority=medium, preferred=evening, duration=20 min
  18:30  Brush Coat (Biscuit)  ->  priority=low, preferred=evening, duration=15 min

Scheduled 105 min out of 240 min available (135 min unused).

====================================================
  TASK SUMMARY BY PET
====================================================

  Biscuit (Golden Retriever)
    Total tasks   : 5
    Scheduled today: 5
    Still pending : 5

  Mochi (Scottish Fold)
    Total tasks   : 4
    Scheduled today: 3
    Still pending : 4




## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
python -m pytest
========================================================================================================================== test session starts ==========================================================================================================================
platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Redacted\Codepath\AI110\Week4\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 2 items                                                                                                                                                                                                                                                        

tests\test_pawpal.py ..                                                                                                                                                                                                                                            [100%]


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting |sort_tasks, sort_by_time(tasks) | e.g., by priority, duration |
| Filtering |filter_by_time_window(tasks),filter_tasks(tasks, completed=, pet_name=)  | e.g., skip tasks if time runs out |
| Conflict handling | detect_conflicts(slots) | e.g., overlapping time slots |
| Recurring tasks | mark_done(),spawn_next(), reset() | e.g., daily vs. weekly |



## Testing PawPal+ :
> Python Command to run: python -m pytest
> Tests overview: 
The tests cover sorting logic using tasks that start at different times of the day and checks to make sure they are sorted correctly. 
It also covers recurrence logic where a new task that is set to reoccur will generate a new task for the next day at the same time
Lastly, the tests cover conflict detection to ensure that warning messages are generated when there are 2 tasks that have overlapping time. 



> Terminal Output: 
python -m pytest
========================================================================================================================== test session starts ==========================================================================================================================
platform win32 -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\jahna\OneDrive\Desktop\Codepath\AI110\Week4\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 10 items                                                                                                                                                                                                                                                       

tests\test_pawpal.py ..........                                                                                                                                                                                                                                    [100%]

========================================================================================================================== 10 passed in 0.05s ===========================================================================================================================

> Confidence Level: 4 because all the test cases have passed and it thought of all the different test cases that I have also thought of. I didn't give it a 5 becuase we might've missed some bugs/logic and it overcomplicated some of the logic for the alorithms which could have been simplified. And, I believe overcomplicating simple logic may lead to more mistakes when further adding new features to the application.  




## 📸 Demo Walkthrough

### Features

| Feature | What it does |
|---|---|
| **Priority-based task sorting** | `sort_tasks()` collects every pending task and sorts by priority (high → medium → low), then by duration shortest-first within each priority tier. High-urgency tasks like medications always appear before grooming or enrichment. |
| **Chronological schedule display** | `sort_by_time()` re-orders the generated schedule by each task's stamped `HH:MM` start time using zero-padded string comparison. Tasks without an assigned time sink to the bottom via a `"99:99"` sentinel. |
| **Time-window filtering** | `filter_by_time_window()` drops any task whose preferred time band (morning 6–12, afternoon 12–17, evening 17–22) does not overlap the owner's availability window, so a "morning walk" is never scheduled for an owner who's only free at 7 PM. |
| **Composable task filtering** | `filter_tasks()` lets you narrow a task list by completion status, by pet name, or both at once. The UI uses this to separate pending from done tasks and to scope views to a single pet. |
| **Conflict detection with warnings** | `detect_conflicts()` does a pairwise comparison of every slot pair and flags any whose minute-ranges overlap. Each conflict surfaces as a distinct `st.warning` banner in the UI so nothing gets buried. |
| **Daily & weekly recurrence** | `spawn_next()` advances a completed task's `due_date` by one day (daily) or seven days (weekly) and returns a fresh copy with `is_completed=False`. The caller adds it back to the pet's task list, preserving the full history of the original. |
| **Greedy schedule generation** | `generate_schedule()` iterates tasks in priority-then-duration order and greedily packs them into the owner's available window, respecting `forced_start` overrides and skipping tasks that no longer fit. |
| **Human-readable plan explanation** | `explain_plan()` prints every scheduled slot with the reason it was chosen (priority, preferred time, duration), plus a summary of minutes used vs. available. |

---

### UI Features and User Actions

The app is divided into four sections that a user works through top to bottom:

- **Owner Info** — Enter your name, email, and the time window you're available (e.g. 17:00–21:00). Saving this locks in the daily scheduling window.
- **Add a Pet** — Register one or more pets (name, species, breed, age). Existing pets are shown below the form with a live count of their pending tasks.
- **Add a Task** — Assign a task to any registered pet. Fields include task name, category, duration, priority, preferred time of day, and whether it repeats daily. Tasks appear in the pet's expandable task list, sorted by priority with color-coded icons (🔴 high, 🟡 medium, 🟢 low).
- **Generate Today's Schedule** — Choose to schedule for a single pet or all pets at once. The app runs the full scheduling pipeline and displays a sorted, icon-annotated table. Conflict warnings appear immediately beneath the summary banner if any slots overlap. A "Why was this plan chosen?" expander shows the full reasoning. Checkboxes at the bottom let you mark tasks done directly from the schedule view.

---

### Example Workflow

1. **Enter owner info.** Type your name and set your availability to `17:00–21:00`. Click **Save owner**.
2. **Add a pet.** Enter `Biscuit`, species `dog`, breed `Golden Retriever`, age `3`. Click **Add pet**.
3. **Add tasks.** Add three tasks for Biscuit:
   - *Heartworm Med* — meds, 5 min, high priority, preferred: any
   - *Evening Walk* — walk, 30 min, high priority, preferred: evening, recurring daily
   - *Brush Coat* — groom, 15 min, low priority, preferred: evening
4. **Generate the schedule.** Select `Biscuit` from the dropdown and click **Generate schedule**.
5. **Read the output.** The table shows tasks in chronological order: Heartworm Med at 17:00, Evening Walk at 17:05, Brush Coat at 17:35. A green banner confirms no conflicts. The expander explains each placement.
6. **Mark a task done.** Check the box next to *Evening Walk*. Because it's a recurring daily task, call `spawn_next()` in code (or extend the UI) to queue tomorrow's walk automatically.

---

### Key Scheduler Behaviors to Notice

- **Shortest-first within a priority tier** — if two high-priority tasks exist, the shorter one is placed first to leave more room for others.
- **Tasks outside your time window are silently filtered** — a "morning" task won't appear if you're only free in the evening. No error is raised; the task stays pending for the next day.
- **Conflict warnings are non-fatal** — `detect_conflicts()` returns strings instead of raising exceptions. The schedule still displays; the warnings tell you what to fix.
- **Recurring tasks don't self-advance** — `spawn_next()` returns a new `Task` object but does not modify the original or add it to the pet automatically. This keeps the history of completed tasks intact.
- **`forced_start` tasks jump the queue** — a task with a hard start time is placed at that exact slot regardless of where the greedy cursor is, which can cause a conflict if the slot overlaps an earlier task.


> sample CLI output: 
python main.py                                                            

============================================================
  DEMO 1 -- CONFLICT DETECTION
============================================================

  Strategy: convert each slot to an integer minute range [start, start+duration).
  Two ranges overlap when  a_start < b_end  AND  b_start < a_end.
  Returns warning strings — never crashes the program.

  'Brush Coat' (Biscuit) and 'Puzzle Feeder' (Mochi) are both
  forced to 17:00 to trigger the check.

  !! CONFLICT: 'Heartworm Med' (Biscuit 17:00-17:05) overlaps 'Puzzle Feeder' (Mochi 17:00-17:15)
  !! CONFLICT: 'Heartworm Med' (Biscuit 17:00-17:05) overlaps 'Brush Coat' (Biscuit 17:00-17:15)
  !! CONFLICT: 'Wet Food Feeding' (Mochi 17:05-17:10) overlaps 'Puzzle Feeder' (Mochi 17:00-17:15)
  !! CONFLICT: 'Wet Food Feeding' (Mochi 17:05-17:10) overlaps 'Brush Coat' (Biscuit 17:00-17:15)
  !! CONFLICT: 'Flea Treatment' (Mochi 17:10-17:15) overlaps 'Puzzle Feeder' (Mochi 17:00-17:15)
  !! CONFLICT: 'Flea Treatment' (Mochi 17:10-17:15) overlaps 'Brush Coat' (Biscuit 17:00-17:15)
  !! CONFLICT: 'Dinner Feeding' (Biscuit 17:15-17:25) overlaps 'Fetch Play' (Biscuit 17:15-17:35)
  !! CONFLICT: 'Evening Walk' (Biscuit 17:25-17:55) overlaps 'Fetch Play' (Biscuit 17:15-17:35)
  !! CONFLICT: 'Puzzle Feeder' (Mochi 17:00-17:15) overlaps 'Brush Coat' (Biscuit 17:00-17:15)

============================================================
  DEMO 2 -- RECURRING TASKS  (spawn_next + timedelta)
============================================================

  When a daily/weekly task is marked complete, spawn_next() creates
  a fresh copy with  due_date = due_date + timedelta(days=1 or 7).
  The original task is NOT modified.


  [recurring tasks BEFORE mark_done]
    TIME   TASK                    PET           RECURS    DUE DATE    
    -------------------------------------------------------------------
    17:00  Heartworm Med           Biscuit       weekly    2026-07-07  
    17:05  Wet Food Feeding        Mochi         daily     2026-07-07  
    17:15  Dinner Feeding          Biscuit       daily     2026-07-07  
    17:25  Evening Walk            Biscuit       daily     2026-07-07  
    -------------------------------------------------------------------

  [spawned next occurrences (due_date + timedelta)]
    TIME   TASK                    PET           RECURS    DUE DATE    
    -------------------------------------------------------------------
    ?????  Heartworm Med                         weekly    2026-07-14  
    ?????  Wet Food Feeding                      daily     2026-07-08  
    ?????  Dinner Feeding                        daily     2026-07-08  
    ?????  Evening Walk                          daily     2026-07-08  
    -------------------------------------------------------------------

  Due-date advancement breakdown:
    Heartworm Med           2026-07-07  +7d  ->  2026-07-14
    Wet Food Feeding        2026-07-07  +1d  ->  2026-07-08
    Dinner Feeding          2026-07-07  +1d  ->  2026-07-08
    Evening Walk            2026-07-07  +1d  ->  2026-07-08

============================================================
  DEMO 3 -- AUTO-ADD NEXT OCCURRENCE TO PET
============================================================

  Calling pet.add_task(next_task) for each spawned task.
  The old completed task stays in history; the new one is pending.

  Added 'Heartworm Med' (due 2026-07-14) to Biscuit
  Added 'Wet Food Feeding' (due 2026-07-08) to Mochi
  Added 'Dinner Feeding' (due 2026-07-08) to Biscuit
  Added 'Evening Walk' (due 2026-07-08) to Biscuit

  Biscuit: 8 total tasks, 5 pending
  Mochi: 4 total tasks, 3 pending