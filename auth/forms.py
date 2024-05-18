from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length

# 用户注册表单
class RegisterForm(FlaskForm):
    # 用户名字段，必须输入，长度在4到15个字符之间
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    # 邮箱字段，必须输入，格式必须为有效的邮箱，最大长度为50个字符
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    # 密码字段，必须输入，长度在8到80个字符之间
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    # 提交按钮
    submit = SubmitField('Register')

# 用户登录表单
class LoginForm(FlaskForm):
    # 用户名字段，必须输入，长度在4到15个字符之间
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    # 密码字段，必须输入，长度在8到80个字符之间
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    # 提交按钮
    submit = SubmitField('Login')