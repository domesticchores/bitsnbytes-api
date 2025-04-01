from flask import Flask, request, abort
import os
import logging
import json
import api.util
import api.s3
from functools import wraps
from api.models.item import Item
from api.models.user import User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.orm import Session
import json
#from flasgger import Swagger

#swagger = Swagger(app)

app = Flask(__name__)
    
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    app.config["DBUSER"],
    app.config["DBPWD"],
    app.config["DBHOST"],
    app.config["DBPORT"],
    app.config["DBNAME"],
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# Commit
#commit = check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').rstrip()

########################
#
# Helpers
#
########################

"""
Handle errors
"""
@app.errorhandler(404)
def page_not_found(e):
    resp = e.get_response()
    resp.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description
    })
    resp.content_type = 'application/json'
    return resp

"""
Auth required wrapper
"""
def auth(f):
    @wraps(f)
    def wrapped(**kwargs):
        if "Authorization" in request.headers:
            if request.headers["Authorization"] == f'{app.config["UI_KEY"]}':
                print("Authorized with UI credential")
                return f(**kwargs)
            if request.headers["Authorization"] == f'{app.config["AI_KEY"]}':
                print("Authorized with AI credential")
                return f(**kwargs)
            if request.headers["Authorization"] == f'{app.config["WEB_KEY"]}':
                print("Authorized with WEB credential")
                return f(**kwargs)
            if request.headers["Authorization"] == f'{app.config["EXTRA_KEY"]}':
                print("Authorized with EXTRA credential")
                return f(**kwargs)
        return abort(403)
    return wrapped

########################
# 
# Routes
# 
########################

# Items
########################

"""
Get all items
"""
@app.route('/items', methods=["GET", "POST"])
@auth
def get_all_items():
    """
    Returns all items as a json obj
    """
    
    if request.method == "GET":
        query = db.session.query(Item)
        items = query.all()

        return [item.as_dict() for item in items]
    
    else:
        try:
            new_item = Item(request.get_json())
            db.session.add(new_item)
            db.session.commit()
            return str(new_item.id)
        except ValueError as value_err:
            return str(value_err), 400

"""
Get Item by ID
"""
@app.route('/items/<id>', methods=["GET", "PUT"])
@auth
def get_item_by_id(id):
    """
    Returns Item Object by ID
    ```
    parameters:
    - name: id
        in: path
        type: int
        required: true
    ```"""

    item = db.get_or_404(Item, id)

    if request.method == "PUT":    
        for field, value in request.form_data.items():
            if hasattr(item, field) and getattr(item, field) != value:
                setattr(item, field, value)
        db.session.commit()
    else:
        return json.dumps(item.as_dict())
    
"""
Deletes item object with given ID
"""
@app.route('/items/<id>', methods=["DELETE"])
@auth
def delete_item(id):
    item = db.get_or_404(Item, id)
    db.session.delete(item)
    db.session.commit()

    return ""

# Users
########################

"""
Get all users
"""
@app.route('/users/', methods=["GET", "POST"])
@auth
def get_all_users():
    """
    Returns all users as a json obj
    """
    
    if request.method == "GET":
        print("GET not POST")
        query = db.session.query(User)
        users = query.all()

        return [user.as_dict() for user in users]
    
    else:
        print("POST not GET")
        try:
            user_data = request.args.to_dict()
            new_user = User(user_data)
            print(f"INPUTTED DATA: {user_data}")
            db.session.add(new_user)
            db.session.commit()
            print(f"POST SUCCESS: {new_user.id}")
            return str(new_user.id)
        except ValueError as value_err:
            print(f"VALUE ERROR: {value_err}")
            return str(value_err), 400

"""
Get User by Token
"""
@app.route('/token/<token>', methods=["GET"])
@auth
def get_user_by_token(token):
    query = db.session.query(User).filter(User.token == token)
    if query.count() == 0:
        abort(404)

    user = query.one()

    return json.dumps(user.as_dict())

"""
Get User by ID
"""
@app.route('/users/<int:id>', methods=["GET", "PUT"])
@auth
def get_user_by_id(id):
    """
    Returns User Object by ID
    ```
    parameters:
    - name: id
        in: path
        type: int
        required: true
    ```"""

    user = db.get_or_404(User, id)

    if request.method == "PUT":    
        for field, value in request.form_data.users():
            if hasattr(user, field) and getattr(user, field) != value:
                setattr(user, field, value)
        db.session.commit()
    else:
        return json.dumps(user.as_dict())
    
"""
Deletes user object with given ID
"""
@app.route('/users/<id>', methods=["DELETE"])
@auth
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()

    return ""