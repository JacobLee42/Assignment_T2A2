from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gyms.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    gym = db.relationship('Gym', back_populates='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    gym = fields.Nested('GymSchema', exclude=['comments'])

    class Meta:
        fields = ('id', 'message', 'gym', 'user')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
