# Author: Mike Bett
# Date: 28/11/2024
# Objective: SQLAlchemy ORM and Marshmallow Serialisation for REST API

# import Flask class definition from library
from flask import Flask, request, jsonify
import json

# SQLAlchemy is an Object Relational Mapper allowing decoupling of db operations
from flask_sqlalchemy import SQLAlchemy

# Marshmallow is an object serialization/deserialization library
from flask_marshmallow import Marshmallow

# instantiate app based of Flask class
app = Flask(__name__)
#------------------------------------------------------------------------------
# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # path to db
app.config['SQLALCHEMY_ECHO'] = True # echoes SQL for debug
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#------------------------------------------------------------------------------
# instantiate db obj using the SQLAlchemy class with the Flask app obj as arg
db = SQLAlchemy(app)
#------------------------------------------------------------------------------
# Marshmallow must be initialised after SQLAlchemy
ma = Marshmallow(app)
#------------------------------------------------------------------------------
# class def for SQLAlchemy ORM
class User(db.Model):
 """Definition of the User Model used by SQLAlchemy"""
 user_id = db.Column(db.String(80), primary_key=True)
 user_forename = db.Column(db.String(80), nullable=False)
 user_surname = db.Column(db.String(80), nullable=False)
 user_email = db.Column(db.String(80), nullable=False)
 def __repr__(self):
    return  '<User %r>' % self.user_id

#------------------------------------------------------------------------------
# class def for Marshmallow serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
 """Definition used by serialization library based on User Model"""
 class Meta:
  fields = ("user_id","user_forename","user_surname", "user_email")
# instantiate objs based on Marshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# decorator used to trigger function based on HTTP GET method sent to app
@app.get("/")
def hello_world():
 return "Hello World"

@app.post("/users/add-users-json")
def users_add_json():
 """endpoint uses json to add user details to db"""
 json_data = request.get_json() # req.get_json() used to access json sent
 print(json_data) # used for debugging purposes
 new_user = User (
 user_id = json_data['user_id'],
 user_forename = json_data['user_forename'],
 user_surname = json_data['user_surname'],
 user_email = json_data['user_email']
 )
 db.session.add(new_user)
 db.session.commit()
 print ("Record added:")
 print (json.dumps(json_data, indent=4)) # used for debugging purposes
 return user_schema.jsonify(new_user)

@app.get('/users/get-all-users')
def get_all_users():
 """endpoint used to view all users from db"""
 users = User.query.all()
 return users_schema.jsonify(users)