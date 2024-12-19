from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FormField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Submit')
    