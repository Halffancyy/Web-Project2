from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length

# RegisterForm
class RegisterForm(FlaskForm):
    # Username field, required, length between 4 and 15 characters
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    # Email field, required, must be a valid email format, max length of 50 characters
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    # Password field, required, length between 8 and 80 characters
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Register')

# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')