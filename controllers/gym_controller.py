from flask import Blueprint, request
from init import db
from models.gym import Gym, gyms_schema, gym_schema

gyms_bp = Blueprint('gyms', __name__, url_prefix='/gyms')

@gyms_bp.route('/')
def get_all_gyms():
    stmt = db.select(Gym)
    gyms = db.session.scalars(stmt)
    return gyms_schema.dump(gyms)
