from app import db
from datetime import datetime

"""
class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    id_event = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    
    event = db.relationship('Event', backref='surveys')

    def __repr__(self):
        return f'<Survey {self.id_survey}>'
"""

class SurveyOption(db.Model):
    __tablename__ = 'survey_options'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.Column(db.Text, nullable=False)

    id_survey = db.Column(db.Integer, db.ForeignKey('event_occurrences.id', ondelete='CASCADE'), nullable=True)
    
    survey = db.relationship('EventOccurrence', backref=db.backref('options', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<SurveyOption {self.id}>'

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    id_survey = db.Column(db.Integer, db.ForeignKey('event_occurrences.id', ondelete='CASCADE'), nullable=False)
    id_option = db.Column(db.Integer, db.ForeignKey('survey_options.id', ondelete='CASCADE'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    survey = db.relationship('EventOccurrence', backref=db.backref('responses', cascade='all, delete-orphan'))
    option = db.relationship('SurveyOption', backref=db.backref('responses', cascade='all, delete-orphan'))
    user = db.relationship('User', backref=db.backref('responses', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<SurveyResponse {self.id}>'