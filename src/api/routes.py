"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Todo
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/todos', methods=['GET'])
def get_all_todos():
  
    response_body = {
        "message": "List of all active Toddos:"
    }

    todos = Todo.query.all()
    todos_serialzied =  [todo.serialize() for todo in todos]
    return jsonify({"todos": todos_serialzied}), 200

@api.route('/todos', methods=['POST'])
def create_todo():
  
    body= request.json
    new_todo = Todo(label=body["label"] , done=body["done"])
    db.session.add(new_todo)
    db.session.commit()

    todos = Todo.query.all()
    todos_serialzied =  [todo.serialize() for todo in todos]
    return jsonify({"todos": todos_serialzied}), 200


@api.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
  
    todo_to_delete = Todo.query.offset(position - 1).limit(1).first()
    if not todo_to_delete:
        return ({"error": "No record exists at that position"}), 400

    db.session.delete(todo_to_delete)
    db.session.commit()

    todos = Todo.query.all()
    todos_serialzied =  [todo.serialize() for todo in todos]
    return jsonify({"todos": todos_serialzied}), 200