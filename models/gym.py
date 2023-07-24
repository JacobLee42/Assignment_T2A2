from init import db, ma
from marshmallow import fields

class Gym(db.Model):
    __tablename__= "gyms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    style = db.Column(db.String(100))
    description = db.Column(db.Text)
    title = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='gyms')
    comments = db.relationship('Comment', back_populates='gym', cascade='all, delete')

class GymSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name'])
    comments = fields.List(fields.Nested('CommentSchema'), exclude=('gym'))

    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'title', 'style', 'description', 'user', 'comments' )
        ordered = True

gym_schema = GymSchema()
gyms_schema = GymSchema(many=True)


