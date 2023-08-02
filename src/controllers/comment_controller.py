# Import the modules
from flask import Blueprint, request
from init import db
from models.gym import Gym
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a blueprint for comments
comments_bp = Blueprint('comments', __name__)


# Define a route to create a new comment for a gym
@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(gym_id):
    body_data = request.get_json()
    stmt = db.select(Gym).filter_by(id=gym_id)
    gym = db.session.scalar(stmt)

    # if gym exists, create a new Comment and the current user's ID and add to database
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
    

# Define a route to delete a comment from a gym
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(gym_id, comment_id):
    # Select comment by ID
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)

    # if the comment exists, delete from database and return success message, otherwise return an error message
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'message': f'Comment {comment.message} deleted successfully'}
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404
    
    

    