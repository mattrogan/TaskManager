import sqlite3
from flask import Flask, render_template, url_for, request, redirect

#region Setup

app = Flask(__name__)

with sqlite3.connect("tasks.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       description TEXT,
                       due_date DATE,
                       complete BOOLEAN DEFAULT FALSE)''')
    cursor.close()
    
#endregion

@app.route("/")
def hello() -> str:
    return render_template("index.html")


@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        complete = 0  # default value for complete is False (0)
        
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, due_date, complete) VALUES (?, ?, ?, ?)",
                  (title, description, due_date, complete))
        conn.commit()
        conn.close()
        
        return redirect(url_for("view_tasks"))
    
    return render_template("add-task.html")



@app.route("/view-tasks", methods=["GET"])
def view_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()
    
    if not tasks:
        return render_template("view-tasks.html", tasks=[], noTasks=True)
    else:
        return render_template("view-tasks.html", tasks=tasks, noTasks=False)

@app.route("/view-tasks/<int:id>")
def view_task(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    # Code to get the task with the given id
    task = cursor.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchone()
    
    if not task:
        return render_template("view-task.html", task=None, noTask=True)
    else:
        return render_template("view-task.html", task=task, noTask=False)


if __name__ == "__main__":
    app.run(debug=True)