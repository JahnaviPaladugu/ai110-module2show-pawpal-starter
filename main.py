from pawpal_system import Owner, Pet, Task, DailyPlanner


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------

def section(title: str) -> None:
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_task_list(tasks: list[Task], label: str = "") -> None:
    if label:
        print(f"\n  [{label}]")
    if not tasks:
        print("    (none)")
        return
    col_time = 7
    col_name = 24
    col_pet  = 14
    col_rec  = 10
    col_due  = 12
    header  = (
        f"    {'TIME':<{col_time}}"
        f"{'TASK':<{col_name}}"
        f"{'PET':<{col_pet}}"
        f"{'RECURS':<{col_rec}}"
        f"{'DUE DATE':<{col_due}}"
    )
    divider = "    " + "-" * (col_time + col_name + col_pet + col_rec + col_due)
    print(header)
    print(divider)
    for t in tasks:
        print(
            f"    {(t.start_time or '?????'):<{col_time}}"
            f"{t.name:<{col_name}}"
            f"{t.pet_name:<{col_pet}}"
            f"{t.recurrence:<{col_rec}}"
            f"{(t.due_date or 'n/a'):<{col_due}}"
        )
    print(divider)


# ---------------------------------------------------------------------------
# Setup — owner and pets
# ---------------------------------------------------------------------------

owner = Owner(
    name="Alex Rivera",
    email="alex@example.com",
    available_start="17:00",
    available_end="21:00",
)

biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age_years=3)
mochi   = Pet(name="Mochi",   species="cat", breed="Scottish Fold",    age_years=5)

owner.add_pet(biscuit)
owner.add_pet(mochi)

# ---------------------------------------------------------------------------
# Tasks — include recurring ones and two forced to the SAME time slot
# ---------------------------------------------------------------------------

# Biscuit
biscuit.add_task(Task("Evening Walk",   "walk",        duration_min=30, priority="high",
                      preferred_time="evening", recurrence="daily",  due_date="2026-07-07"))
biscuit.add_task(Task("Dinner Feeding", "feed",        duration_min=10, priority="high",
                      preferred_time="evening", recurrence="daily",  due_date="2026-07-07"))
biscuit.add_task(Task("Heartworm Med",  "meds",        duration_min=5,  priority="high",
                      preferred_time="any",     recurrence="weekly", due_date="2026-07-07"))
biscuit.add_task(Task("Fetch Play",     "enrichment",  duration_min=20, priority="medium",
                      preferred_time="evening"))
# Force to 17:00 to create a conflict with Mochi's task below
biscuit.add_task(Task("Brush Coat",     "groom",       duration_min=15, priority="low",
                      preferred_time="evening", forced_start="17:00"))

# Mochi
mochi.add_task(Task("Wet Food Feeding", "feed",        duration_min=5,  priority="high",
                    preferred_time="evening", recurrence="daily",  due_date="2026-07-07"))
mochi.add_task(Task("Flea Treatment",   "meds",        duration_min=5,  priority="high",
                    preferred_time="any"))
# Also forced to 17:00 — intentional conflict with Biscuit's Brush Coat
mochi.add_task(Task("Puzzle Feeder",    "enrichment",  duration_min=15, priority="medium",
                    preferred_time="evening", forced_start="17:00"))

# ---------------------------------------------------------------------------
# Generate schedule
# ---------------------------------------------------------------------------

planner = DailyPlanner(owner=owner)
planner.generate_schedule()
all_scheduled = [slot.task for slot in planner.schedule]

# ===========================================================================
# DEMO 1 — Conflict detection
# ===========================================================================

section("DEMO 1 -- CONFLICT DETECTION")
print("""
  Strategy: convert each slot to an integer minute range [start, start+duration).
  Two ranges overlap when  a_start < b_end  AND  b_start < a_end.
  Returns warning strings — never crashes the program.

  'Brush Coat' (Biscuit) and 'Puzzle Feeder' (Mochi) are both
  forced to 17:00 to trigger the check.
""")

conflicts = planner.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  !! {warning}")
else:
    print("  No conflicts found.")

# ===========================================================================
# DEMO 2 — Recurring task: spawn_next() with timedelta
# ===========================================================================

section("DEMO 2 -- RECURRING TASKS  (spawn_next + timedelta)")
print("""
  When a daily/weekly task is marked complete, spawn_next() creates
  a fresh copy with  due_date = due_date + timedelta(days=1 or 7).
  The original task is NOT modified.
""")

recurring_tasks = [t for t in all_scheduled if t.recurrence != "none"]
print_task_list(recurring_tasks, "recurring tasks BEFORE mark_done")

# Mark them all done and spawn next occurrences
spawned: list[tuple[Task, Task]] = []
for task in recurring_tasks:
    task.mark_done()
    next_task = task.spawn_next()
    if next_task:
        spawned.append((task, next_task))

print_task_list([n for _, n in spawned], "spawned next occurrences (due_date + timedelta)")

# Show the delta clearly
print("\n  Due-date advancement breakdown:")
for original, nxt in spawned:
    days = 1 if original.recurrence == "daily" else 7
    print(f"    {original.name:<22}  {original.due_date}  +{days}d  ->  {nxt.due_date}")

# ===========================================================================
# DEMO 3 — Auto-add spawned tasks back to pet
# ===========================================================================

section("DEMO 3 -- AUTO-ADD NEXT OCCURRENCE TO PET")
print("\n  Calling pet.add_task(next_task) for each spawned task.")
print("  The old completed task stays in history; the new one is pending.\n")

for original, nxt in spawned:
    # Find which pet owns the original task
    for pet in owner.get_pets():
        if any(t is original for t in pet.get_tasks()):
            pet.add_task(nxt)
            print(f"  Added '{nxt.name}' (due {nxt.due_date}) to {pet.name}")
            break

print()
for pet in owner.get_pets():
    pending = len(pet.get_pending_tasks())
    total   = len(pet.get_tasks())
    print(f"  {pet.name}: {total} total tasks, {pending} pending")
