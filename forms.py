from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from datetime import datetime, date

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

# 请求创建表单
class RequestForm(FlaskForm):
    # 标题字段，必须输入
    title = StringField('Title', validators=[DataRequired()])
    # 描述字段，必须输入
    description = TextAreaField('Description', validators=[DataRequired()])
    # 提交按钮
    submit = SubmitField('Submit')

# 评论表单
class CommentForm(FlaskForm):
    # 内容字段，必须输入，长度在1到500个字符之间
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=500)])
    # 提交按钮
    submit = SubmitField('Submit Comment')
