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

    Yes, I asked AI agent to review my design and check if there are any flaws. One of the flaws that it identified is that Owner and pet relationship is not enforced. Owner has a list of all the pets it owns but pet doesn't have what its owner is so If we ever need "which owner does this pet belong to?", we would have to search all owners. I missed this logic initially as I was thinking of one way relation where owners have multiple pets but not considering the pet so I updated the design to include pet owner attribute in pet class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

It considered time, priority, contraints like when they are available to do pet tasks. The agent decided that availablity is the what mattered most because it would not schedule tasks that are outside of the owners availability even if the task has no time conflict with another task. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

I asked AI agent to simplify the algorithm for Detecting task conflicts and one of the tradeoffs that I saw is that the simplified version doesn't check for overlaps between tasks that are non adjacent. For example, Task A start from 1-3, task B starts from 2-2:30 and task C starts from 2:30 to 4. In this case, Task A and Task B has scehduling conflicts but it doesn't show that task A and Task C have conflicts because they are sorted using task start time and Task A and C are not next to each other in the list.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI from end-to-end this project. I gave the prompt first and brainstormed the ideas and how it can be implemented and it designed the UML diagram for me given my requirements. It also implemented the code and logic when I gave it a requirement and also created the test cases needed for each scenario. 

I think that being specific in the prompts was the most helpful. Rather than saying "create a algorithm to solve schedule conflicts", I gave it prompts such as "Create an algorithm that will solve time conflicts between tasks but checking the start time, endtime and the duration of the task. If tasks are conflicted, notify user with a warning message and don't add that task to the schedule". If the prompt is too broad, agent will create logic that it may think is the best but may not align with the project goals we have. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I asked the agent to summarize the code for each promot that I gave and I noticed that it didn't correctly think of sorting correctly (it was only sorting by priority and not time) so I had to reprompt that correctly and it suggested the right changes.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested using the UI mainly because thats what the end users experience. I tested adding multiple pets for an owner and adding multiple tasks for each pet with conflicted schedules, various priorities, and ownder available time. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident that the scheduler works after I have tested the application. The agent covered the main test cases that I have also thought of but we might have missed edge cases so I am confident 4/5. 

Some of the edge cases I would test next time is duplicate items like duplicate pets, duplicate tasks and see how we can resolve that. Another test case is how to handle tasks that are outside of owners available time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I liked that I was able to guide the agent to generate code exactly how I want it and I wasn't confused anywhere when it created the code because my prompts were specific. This also showed me how fast I can build an application if the system design and planning stage is done right because there would be less bugs to fix later. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I think I would improve my initial design and plan with the AI more on how to implement all of the extra methods in the other phases at once in the beginning rather than one by one so that the agent knows all of its requirements from the beginning and implement based on that. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

In the last project, we were fixing bugs for a given project and although it was useful, I didn't see why Claude Agent is powerful because I am used to fixing bugs for projects using AI generic chats. But this project allowed me to use AI agent to full implment the application from end to end based on the requirements that I gave and it showed me how powerful it is to work with the agent but also to be careful when prompting. Although AI is taking the code, I still needed to be the leader and plan the basic system design so that it creates an application thats clean and scalable. 
