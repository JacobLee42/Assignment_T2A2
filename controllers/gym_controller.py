from flask import Blueprint, request
from init import db
from models.gym import Gym, gyms_schema, gym_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.comment import Comment, comment_schema, comments_schema

gyms_bp = Blueprint('gyms', __name__, url_prefix='/gyms')

@gyms_bp.route('/')
def get_all_gyms():
    stmt = db.select(Gym)
    gyms = db.session.scalars(stmt)
    return gyms_schema.dump(gyms)

@gyms_bp.route('/<int:id>')
def get_one_gym(id):
    stmt = db.select(gym).filter_by(id=id)
    gym = db.session.scalar(stmt)
    if gym:
        return gym_schema.dump(gym)
    else:
        return {'error': f'Gym not found with id {id}'}, 404
    
@gyms_bp.route('/', methods=['POST'])
@jwt_required()
def create_gym():
    body_data = request.get_json()
    gym = Gym(
        title=body_data.get('title'),
        name=body_data.get('name'),
        address=body_data.get('address'),
        phone=body_data.get('phone'),
        style=body_data.get('style'),
        description=body_data.get('description'),
        user_id=get_jwt_identity()
    )

    db.session.add(gym)
    db.session.commit()

    return gym_schema.dump(gym), 201

@gyms_bp.route('/<int:id>', methods={'DELETE'})
@jwt_required()
def delete_one_gym(id):
    stmt = db.select(Gym).filter_by(id=id)
    gym = db.session.scalar(stmt)
    if gym:
        db.session.delete(gym)
        db.session.commit()
        return {'message': f'Gym {gym.title} deleted successfully'}
    else: 
        return {'error': f'Gym not found with id {id}'}, 404

@gyms_bp.route('/<int:id>', methods=['PUT', 'PATCH']) 
@jwt_required()
def update_one_gym(id): 
    body_data = request.get_json()
    stmt = db.select(Gym).filter_by(id=id)
    gym = db.session.scalar(stmt)
    if gym:
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
    

@gyms_bp.route('/<int:gym_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(gym_id):
    body_data = request.get_json()
    stmt = db.select(Gym).filter_by(id=gym_id)
    gym = db.session.scalar(stmt)
    if gym:
        comment = Comment(
            message=body_data.get('message'),
            user_id=get_jwt_identity(),
            gym_id=gym.id
        )
        
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {'error': f'Gym not found with id {gym_id}'}, 404
    

@gyms_bp.route('/<int:gym_id>/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(gym_id, comment_id):
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'Comment {comment.message} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404
    

@gyms_bp.route('/<int:gym_id>/comments/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(gym_id, comment_id):
    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        comment.message = body_data.get('message') or comment.message
        db.session.commit()
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404