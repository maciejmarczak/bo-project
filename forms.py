from flask_wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class AlgorithmForm(Form):

    PROPER_NUMBER_ALERT = "This field should contain a number greater than 0"

    iterations_limit = IntegerField('iterations_limit', validators=[DataRequired(message=PROPER_NUMBER_ALERT),
                                                                   NumberRange(1)])
    employeed_bees = IntegerField('employeed_bees', validators=[DataRequired(message=PROPER_NUMBER_ALERT),
                                                               NumberRange(1)])
    onlooker_bees = IntegerField('onlooker_bees', validators=[DataRequired(message=PROPER_NUMBER_ALERT),
                                                             NumberRange(1)])
    scout_bees = IntegerField('scout_bees', validators=[DataRequired(message=PROPER_NUMBER_ALERT),
                                                       NumberRange(1)])
