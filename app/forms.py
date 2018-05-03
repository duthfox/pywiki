#-*- coding:utf-8 -*-
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField, URLField
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Length

_required_text = '该字段为必填项'

validators = {
    'email': [
        DataRequired(message=_required_text),
    ],
    'username': [
        DataRequired(message=_required_text),
        Length(min=2, max=18, message='用户名长度为2到18位')
    ],
    'password': [
        DataRequired(message=_required_text),
        Regexp(regex=r'^[A-Za-z0-9@#$%^&+=_-]{6,18}$',message='密码格式错误')
    ]
}

class LoginForm(Form):
    email = EmailField('邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    # recaptcha = RecaptchaField('验证码', validators=[DataRequired()])

class RegisterForm(Form):
    email = EmailField('邮箱', validators=validators['email'])
    username = StringField('用户名', validators=validators['username'])
    password = PasswordField('密码', validators=validators['password'])
    repeat = PasswordField('重复密码', validators=validators['password'])

class BaseEntryForm(Form):
    title = StringField('名称', validators=[DataRequired(message=_required_text)])
    type = StringField('类别', validators=[DataRequired(message=_required_text)])

class ProfileForm(Form):
    username = StringField('呢称*', validators=validators['username'])
    location = StringField('所在地区', validators=[Length(max=64)])
    website = URLField('个人主页', validators=[Length(max=256)])
    introduction = TextAreaField('个人简介', validators=[Length(max=1024)])
