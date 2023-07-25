from flask import Blueprint, request
from init import db
from models.gym import Gym
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__)



@comments_bp.route('/', methods=['POST'])
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
    

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
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
    

@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
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