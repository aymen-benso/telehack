from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Users.User import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)


class Complaint(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_resolved = db.Column(db.Boolean, default=False)
    response = db.Column(db.String(255))
    responder_full_name = db.Column(db.String(80))
    responder_username = db.Column(db.String(80))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'is_resolved': self.is_resolved
        }

    def resolve_complaint(self):
        self.is_resolved = True
        db.session.commit()

    def unresolve_complaint(self):
        self.is_resolved = False
        db.session.commit()

    def get_complaints_by_user_id(user_id):
        with app.app_context():
            complaints = Complaint.query.filter_by(user_id=user_id).all()
            if complaints:
                return complaints
            return None

    def get_complaint_by_id(id):
        with app.app_context():
            complaint = Complaint.query.filter_by(id=id).first()
            if complaint:
                return complaint
            return None
        
    def add_complaint(user_id, title, description):
        with app.app_context():
            complaint = Complaint(
                user_id=user_id,
                title=title,
                description=description
            )
            db.session.add(complaint)
            db.session.commit()
            return complaint
    
    def respond_complaint(id, response, full_name, username):
        with app.app_context():
            complaint = Complaint.query.filter_by(id=id).first()
            if complaint:
                complaint.update_complaint(response, full_name, username)
                return complaint
            return None
        
    @staticmethod
    def get_all_complaints():
        with app.app_context():
            complaints = Complaint.query.all()
            if complaints:
                return complaints
            return None

print('test_respondTocomplain',