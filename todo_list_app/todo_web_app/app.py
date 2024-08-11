from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Path to the local file
TODO_FILE = "todo_list.json"

# Load tasks from the file
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks to the file
def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("search", "")
    todo_list = load_tasks()

    if search_query:
        filtered_tasks = [task for task in todo_list if search_query.lower() in task["task"].lower()]
    else:
        filtered_tasks = todo_list

    return render_template("index.html", tasks=filtered_tasks, search_query=search_query)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    due_date = request.form["due_date"]
    priority = request.form["priority"]
    todo_list = load_tasks()
    todo_list.append({"task": task, "completed": False, "due_date": due_date, "priority": priority})
    save_tasks(todo_list)
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    todo_list = load_tasks()
    todo_list[task_id]["completed"] = True
    save_tasks(todo_list)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    todo_list = load_tasks()
    if request.method == "POST":
        todo_list[task_id]["task"] = request.form["task"]
        todo_list[task_id]["due_date"] = request.form["due_date"]
        todo_list[task_id]["priority"] = request.form["priority"]
        save_tasks(todo_list)
        return redirect(url_for("index"))
    task = todo_list[task_id]
    return render_template("edit_task.html", task=task, task_id=task_id)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    todo_list = load_tasks()
    todo_list.pop(task_id)
    save_tasks(todo_list)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
