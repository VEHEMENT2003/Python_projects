import sys
import json

todo_list = []

def show_menu():
    print("\nTodo List Application")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Complete")
    print("4. Exit")

def add_task():
    task = input("Enter the task: ")
    todo_list.append({"task": task, "completed": False})
    save_tasks()
    print(f"Task '{task}' added.")

def view_tasks():
    if not todo_list:
        print("No tasks to show.")
        return
    for idx, task in enumerate(todo_list, 1):
        status = "Done" if task["completed"] else "Pending"
        print(f"{idx}. {task['task']} [{status}]")

def mark_task_complete():
    view_tasks()
    try:
        task_num = int(input("Enter the task number to mark as complete: "))
        if 0 < task_num <= len(todo_list):
            todo_list[task_num - 1]["completed"] = True
            save_tasks()
            print(f"Task {task_num} marked as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(todo_list, file)

def load_tasks():
    global todo_list
    try:
        with open("tasks.json", "r") as file:
            todo_list = json.load(file)
    except FileNotFoundError:
        todo_list = []

load_tasks()

while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        mark_task_complete()
    elif choice == "4":
        print("Exiting...")
        sys.exit()
    else:
        print("Invalid choice! Please select a valid option.")
