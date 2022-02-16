from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, jsonify, request

DATABASE_URI = 'sqlite:///todo.db'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    details = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Task("{self.title}", "{self.created_at}")'


db.create_all()


@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        all_tasks = Todo.query.all()
        result = []
        for task in all_tasks:
            dict={}
            dict['id'] = task.id
            dict['title'] = task.title
            dict['details'] = task.details
            dict['created_at'] = task.created_at

            result.append(dict)

        return jsonify({
            "status": "success",
            "data": result
        })

    if request.method == 'POST':
        title = request.json.get('title')
        details = request.json.get('details')
        created_at = request.json.get('created_at')

        newTask = Todo(title=title, details=details, created_at=created_at)
        db.session.add(newTask)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": f"task {title} added successfully"
        })


@app.route('/task/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def mod_task(id):
    task = Todo.query.filter_by(id=id).first()
    if request.method == 'GET':
        dict = {}
        dict['id'] = task.id
        dict['title'] = task.title
        dict['details'] = task.details
        dict['created_at'] = task.created_at

        return jsonify({
            "data": dict
        })

    if request.method == 'PUT':
        task.title = request.json.get('title')
        task.details = request.json.get('details')
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": "Task updated successfully"
        })

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": "Task deleted successfully"
        })


@app.route('/')
def home():
    return "<h1> Welcome in Home Page </h1>"


db.create_all()
app.run(debug=True)
