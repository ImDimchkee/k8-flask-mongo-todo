from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl
from werkzeug.utils import redirect
from flask import render_template, flash, request, url_for
from flaskr import app, db
from .form import ToDo
from datetime import datetime
from bson import ObjectId


@app.route("/")
def get_todo():
    todos = []
    for todo in db.todo.find().sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)
    return render_template("view_todos.html", title="Layout page", todos=todos)

@app.route("/add_todo", methods=["GET", "POST", "DELETE"])
def add_todo():
    if request.method == "POST":
        form = ToDo(request.form)   
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data
        
        db.todo.insert_one({
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.now()
        })
        flash("Todo successfully added", "success")

        return redirect("/")
    else:

        form = ToDo()
        return render_template("add_todo.html", form=form)

@app.route("/update_todo/<id>", methods=["GET", "POST"])
def update_todo(id):
    pass
    if request.method == "POST":
        form = ToDo(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo.find_one_and_update({"_id": ObjectId(id)}, {"$set":{
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.now()
        }})
        flash("Todo successfully updated")
        return redirect("/")
    else:
        form = ToDo()

        todo = db.todo.find_one_or_404({"_id": ObjectId(id)})
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)

    return render_template("add_todo.html", form=form)

@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todo.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo deleted", "success")
    return redirect("/")