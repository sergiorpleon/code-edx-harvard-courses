from datetime import datetime
from flask_login import UserMixin
from app import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationship with Users
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Field for user role
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relationship with Events
    events = db.relationship('Event', backref='creator', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def is_admin(self):
        return self.id_role.name == 'administrator'
    
    def allowed(self, access_level):
        role = Role.query.filter_by(name=access_level).first()
        return self.id_role >= role.id