from app import db
from enum import Enum

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # Relationship with Events
    events = db.relationship('Event', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    header = db.Column(db.Text)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    
    # Field for the user who created the event
    id_user_creator = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # Field for category
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Event {self.name}>'