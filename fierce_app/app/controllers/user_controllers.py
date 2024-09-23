from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.extensions import bcrypt, db

# Create a Blueprint for user endpoints
user = Blueprint('user', __name__, url_prefix='/api/v1/user')

# Define the registration endpoint
@user.route('/register', methods=['POST'])
def register():
    try:
        # Extract request data
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')  # Extract the password correctly
        role = data.get('role', 'customer')
        phone_number = data.get('phone_number')
        address = data.get('address')

        # Validate required fields
        required_fields = ['name', 'email', 'password']
        if not all(data.get(field) for field in required_fields):
            return jsonify({'error': 'All fields are required'}), 400

        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password is too short'}), 400

        # Check if email already exists
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error': 'Email already exists'}), 409

        # Create a new user object
        new_user = User(
            name=name,
            email=email,
            password=password,  # Pass the plain password, it will be hashed in the model
            role=role,
            phone_number=phone_number,
            address=address
        )

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Response with sanitized user data (without password_hash)
        response_user = {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'phone_number': new_user.phone_number,
            'address': new_user.address,
            'role': new_user.role,
            'created_at': new_user.created_at,
            'updated_at': new_user.updated_at
        }

        return jsonify({
            'message': f'{new_user.name} has been successfully created',
            'user': response_user
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the login endpoint
@user.route('/login', methods=["POST"])
def login():
    try:
        # Extract request data
        data = request.json
        email = data.get("email")
        password = data.get("password")  # Extract the password correctly

        # Retrieve user by email
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Create access token
            access_token = create_access_token(identity={'id': user.id, 'role': user.role})
            return jsonify({
                'access_token': access_token,
                'user_id': user.id,
                'isAdmin': user.role == 'admin'
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Editing a User endpoint
@user.route('/edit/<int:user_id>', methods=["PUT"]) 
@jwt_required() 
def edit_user(user_id):
    try: 
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user['id']).first()

        # Get the user to be edited
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        elif loggedInUser.role != 'admin' and user.id != current_user['id']:
            return jsonify({'error': 'You are not authorized to update user details'}), 403

        # Get request data
        data = request.get_json()

        # Update user fields if provided in request
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.role = data.get('role', user.role)

        # Update password if provided
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.set_password(password)  # Use the set_password method to hash the password

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            'message': f"{user.name}'s details have been successfully updated",
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'role': user.role,
                'updated_at': user.updated_at,
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the delete user endpoint
@user.route('/delete/<int:user_id>', methods=["DELETE"]) 
@jwt_required() 
def delete_user(user_id): 
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user['id']).first()

        # Get current user by id
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Check authorization
        if loggedInUser.role != 'admin':
            return jsonify({'error': 'You are not authorized to delete this user'}), 403

        # Delete user from database
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all users endpoint
@user.route('/all_users', methods=["GET"])
@jwt_required()  # Protect this endpoint with JWT authentication
def get_all_users():
    try:
        # Check if current user is admin
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user['id']).first()
        if not loggedInUser or loggedInUser.role != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        # Fetch all users
        users = User.query.all()

        # Serialize users data (exclude sensitive fields)
        serialized_users = []
        for user in users:
            serialized_user = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'role': user.role,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            serialized_users.append(serialized_user)

        return jsonify(serialized_users), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get current user endpoint
@user.route('/current_user', methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['id']).first()

        if user:
            # Serialize user data (exclude sensitive fields like password_hash)
            serialized_user = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'role': user.role
            }
            return jsonify(serialized_user), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_token(user_id):
    try:
        # Set the expiration time for the token (e.g., 1 day)
        expiration_time = datetime.utcnow() + timedelta(days=1)
        
        # payload is a JSON object that contains assertions about the user or any entity
        # In this case the payload is containing user_id and expiration time
        payload = {
            'user_id': user_id,
            'exp': expiration_time
        }

        # Encode the payload and create the token jwt(JSON Web Tokens)
        # algorithm is the method used for signing and verifying the token
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return token

    except Exception as e:
        # Handle token generation error
        print(f"Token generation failed: {str(e)}")

