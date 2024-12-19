from app import db
from datetime import datetime
from enum import Enum


class OcurrenceTypeEnum(Enum):
    NARRATION = "narration"
    SURVEY = "survey"

class EventOccurrence(db.Model):
    __tablename__ = 'event_occurrences'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    ocurrence_type = db.Column(db.Enum(OcurrenceTypeEnum), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.now())

    #id_ocurrence_type = db.Column(db.Integer, db.ForeignKey('ocurrence_types.id'), nullable=False)
    
    id_event = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    event = db.relationship('Event', backref=db.backref('occurrences', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('occurrences', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<EventOccurrence {self.id}>'