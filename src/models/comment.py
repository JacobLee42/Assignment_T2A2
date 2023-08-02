# Import modules
from init import db, ma
from marshmallow import fields

# Define a Comment Model
class Comment(db.Model):
    __tablename__ = 'comments'

    # Define columns for table
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)


    # Define relationship with other models
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    gym = db.relationship('Gym', back_populates='comments')


# Define schema for Comment model
class CommentSchema(ma.Schema):
    # Define nested fields for related models
    user = fields.Nested('UserSchema', only=['name', 'email'])
    gym = fields.Nested('GymSchema', exclude=['comments'])

    # Define the fields to include in schema
    class Meta:
        fields = ('id', 'message', 'gym', 'user')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
