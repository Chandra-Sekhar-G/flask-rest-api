from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("name", type=str, help="name is required", required=True)
task_post_args.add_argument("email", type=str, help="email is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("name", type=str)
task_put_args.add_argument("email", type=str)


resource_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String
}

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))

# db.create_all()


        
class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Could not find name with that id")
        return task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        task = TodoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, message="name id taken..")
        todo = TodoModel(id=todo_id, name=args["name"], email=args["email"])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="name doesn't exsist, cannot update")
        if args["name"]:
            task.name = args["name"]
        if args["email"]:
            task.email = args["email"]
        db.session.commit()
        return task

    def delete(self, todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return "Todo Deleted", 204

class TodoList(Resource):
    def get(self):
        tasks = TodoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"name": task.name, "email":task.email}
        return todos


api.add_resource(TodoList,"/todolist")
api.add_resource(Todo,"/todo/<int:todo_id>")

if __name__ == "__main__":
    app.run(debug=True)