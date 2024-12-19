from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    id_event = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    event = db.relationship('Event', backref=db.backref('comments', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('comments', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Comment {self.id}>'