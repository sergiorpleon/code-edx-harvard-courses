from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FormField, SubmitField, FieldList, RadioField
from wtforms.validators import DataRequired
from app.models import OcurrenceTypeEnum  # Asegúrate de importar tu Enum

class SurveyOptionForm(FlaskForm):
    option = StringField('Option')

class EventOccurrenceForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    ocurrence_type = SelectField('Ocurrence type', choices=[(type.name, type.value) for type in OcurrenceTypeEnum], validators=[DataRequired()])
    options = FieldList(FormField(SurveyOptionForm), min_entries=5)
    submit = SubmitField('Save')
    
class EmptyForm(FlaskForm):
    pass
