from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
DB_CONNECTION_STRING = os.environ.get(
    "DB_URI", "postgresql://postgres:grunger@localhost:5432/postgres")


app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    assign = db.Column(db.String(255))

    def __init__(self, title, assign, _id=None):
        self.title = title
        self.assign = assign
        if _id:
            self.id = _id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "assign": self.assign
        }


@app.route("/", methods=["GET"])
def hello_world():
    return {'message': 'Hello World!'}, 200


@app.route("/tasks", methods=["GET"])
def get_task():
    args = request.args
    task_title = args.get("title", "")
    task_assign = args.get("assign", "")

    tasks = Task.query.filter(Task.title.contains(task_title)).filter(
        Task.assign.contains(task_assign)).order_by(Task.id).all()

    if not tasks:
        return {"message": "Tasks not fount"}, 404

    tasks = [task.to_dict() for task in tasks]

    return {"tasks": tasks}, 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": "Task not found"}, 404
    return task.to_dict()


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    new_task = Task(data.get('title'), data.get('assign'))
    db.session.add(new_task)
    db.session.commit()
    return {'message': 'Object created successesfully'}, 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {'message': 'Object deleted successesfully'}, 200


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_by_id(task_id):

    task = Task.query.get(task_id)
    if not task:
        return {"message": "Task not found"}, 404

    data = request.json
    task.title = data.get('title', "")
    task.assign = data.get('assign', "")

    db.session.add(task)
    db.session.commit()

    return {'message': 'Object updated successesfully'}, 200


@app.route("/upload", methods=["POST"])
def upload_files():
    f = request.files['image']
    f.save('./uploads/' + secure_filename(f.filename))
    f = request.files['text_file']
    f.save('./uploads/' + secure_filename(f.filename))

    return {'message': 'Files saved.'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
