from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# 请求创建表单
class RequestForm(FlaskForm):
    # 标题字段，必须输入
    title = StringField('Title', validators=[DataRequired()])
    # 描述字段，必须输入
    description = TextAreaField('Description', validators=[DataRequired()])
    # 提交按钮
    submit = SubmitField('Submit')