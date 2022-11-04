from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from werkzeug.security import check_password_hash
from .models import User


class LoginForm(FlaskForm):
    """登录表单
    """

    def qs_username(username):
        # 对该字段在传递之前处理
        u = f'{username}123456'
        print(u)
        return username

    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(max=32, message="不符合字数要求！")
        ], filters=(qs_username,))
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(max=32, message="不符合字数要求！")
        ])
    """自定义验证器方法
    登录验证函数，该函数参数是固定的
    :param form: 表单
    :param field: 字段
    """

    def validate_username(form, field):
        # 查询当前输入是否在数据库中存在：用户、密码
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            error = '该用户不存在！'
            raise ValidationError(error)
        elif not check_password_hash(user.password, form.password.data):
            raise ValidationError('密码不正确')


class RegisterForm(FlaskForm):
    # 注册表单
    username = StringField('username', validators=[
        DataRequired(message="不能为空"), 
        Length(min=2, max=32, message="超过限制字数！")
        ])
    password = PasswordField('password', validators=[
        DataRequired(message="不能为空"),
        Length(min=2, max=32, message="超过限制字数！"),
        EqualTo('password1', message='两次密码输入不一致！')
        ])
    password1 = PasswordField('password1')

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            error = '该用户名称已存在！'
            raise ValidationError(error)