# Import the necessary modules
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

# Define a Gym Model
class Gym(db.Model):
    __tablename__= "gyms"

    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    style = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    title = db.Column(db.String(100))

    # Define a relationship with the User Model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='gyms')

    # Define a relationship with the Comment Model
    comments = db.relationship('Comment', back_populates='gym', cascade='all, delete')


# Define a schema for the Gym Model
class GymSchema(ma.Schema):
    # Define nested fields for related models
    user = fields.Nested('UserSchema', only=['name'])
    comments = fields.List(fields.Nested('CommentSchema'), exclude=('gym'))
    # Define validation rules for the 'title' field
    title = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')  
        ))
    # Define fields to be included in schema
    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'title', 'style', 'description', 'date', 'user', 'comments' )
        ordered = True

gym_schema = GymSchema()
gyms_schema = GymSchema(many=True)


