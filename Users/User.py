from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    plan = db.Column(db.String(80), nullable=False)
    subscription_date = db.Column(db.Date, nullable=False)
    expired_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20))  # New field
    is_blocked = db.Column(db.Boolean, default=False)
    device_info = db.Column(db.String(200))
    password_hash = db.Column(db.String(128), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='client')

    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'plan': self.plan,
            'subscription_date': self.subscription_date.isoformat(),
            'expired_date': self.expired_date.isoformat(),
            'phone': self.phone,
            'is_blocked': self.is_blocked
        }
    

    def block_user(self):
        self.is_blocked = True
        db.session.commit()
    
    def unblock_user(self):
        self.is_blocked = False
        db.session.commit()
    
    def auth(username, password):
        with app.app_context():
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                return user
            return None
        
    def get_user_by_username(username):
        with app.app_context():
            user = User.query.filter_by(username=username).first()
            if user:
                return user 
            return None
        
    def update_user(self, part, value):
        with app.app_context():
            setattr(self, part, value)
            db.session.commit()
    
    def delete_user(self):
        with app.app_context():
            db.session.delete(self)
            db.session.commit()
    

    @staticmethod
    def username_exists(username):
        with app.app_context():
            return db.session.query(User.username).filter_by(username=username).first() is not None
    
    @staticmethod
    def get_all_users():
        with app.app_context():
            users = User.query.all()
            return users



