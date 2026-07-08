# PawPal+ Project Reflection

## 1. System Design

3 Core Actions: 
1. User should be able to enter pet info 
2. User should be able to add tasks and their contraints
3. User should be able to schedule the task for a certain time in the day.

**a. Initial design**

- Briefly describe your initial UML design.
     An owner can have 1 or more pets
     A pet has multiple tasks
     
- What classes did you include, and what responsibilities did you assign to each?
1. Owner: Has owners information and contraints (ex, available time for pet care only after 5pm). Owners may have more than 1 pet.
2. Pet: Stores pet infromation (breed, age, name), list of Tasks for this pet
3. Task: Stored the pet activity type and Needs to have different attributes such as priority, duration, preferred time, etc
4. DailyPlanner: Stores the daily plan and sorts the tasks by requirements and generates a daily schedule. Also should explain the reasoning behind the task selection.

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
