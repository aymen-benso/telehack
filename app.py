from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Users.User import User
from Complaints.Complaint import Complaint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db.init_app(app)

print('Database created', db)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.get_all_users()
    if users:
        return jsonify([user.serialize() for user in users], 200)
    else:
        return jsonify({'error': 'No users found'}, 404)

@app.route('/api/users/addUser', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    full_name = data.get('full_name')
    username = data.get('username')
    plan = data.get('plan')
    subscription_date = datetime.strptime(data.get('subscription_date'), '%Y-%m-%d').date()
    expired_date = datetime.strptime(data.get('expired_date'), '%Y-%m-%d').date()
    phone = data.get('phone')
    password = data.get('password')
    password_hash = generate_password_hash(password)
    username_exists = User.username_exists(username)
    if data :
        if username_exists is False:
            user = User(
                full_name=full_name,
                username=username,
                plan=plan,
                subscription_date=subscription_date,
                expired_date=expired_date,
                phone=phone,
                password_hash=password_hash
            )
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'User created successfully'}, 201)
        else:
            return jsonify({'error': 'Username already exists'}, 400)
    else:
        return jsonify({'error': 'The request payload is empty'}, 400)
    

@app.route('/api/users/authUser', methods=['GET'])
def authenticate_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.auth(username,password)

    if user is None:
        return jsonify({'isAuthenticated': False, 'message': 'User not found.'}, 404)

    if user.is_blocked:
        user.Block_user()
        return jsonify({'isAuthenticated': False, 'message': 'This account has been blocked due to too many failed login attempts.'}, 401)

    if not check_password_hash(user.password_hash, password):
        failed_attempts += 1
        if failed_attempts >= 5:
            user.is_blocked = True
        user.device_info = request.headers.get('User-Agent')
        db.session.commit()
        return jsonify({'isAuthenticated': False, 'message': 'Invalid password.'}, 401)

    user.failed_attempts = 0
    db.session.commit()
    return jsonify({'isAuthenticated': True, 'message': 'User authenticated successfully.','user':{'id': user.id ,'full_name': user.full_name,'username': user.username,'plan': user.plan,'subscription_date': user.subscription_date,'expired_date': user.expired_date,'phone': user.phone,'role': user.role}}, 200)

@app.route('/api/user', methods=['GET'])
def get_user():
    data = request.get_json()
    username = data.get('username')
    user = User.get_user_by_username(username)
    if user:
        print(user)
        return jsonify(user.serialize(), 200)
    else:
        return jsonify({'error': 'User not found'}, 404)

@app.route('/api/blockUser', methods=['PUT'])
def block_user():
    data = request.get_json()
    username = data.get('username')
    user = User.get_user_by_username(username)
    if user:
        user.block_user()
        return jsonify({'message': 'User blocked successfully'}, 200)
    else:
        return jsonify({'error': 'User not found'}, 404)

@app.route('/api/unblockUser', methods=['PUT'])
def unblock_user():
    data = request.get_json()
    username = data.get('username')
    user = User.get_user_by_username(username)
    if user:
        user.unblock_user()
        return jsonify({'message': 'User unblocked successfully'}, 200)
    else:
        return jsonify({'error': 'User not found'}, 404)

@app.route('/api/deleteUser', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    username = data.get('username')
    user = User.get_user_by_username(username)
    if user:
        user.delete_user()
        return jsonify({'message': 'User deleted successfully'}, 200)
    else:
        return jsonify({'error': 'User not found'}, 404)

@app.route('/api/updateUser', methods=['PUT'])
def update_user():
    data = request.get_json()
    username = data.get('username')
    part = data.get('part')
    value = data.get('value')
    user = User.get_user_by_username(username)
    if user:
        user.update_user(part, value)
        return jsonify({'message': 'User updated the '+ part +' successfully'}, 200)
    else:
        return jsonify({'error': 'User not found'}, 404)


@app.route('/api/addComplaint', methods=['POST'])
def add_complaint():
    # Get the data from the request
    data = request.get_json()
    if data:
        # Create a new complaint
        complaint = Complaint(
            title=data.get('title'),
            description=data.get('description'),
            user_id=data.get('user_id'),
            created_at=datetime.now()
        )
        db.session.add(complaint)
        db.session.commit()
        return jsonify({'message': 'Complaint created successfully'}, 201)
    else:
        return jsonify({'error': 'The request payload is empty'}, 400)

@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.get_all_complaints()
    if complaints:
        return jsonify([complaint.serialize() for complaint in complaints], 200)
    else:
        return jsonify({'error': 'No complaints found'}, 404)


@app.route('/api/respondTocomplaint', methods=['GET'])
def respond_to_complaint():
    data = request.get_json()
    id = data.get('id')
    response = data.get('response')
    full_name = data.get('full_name')
    username = data.get('username')
    complaint = Complaint.respond_complaint(id, response, full_name, username)
    if complaint:
        return jsonify(complaint.serialize(), 200)
    else:
        return jsonify({'error': 'Complaint not found'}, 404)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database
    app.run()