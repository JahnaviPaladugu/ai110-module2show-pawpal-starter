import json
import os
import streamlit as st
import pawpal_system as ps

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

SAVE_FILE = "pawpal_data.json"

# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def _save(owner: ps.Owner) -> None:
    """Serialise the owner and all pets/tasks to a JSON file."""
    data = {
        "owner": {
            "name":            owner.name,
            "email":           owner.email,
            "available_start": owner.available_start,
            "available_end":   owner.available_end,
        },
        "pets": [
            {
                "name":      pet.name,
                "species":   pet.species,
                "breed":     pet.breed,
                "age_years": pet.age_years,
                "tasks":     [t.to_dict() for t in pet.get_tasks()],
            }
            for pet in owner.get_pets()
        ],
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _load() -> "ps.Owner | None":
    """Rebuild an Owner (with pets and tasks) from the JSON file, or return None."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE) as f:
        data = json.load(f)
    owner = ps.Owner(**data["owner"])
    for pet_data in data["pets"]:
        tasks = pet_data.pop("tasks", [])
        pet = ps.Pet(**pet_data)
        for task_dict in tasks:
            pet.add_task(ps.Task(**task_dict))
        owner.add_pet(pet)
    return owner


# ---------------------------------------------------------------------------
# Session-state vault — initialise once, survive every rerun
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = _load()      # restore from file, or None if first run

if "schedule" not in st.session_state:
    st.session_state.schedule = []         # list[ScheduledSlot]

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("🐾 PawPal+")
st.caption("A daily pet-care planner for busy owners.")
st.divider()

# ===========================================================================
# SECTION 1 — Owner info
# ===========================================================================
st.subheader("1. Owner Info")

with st.form("owner_form"):
    col1, col2 = st.columns(2)
    with col1:
        owner_name  = st.text_input("Your name",  placeholder="Alex Rivera")
        owner_email = st.text_input("Email",       placeholder="alex@example.com")
    with col2:
        avail_start = st.text_input("Available from (HH:MM)", value="17:00")
        avail_end   = st.text_input("Available until (HH:MM)", value="21:00")

    save_owner = st.form_submit_button("Save owner")

if save_owner:
    if not owner_name.strip():
        st.error("Please enter your name before saving.")
    else:
        # Preserve existing pets if owner already existed
        existing_pets = st.session_state.owner.get_pets() if st.session_state.owner else []
        st.session_state.owner = ps.Owner(
            name=owner_name.strip(),
            email=owner_email.strip(),
            available_start=avail_start.strip(),
            available_end=avail_end.strip(),
        )
        for pet in existing_pets:
            st.session_state.owner.add_pet(pet)
        _save(st.session_state.owner)
        st.success(f"Owner saved: {owner_name}  |  window {avail_start} - {avail_end}")

owner: ps.Owner | None = st.session_state.owner

# ===========================================================================
# SECTION 2 — Add a Pet
# ===========================================================================
st.divider()
st.subheader("2. Add a Pet")

if owner is None:
    st.info("Save owner info above before adding pets.")
else:
    with st.form("pet_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pet_name    = st.text_input("Pet name",  placeholder="Biscuit")
        with col2:
            pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
        with col3:
            pet_breed   = st.text_input("Breed",     placeholder="Golden Retriever")
        with col4:
            pet_age     = st.number_input("Age (years)", min_value=0, max_value=30, value=2)

        add_pet = st.form_submit_button("Add pet")

    if add_pet:
        if not pet_name.strip():
            st.error("Pet name cannot be empty.")
        elif any(p.name == pet_name.strip() for p in owner.get_pets()):
            st.warning(f"{pet_name} is already in the list.")
        else:
            new_pet = ps.Pet(
                name=pet_name.strip(),
                species=pet_species,
                breed=pet_breed.strip() or pet_species,
                age_years=int(pet_age),
            )
            owner.add_pet(new_pet)          # sets new_pet.owner = owner
            _save(owner)
            st.success(f"Added {new_pet.name} ({new_pet.breed}).")

    # Show existing pets
    if owner.get_pets():
        st.write("**Your pets:**")
        for pet in owner.get_pets():
            pending = len(pet.get_pending_tasks())
            st.markdown(
                f"- **{pet.name}** — {pet.breed}, {pet.age_years} yr  "
                f"({pending} pending task{'s' if pending != 1 else ''})"
            )

# ===========================================================================
# SECTION 3 — Add a Task
# ===========================================================================
st.divider()
st.subheader("3. Add a Task")

if owner is None or not owner.get_pets():
    st.info("Add at least one pet above before adding tasks.")
else:
    pet_names = [p.name for p in owner.get_pets()]

    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            target_pet    = st.selectbox("Assign to pet", pet_names)
            task_name     = st.text_input("Task name", placeholder="Evening Walk")
            task_category = st.selectbox("Category", ["walk", "feed", "meds", "groom", "enrichment"])
        with col2:
            task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            task_priority = st.selectbox("Priority", ["high", "medium", "low"])
            task_time     = st.selectbox("Preferred time", ["morning", "afternoon", "evening", "any"])
            task_recurring = st.checkbox("Recurring daily?")

        add_task = st.form_submit_button("Add task")

    if add_task:
        if not task_name.strip():
            st.error("Task name cannot be empty.")
        else:
            pet_obj = next(p for p in owner.get_pets() if p.name == target_pet)
            new_task = ps.Task(
                name=task_name.strip(),
                category=task_category,
                duration_min=int(task_duration),
                priority=task_priority,
                preferred_time=task_time,
                is_recurring=task_recurring,
            )
            pet_obj.add_task(new_task)
            _save(owner)
            st.success(f"Added '{new_task.name}' to {pet_obj.name}.")

    # Show all tasks per pet
    for pet in owner.get_pets():
        tasks = pet.get_tasks()
        if tasks:
            with st.expander(f"{pet.name}'s tasks ({len(tasks)} total)"):
                for t in tasks:
                    status = "✅" if t.is_completed else "⬜"
                    st.markdown(
                        f"{status} **{t.name}** — {t.category}, "
                        f"{t.duration_min} min, priority: {t.priority}, "
                        f"preferred: {t.preferred_time}"
                    )

# ===========================================================================
# SECTION 4 — Generate Schedule
# ===========================================================================
st.divider()
st.subheader("4. Generate Today's Schedule")

if owner is None or not owner.get_pets():
    st.info("Add an owner and at least one pet with tasks to generate a schedule.")
else:
    target_options = ["All pets"] + [p.name for p in owner.get_pets()]
    schedule_target = st.selectbox("Schedule for", target_options)

    if st.button("Generate schedule", type="primary"):
        selected_pet = None
        if schedule_target != "All pets":
            selected_pet = next(p for p in owner.get_pets() if p.name == schedule_target)

        planner = ps.DailyPlanner(owner=owner, pet=selected_pet)
        st.session_state.schedule = planner.generate_schedule()
        st.session_state.planner  = planner

    if st.session_state.schedule:
        planner = st.session_state.planner
        slots   = st.session_state.schedule

        st.success(
            f"Scheduled {len(slots)} task(s) — "
            f"{sum(s.task.duration_min for s in slots)} min used of "
            f"{planner.available_minutes} min available."
        )

        # Schedule table
        st.markdown("#### Schedule")
        rows = [
            {
                "Time":     s.start_time,
                "Task":     s.task.name,
                "Pet":      s.pet_name,
                "Category": s.task.category,
                "Duration": f"{s.task.duration_min} min",
                "Priority": s.task.priority,
            }
            for s in slots
        ]
        st.table(rows)

        # Reasoning
        with st.expander("Why was this plan chosen?"):
            st.text(planner.explain_plan())

        # Mark tasks done
        st.markdown("#### Mark tasks as done")
        for slot in slots:
            label = f"{slot.start_time}  {slot.task.name} ({slot.pet_name})"
            if st.checkbox(label, value=slot.task.is_completed, key=f"done_{slot.task.name}_{slot.pet_name}"):
                slot.task.mark_done()
            else:
                slot.task.reset()
