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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='gyms')

class GymSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name'])

    class Meta:
        fields = ('id', 'name', 'address', 'phone', 'style', 'description', 'user' )
        ordered = True
        
gym_schema = GymSchema()
gyms_schema = GymSchema(many=True)


