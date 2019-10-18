from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,RadioField
from datetime import datetime, timedelta
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email



class date(FlaskForm):
    enterDate = DateField('dateInput',format = '%Y-%m-%d',default=datetime.today())
    selectType = RadioField("Data Type", choices=[('1','per-game'),('2','zscores')],default='1')
    submit = SubmitField('submit')

