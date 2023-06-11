from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Length, Regexp

class RegistrationForm(FlaskForm):
    # name is optional string field
    name = StringField('name')
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6), Regexp('[A-Z]+', message='Password must contain at least one uppercase letter')])
    confirm = PasswordField('confirm', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])

class AddTaskForm(FlaskForm):
    content = StringField('content', validators=[DataRequired()])
    priority = IntegerField('priority', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('submit')
