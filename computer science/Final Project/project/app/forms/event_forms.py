from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired
from app.models import Category
from datetime import datetime


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    save = SubmitField('Save')

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    header = TextAreaField('Header')
    description = TextAreaField('Description')
    date = DateTimeField('Fecha y Hora', default=datetime.utcnow, format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    save_and_view = SubmitField('Save and View')
    save = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
  