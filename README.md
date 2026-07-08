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
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
