# Import the necessary modules
from init import db, ma
from marshmallow import fields

# Define a User Model
class User(db.Model):
    __tablename__ = 'users'

    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Define relationships with other models
    gyms = db.relationship('Gym', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')

# Define a schema for the User Model
class UserSchema(ma.Schema):
    # Define nested fields for related models
    gyms = fields.List(fields.Nested('GymSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))
    # Define the fields to include in schema
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'gyms', 'comments')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
