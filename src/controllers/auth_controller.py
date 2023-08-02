from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta


# Create a blueprint for authentication with a URL prefix of '/auth'.
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Define a route to register a new user
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:   
        body_data = request.get_json()
        # Create a new User model instance from user info
        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        # Add the user to the session
        db.session.add(user)
        # Commit to add the user to database
        db.session.commit()
        # Respond to the client
        return user_schema.dump(user), 201
    
    # Handle errors that may occur when adding the user to database
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address is already in use' }, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return { 'error': f'The {err.orig.diag.column_name} is required' }, 409
        

# Define a route to log in a user and generate access token
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct, create an access token with their ID and return it along with email and admin status.
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return { 'email': user.email, 'token': token, 'is_admin': user.is_admin }
    else:
        return { 'error': 'Invalid email or password' }, 401



# Define a route to delete a user by ID
@auth_bp.route('/user/<int:user_id>', methods=['DELETE'])
def auth_delete_user(user_id):
    # Select the user by ID and delete them from database if they exist, otherwise return an error message.
    user = db.session.query(User).filter_by(id=user_id).first()
    if user: 
        db.session.delete(user)
        db.session.commit()
        return { 'message': 'User and login deleted successfully' }
    else:
        return { 'error': 'User not found' }, 404