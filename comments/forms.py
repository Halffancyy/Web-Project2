from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

# 评论表单
class CommentForm(FlaskForm):
    # 内容字段，必须输入，长度在1到500个字符之间
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=500)])
    # 提交按钮
    submit = SubmitField('Submit Comment')