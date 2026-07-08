from pawpal_system import Owner, Pet, Task, DailyPlanner


# ---------------------------------------------------------------------------
# Helper — pretty terminal banner
# ---------------------------------------------------------------------------

def section(title: str) -> None:
    width = 52
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_schedule(planner: DailyPlanner) -> None:
    slots = planner.schedule
    if not slots:
        print("  (no tasks scheduled)")
        return

    col_time  = 7
    col_task  = 24
    col_dur   = 8
    col_pri   = 9
    col_pet   = 14

    header = (
        f"  {'TIME':<{col_time}}"
        f"{'TASK':<{col_task}}"
        f"{'DURATION':<{col_dur}}"
        f"{'PRIORITY':<{col_pri}}"
        f"{'PET':<{col_pet}}"
    )
    divider = "  " + "-" * (col_time + col_task + col_dur + col_pri + col_pet)

    print(header)
    print(divider)
    for slot in slots:
        dur_str = f"{slot.task.duration_min} min"
        print(
            f"  {slot.start_time:<{col_time}}"
            f"{slot.task.name:<{col_task}}"
            f"{dur_str:<{col_dur}}"
            f"{slot.task.priority:<{col_pri}}"
            f"{slot.pet_name:<{col_pet}}"
        )
    print(divider)
    total = sum(s.task.duration_min for s in slots)
    print(f"  Total: {total} min scheduled  |  {planner.available_minutes - total} min unused\n")


# ---------------------------------------------------------------------------
# Setup — owner and pets
# ---------------------------------------------------------------------------

owner = Owner(
    name="Alex Rivera",
    email="alex@example.com",
    available_start="17:00",   # only free after 5 PM
    available_end="21:00",
)

biscuit = Pet(name="Biscuit", species="dog",  breed="Golden Retriever", age_years=3)
mochi   = Pet(name="Mochi",   species="cat",  breed="Scottish Fold",    age_years=5)

owner.add_pet(biscuit)
owner.add_pet(mochi)

# ---------------------------------------------------------------------------
# Tasks — mix of priorities, durations, and preferred times
# ---------------------------------------------------------------------------

# Biscuit's tasks
biscuit.add_task(Task("Evening Walk",      "walk",       duration_min=30, priority="high",   preferred_time="evening"))
biscuit.add_task(Task("Dinner Feeding",    "feed",       duration_min=10, priority="high",   preferred_time="evening"))
biscuit.add_task(Task("Heartworm Med",     "meds",       duration_min=5,  priority="high",   preferred_time="any"))
biscuit.add_task(Task("Fetch Play",        "enrichment", duration_min=20, priority="medium", preferred_time="evening"))
biscuit.add_task(Task("Brush Coat",        "groom",      duration_min=15, priority="low",    preferred_time="evening"))

# Mochi's tasks
mochi.add_task(Task("Wet Food Feeding",    "feed",       duration_min=5,  priority="high",   preferred_time="evening"))
mochi.add_task(Task("Flea Treatment",      "meds",       duration_min=5,  priority="high",   preferred_time="any"))
mochi.add_task(Task("Puzzle Feeder",       "enrichment", duration_min=15, priority="medium", preferred_time="evening"))
mochi.add_task(Task("Morning Feeding",     "feed",       duration_min=5,  priority="high",   preferred_time="morning"))  # outside window — filtered out

# ---------------------------------------------------------------------------
# Run the scheduler
# ---------------------------------------------------------------------------

planner = DailyPlanner(owner=owner)   # schedules across all pets
planner.generate_schedule()

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

section("PAWPAL+  --  TODAY'S SCHEDULE")
print(f"\n  Owner : {owner.name}  ({owner.email})")
print(f"  Window: {owner.available_start} - {owner.available_end}  "
      f"({planner.available_minutes} min available)")
print(f"  Pets  : {', '.join(p.name for p in owner.get_pets())}")

section("SCHEDULE")
print_schedule(planner)

section("REASONING")
print(planner.explain_plan())

section("TASK SUMMARY BY PET")
for pet in owner.get_pets():
    total     = len(pet.get_tasks())
    scheduled = sum(1 for s in planner.schedule if s.pet_name == pet.name)
    pending   = len(pet.get_pending_tasks())
    print(f"\n  {pet.name} ({pet.breed})")
    print(f"    Total tasks   : {total}")
    print(f"    Scheduled today: {scheduled}")
    print(f"    Still pending : {pending}")
