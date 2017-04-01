from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class AlgorithmForm(Form):
    iterations_limit = StringField('iterations_limit', validators=[DataRequired()])
