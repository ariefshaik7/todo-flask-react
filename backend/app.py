import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- Configuration ---
# IMPORTANT: Change this secret key! It's used for session security and JWT signing.
app.config['SECRET_KEY'] = 'a-very-secret-key-that-you-should-change'

# IMPORTANT: Update this with your PostgreSQL credentials!
# Format: postgresql://<your_username>:<your_password>@<host>/<database_name>
# Example: 'postgresql://postgres:admin123@localhost/todolist'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/todolist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Database and Hashing Setup ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- Database Models ---

class User(db.Model):
    """User model for storing user credentials."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class Todo(db.Model):
    """Todo model for storing task items."""
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """Serializes the Todo object to a dictionary."""
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed,
            'user_id': self.user_id
        }

# --- Authentication Decorator ---

def token_required(f):
    """Decorator to protect routes by validating JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for token in the 'x-access-token' header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token using the secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                 return jsonify({'message': 'User not found!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Pass the current_user object to the decorated function
        return f(current_user, *args, **kwargs)
    return decorated


# --- API Routes ---

# User Registration
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists!'}), 409

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

# User Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Generate JWT
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24) # Token expires in 24 hours
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

# --- To-Do List Routes (Protected) ---

@app.route('/api/todos', methods=['GET'])
@token_required
def get_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.id).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()
    task = data.get('task')

    if not task:
        return jsonify({'message': 'Task content is required'}), 400

    new_todo = Todo(task=task, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify(new_todo.to_dict()), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message': 'Todo not found or you do not have permission to edit it'}), 404

    data = request.get_json()
    if 'completed' in data:
        todo.completed = data['completed']

    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

    if not todo:
        return jsonify({'message': 'Todo not found or you do not have permission to delete it'}), 404

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully!'})


if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    # Run the Flask app
    app.run(port=5001, debug=True)