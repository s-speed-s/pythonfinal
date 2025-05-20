from datetime import datetime, timedelta
import heapq
from collections import defaultdict

# graph from class
class GraphAL:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, data):
        if data not in self.graph:
            self.graph[data] = []

    def add_edge(self, vertex1, vertex2, weight = 1):
        if vertex1 in self.graph and vertex2 in self.graph:
            if all(neighbor != vertex2 for neighbor, _ in self.graph[vertex1]):
                self.graph[vertex1].append((vertex2, weight))
        else:
            print("One or both vertices do not exist in the graph")

    def display_graph(self):
        print("Graph:")
        for vertex in sorted(self.graph):
            neighbors = sorted(self.graph[vertex])
            print(f"{vertex} -> {neighbors}")

    #dijkstra algorithm from class
    def dijkstra(self, start):
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        pq = [(0, start)]
        #changed to set to be faster
        visited = set()

        while pq:
            current_dist, current_vertex = heapq.heappop(pq)

            if current_vertex in visited:
                continue
            visited.add(current_vertex)

            for neighbor, weight in self.graph[current_vertex]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances


# Linked List Implementation
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, task):
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.task)
            current = current.next
        return result

class Task:
    def __init__(self, name, deadline, workload, priority):
        self.name = name
        self.deadline = deadline
        self.workload = workload  # in minutes
        self.priority = priority
        #what task depends on
        self.dependencies = []

    def __lt__(self, other):
        return self.priority < other.priority  # used by heapq

    def __str__(self):
        return f"{self.name} | Priority: {self.priority}, Workload: {self.workload} mins, Deadline: {self.deadline}" # displays relevant task information

class TimeSlot:
    def __init__(self, start_time, task):
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=task.workload)
        self.task = task

    def overlaps(self, other):
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time) # checks if time slots overlap

class AvailabilitySlot:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def contains(self, time_slot):
        return self.start_time <= time_slot.start_time and time_slot.end_time <= self.end_time # checks if time slot is within given availability time ranges

# merge sort to sort tasks
def merge_sort(tasks, key=lambda x: x.deadline):
    if len(tasks) <= 1:
        return tasks
    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid], key)
    right = merge_sort(tasks[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) < key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

class Calendar:
    def __init__(self, availability_slots):
        self.schedule = defaultdict(list)  # calendar dictionary, key = day, value = list of TimeSlot
        self.availability = availability_slots

    def is_available(self, start_time, task): # checks if task can be scheduled at given start time using TimeSlot and AvailabilitySlot classes
        new_slot = TimeSlot(start_time, task)
        day_key = start_time.strftime('%Y-%m-%d')
        for slot in self.schedule[day_key]:
            if new_slot.overlaps(slot):
                return False
        return any(avail.contains(new_slot) for avail in self.availability)

    def find_next_available_time(self, task): # finds next available time slot for task
        for avail in self.availability:
            check_time = avail.start_time
            while check_time + timedelta(minutes=task.workload) <= avail.end_time:
                if self.is_available(check_time, task):
                    return check_time
                check_time += timedelta(minutes=5)
        return None

    def add_to_calendar(self, task): # adds task to calendar
        start_time = self.find_next_available_time(task)
        if start_time:
            slot = TimeSlot(start_time, task)
            day_key = start_time.strftime('%Y-%m-%d')
            self.schedule[day_key].append(slot)
            print(f"Scheduled '{task.name}' at {start_time.strftime('%Y-%m-%d %H:%M')}.")
        else:
            print(f"Couldn't schedule '{task.name}' — not enough time.")

    #task removal for when user is done with task
    def remove_task(self, task_name):
        found = False
        #go through calendar days and find task
        for day in list(self.schedule.keys()):
            new_day_schedule = []
            for slot in self.schedule[day]:
                if slot.task.name != task_name:
                    new_day_schedule.append(slot)
                else:
                    found = True
            self.schedule[day] = new_day_schedule
            if not self.schedule[day]:
                del self.schedule[day]  #remove empty days from calendar
        if found:
            print(f"Task '{task_name}' has been removed from the schedule.")
        else:
            print(f"No task named '{task_name}' found in the schedule.")

    def display(self): # displays calendar
        if not self.schedule:
            print("Calendar is empty.")
            return
        for day in sorted(self.schedule.keys()):
            print(f"\n{day}:")
            for slot in sorted(self.schedule[day], key=lambda s: s.start_time):
                print(f"  {slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')} | {slot.task.name} (Priority {slot.task.priority})")

    def sort_scheduled_tasks(self, sort_by): # sorts tasks in calendar by given criteria
        key_funcs = {
            "priority": lambda s: s.task.priority,
            "workload": lambda s: s.task.workload,
            "deadline": lambda s: s.task.deadline
        }
        if sort_by in key_funcs:
            for day in self.schedule:
                self.schedule[day] = merge_sort(self.schedule[day], key=key_funcs[sort_by])
            print(f"\nTasks sorted by {sort_by.capitalize()}:")
            self.display()
        else:
            print("Invalid sort option.")

class TaskScheduler:
    def __init__(self):
        self.tasks = []  # min heap for priority queue

    def add_task(self, task): # adds task to priority queue based of priority value
        heapq.heappush(self.tasks, task)

    def schedule_all(self, calendar): # schedules all tasks in priority queue
        while self.tasks:
            task = heapq.heappop(self.tasks)
            calendar.add_to_calendar(task)

# UI functions
def get_task_from_user(task_names):  # pass existing task names
    name = input("Task name (or type 'done' to finish): ").strip()
    if name.lower() == "done":
        return None
    try:
        priority = int(input("Priority (1-5): ").strip())
        workload = int(input("Workload in minutes: ").strip())
        deadline_str = input("Deadline (YYYY-MM-DD HH:MM): ").strip()
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

        dependencies = []
        if task_names:
            print("Enter dependencies (comma-separated task names), or press Enter if none:")
            depend_input = input("Depends on: ").strip()
            if depend_input:
                dependencies = [dep.strip() for dep in depend_input.split(",") if dep.strip() in task_names]

        task = Task(name, deadline, workload, priority)
        task.dependencies = dependencies
        return task
    except Exception as e:
        print(f"Invalid input: {e}")
        return get_task_from_user(task_names)

def get_availability_ranges(): # gets availability time ranges from user and creates AvailabilitySlot objects based on input
    slots = []
    print("\nEnter availability time ranges (or type 'done' to finish).")
    while True:
        start = input("Start time (YYYY-MM-DD HH:MM): ").strip()
        if start.lower() == "done":
            break
        end = input("End time (YYYY-MM-DD HH:MM): ").strip()
        try:
            start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
            if end_dt > start_dt:
                slots.append(AvailabilitySlot(start_dt, end_dt))
            else:
                print("End must be after start.")
        except:
            print("Invalid format.")
    return slots

def build_task_graph(tasks):
    #create graph using graph class
    graph = GraphAL()
    #create dictionary to map task names to tasks
    task_dict = {task.name: task for task in tasks}

    # loop through tasks and add vertices and edges to graph
    for task in tasks:
        graph.add_vertex(task.name)
    for task in tasks:
        for dep in task.dependencies:
            weight = task_dict[task.name].workload
            graph.add_edge(dep, task.name, weight)  # task depends on dependency
    return graph, task_dict

#topological sort for task scheduling
def topological_sort(graph):
    #create visited set and stack
    visited = set()
    stack = []

    #depth first search function to visit vertices and add to stack
    def dfs(vertex):
        #mark vertex as visited
        visited.add(vertex)
        #loop through neighbors of vertex
        for neighbor, _ in graph.graph.get(vertex, []):
            #recursively call dfs on unvisited neighbors
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)

    #loop through vertices in graph and call dfs on unvisited vertices
    for vertex in graph.graph:
        if vertex not in visited:
            dfs(vertex)

    return stack[::-1]  # reverse to get correct order

# Main
def main():
    print("Welcome to the Task Scheduler!\n")

    availability = get_availability_ranges()
    if not availability:
        print("No availability given. Exiting.")
        return

    calendar = Calendar(availability)
    scheduler = TaskScheduler()

    task_list = []
    task_names = set()

    print("\nEnter your tasks (enter task that has other tasks depending on it first):")
    while True:
        task = get_task_from_user(task_names)
        if task is None:
            break
        task_list.append(task)
        task_names.add(task.name)
        print(f"Task added: {task}\n")

    #build and display dependency graph
    print("\nTask Dependency Graph:")
    graph, task_dict = build_task_graph(task_list)
    graph.display_graph()

    #topological sort tasks to respect dependencies
    sorted_task_names = topological_sort(graph)
    print("\nYou should do the assignments in this order:", " -> ".join(sorted_task_names))

    #add tasks to scheduler in topological order
    print("\nScheduling tasks based on dependencies...\n")
    #loop through sorted tasks and add to scheduler
    for name in sorted_task_names:
        scheduler.add_task(task_dict[name])
    scheduler.schedule_all(calendar)

    print("\nSort scheduled tasks?")
    print("1. By Priority")
    print("2. By Workload")
    print("3. By Deadline")
    print("4. No sorting")

    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        calendar.sort_scheduled_tasks("priority")
    elif choice == "2":
        calendar.sort_scheduled_tasks("workload")
    elif choice == "3":
        calendar.sort_scheduled_tasks("deadline")
    else:
        print("No additional sorting applied.")

    #use dijkstra algorithm to find shortest path in terms of time from a selected task
    start_task = input("\nEnter a starting task to analyze shortest paths: ").strip()
    if start_task in graph.graph:
        distances = graph.dijkstra(start_task)
        print(f"\nSmallest workload from '{start_task}' to other tasks:")
        for task, dist in distances.items():
            print(f"  {task}: {dist}")
    else:
        print("Invalid task name for Dijkstra analysis.")

    #remove tasks from calendar when user says that they finished them
    while True:
        done_input = input("Enter task name to remove when done or type 'no' to finish: ").strip()
        if done_input.lower() == "no":
            break
        calendar.remove_task(done_input)
        calendar.display()

if __name__ == "__main__":
    main()
# https://support.google.com/calendar/answer/37118?hl=en&co=GENIE.Platform%3DDesktop
'''
to-do:
add checks for dependency cycles and invalid inputs
add functionality to automatically remove tasks once due date has passed
'''
