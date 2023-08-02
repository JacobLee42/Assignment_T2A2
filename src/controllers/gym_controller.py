# Import modules
from flask import Blueprint, request
from init import db
from models.gym import Gym, gyms_schema, gym_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.comment_controller import comments_bp
from datetime import date
from models.user import User

# Create a blueprint for gyms with URL prefix of '/gyms
gyms_bp = Blueprint('gyms', __name__, url_prefix='/gyms')
gyms_bp.register_blueprint(comments_bp, url_prefix='/<int:gym_id>/comments')

# Define a route to get all gyms
@gyms_bp.route('/', methods=["GET"])
def get_all_gyms():
    stmt = db.select(Gym).order_by(Gym.date.desc())
    gyms = db.session.scalars(stmt)
    return gyms_schema.dump(gyms)

# Define a route to get one gym by id
@gyms_bp.route('/<int:id>', methods=["GET"])
def get_one_gym(id):
    stmt = db.select(Gym).filter_by(id=id)
    gym = db.session.scalar(stmt)
    if gym:
        return gym_schema.dump(gym)
    else:
        return {'error': f'Gym not found with id {id}'}, 404


# Define a route to create a new gym
@gyms_bp.route('/', methods=['POST'])
@jwt_required()
def create_gym():
    body_data = gym_schema.load(request.get_json())
    gym = Gym(
        title=body_data.get('title'),
        name=body_data.get('name'),
        address=body_data.get('address'),
        phone=body_data.get('phone'),
        style=body_data.get('style'),
        description=body_data.get('description'),
        date=date.today(),
        user_id=get_jwt_identity()
    )

    # Add the new gym to the database and commit the transaction
    db.session.add(gym)
    db.session.commit()

    return gym_schema.dump(gym), 201


# Define a route to delete one gym by ID
@gyms_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_gym(id):
    # Check if current user is an admin, if not return error message
    is_admin = authorise_as_admin()
    if not is_admin:
        return {'error': 'Not authorised to delete gyms'}, 403
    stmt = db.select(Gym).filter_by(id=id)
    gym = db.session.scalar(stmt)
    if gym:
        db.session.delete(gym)
        db.session.commit()
        return {'message': f'Gym {gym.title} deleted successfully'}
    else: 
        return {'error': f'Gym not found with id {id}'}, 404
    

# Define a route to update one gym by id
@gyms_bp.route('/<int:id>', methods=['PUT', 'PATCH']) 
@jwt_required()
def update_one_gym(id): 
    body_data = gym_schema.load(request.get_json(), partial=True)
    stmt = db.select(Gym).filter_by(id=id)
    gym = db.session.scalar(stmt)

    # if gym exists, check current user is owner, if not return error message
    if gym:
        if str(gym.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the gym can edit'}, 403
        gym.title = body_data.get('title') or gym.title
        gym.description = body_data.get('description') or gym.description
        gym.name = body_data.get('name') or gym.name 
        gym.address = body_data.get('address') or gym.address
        gym.phone = body_data.get('phone') or gym.phone
        gym.style = body_data.get('style') or gym.style
        
        db.session.commit()
        return gym_schema.dump(gym)
    else:
        return {'error': f'Gym not found with id {id}'}, 404
    

# Define helper function to check if current user is an admin 
def authorise_as_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin
    