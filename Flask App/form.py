from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])

    email = StringField('Email',validators=[DataRequired(),Email()])
    date = dateutil(label = 'Date', format='%Y-%m-%d')
    submit = SubmitField(label= 'sign up')


