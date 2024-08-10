import tkinter as tk
from tkinter import messagebox
import json

# File to store tasks
TASKS_FILE = "tasks.json"

# Global variable to hold tasks
todo_list = []

def load_tasks():
    """Load tasks from a JSON file."""
    global todo_list
    try:
        with open(TASKS_FILE, "r") as file:
            todo_list = json.load(file)
    except FileNotFoundError:
        todo_list = []

def save_tasks():
    """Save tasks to a JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(todo_list, file)

def update_listbox():
    """Update the listbox with the current tasks."""
    listbox_tasks.delete(0, tk.END)
    for task in todo_list:
        status = "Done" if task["completed"] else "Pending"
        listbox_tasks.insert(tk.END, f"{task['task']} [{status}]")

def add_task():
    """Add a new task to the todo list."""
    task = entry_task.get()
    if task:
        todo_list.append({"task": task, "completed": False})
        save_tasks()
        update_listbox()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    """Delete the selected task."""
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        del todo_list[selected_task_index]
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

def mark_task_complete():
    """Mark the selected task as complete."""
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        todo_list[selected_task_index]["completed"] = True
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

# Load tasks when the application starts
load_tasks()

# Initialize the main application window
app = tk.Tk()
app.title("Todo List")

# Frame to hold the listbox and scrollbar
frame_tasks = tk.Frame(app)
frame_tasks.pack()

# Listbox to display tasks
listbox_tasks = tk.Listbox(frame_tasks, height=10, width=50)
listbox_tasks.pack(side=tk.LEFT)

# Scrollbar for the listbox
scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the scrollbar to work with the listbox
listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_tasks.yview)

# Update the listbox with tasks from the JSON file
update_listbox()

# Entry widget for adding new tasks
entry_task = tk.Entry(app, width=50)
entry_task.pack()

# Buttons to add, delete, and mark tasks as complete
button_add_task = tk.Button(app, text="Add task", width=48, command=add_task)
button_add_task.pack()

button_delete_task = tk.Button(app, text="Delete task", width=48, command=delete_task)
button_delete_task.pack()

button_mark_complete = tk.Button(app, text="Mark task complete", width=48, command=mark_task_complete)
button_mark_complete.pack()

# Run the application
app.mainloop()
