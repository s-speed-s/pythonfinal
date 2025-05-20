# python-midterm
# Task Scheduler

This is a console-based Task Scheduler built in Python that allows users to manage their tasks efficiently based on priority, deadlines, and availability. It automatically schedules tasks into available time slots and lets users view and sort their scheduled tasks.

---

## Features

- Add tasks with:
  - Priority (1-5, higher number means lower priority)
  - Workload (in minutes)
  - Deadline (`YYYY-MM-DD HH:MM`, 24 hour format)
  - Optional dependencies (ex. folding clothes requires washing them first)
- Remove tasks once done
- Input custom availability time ranges
- Automatically schedules tasks to avoid conflicts
- Sort scheduled tasks by:
  - Priority
  - Workload
  - Deadline
- Create graphs for tasks through adjacency mapping
- Provide most time efficient order to do tasks if there is not sufficient time to do all of them
- Console-based user interface

---

When ran, the program will prompt the user for information relevant to creating the schedule. Follow the directions in the console to create your schedule.
