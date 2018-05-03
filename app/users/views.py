#-*- coding:utf-8 -*-
from app.extensions import mongo
from app.forms import LoginForm, RegisterForm, ProfileForm
from app.models import User
from app.util import bson_obj_id, AllowFile
from gridfs import GridFS, NoFile
from flask import render_template, redirect, url_for, request, flash, jsonify, abort, make_response
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.mail import Message
from werkzeug.utils import secure_filename

from app.tasks.mail import send_async_email

from . import users

def send_email(to, subject, template, **kwargs):
    from app import app
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
        sender= app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    send_async_email(msg)

@users.route('/confirm/<token>')
@login_required
def confirm(token):
    user = User.verify_auth_token(token)
    if user:
        r = User.set_active(user['_id'])
        if r:
            flash('激活成功', 'green')
        else:
            flash('激活失败', 'red')
    return redirect(url_for('main.index'))


@users.route('/sign_up', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    lg_form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            uname = form.username.data
            passwd = form.password.data
            rp_passwd = form.repeat.data
            if passwd != rp_passwd:
                flash('两次密码不相同', 'WARNING')
            elif User.find_by_username(uname) is not None:
                flash('该用户名已被注册', 'WARNING')
            elif User.find_by_email(email) is not None:
                flash('该邮箱已被注册', 'WARNING')
            else:
                id = User.add_user(email, uname, passwd)
                if id is not None:
                    user = User(bson_obj_id(id))
                    login_user(user)
                    token = user.gen_auth_token(expiration=600)
                    send_email(email, '欢迎注册pywiki,请确认你的账户', 'email', token=token)
                    return redirect(url_for('main.index'))
                flash('注册失败', 'WARNING')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash("%s: %s" %(getattr(form, field).label.text, error), 'WARNING')
    return render_template('register.html', form=form, lg_form=lg_form)

@users.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            db_user = User.find_by_email(form.email.data)
            if db_user is not None:
                db_passwd = db_user.get('password', None)
                if User.verify_passwd(db_passwd, form.password.data):
                    user = User(db_user['_id'])
                    login_user(user)
                    return jsonify(status=True, reason="登录成功", redirect_url=url_for('main.index'))
                else:
                    return jsonify(status=False, reason="邮箱或密码错误")
            else:
                return jsonify(status=False, reason="不存在该用户")
        return jsonify(status=False, reason="登录失败")

@users.route('/profile')
@users.route('/profile/<id>')
def profile(id=None):
    user = None
    if id is None:
        if current_user is not None:
            return redirect(url_for('.profile', id=current_user.id))
    else:
        user = User.find_by_id(bson_obj_id(id))
    return render_template('profile.html', user=user)

@users.route('/profile/edit', methods=['GET','POST'])
@login_required
def profile_edit():
    user = User.find_by_id(bson_obj_id(current_user.id))
    if not user:
        abort(404)
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            location = form.location.data
            website = form.website.data
            introduction = form.introduction.data
            data = {
                'username': username,
                'location': location,
                'website': website,
                'introduction': introduction
            }

            avatar = request.files['avatar']
            if avatar and AllowFile.is_img(avatar.filename):
                filename = secure_filename(avatar.filename)
                fs = GridFS(mongo.db, collection="avatar")
                avatar_id = fs.put(avatar, content_type=avatar.content_type, filename=filename)
                if avatar_id:
                    if user['avatar']:
                        fs.delete(bson_obj_id(user['avatar']))
                    data['avatar'] = avatar_id
            else:
                flash('图片格式不支持', 'red')

            User.update_user(user['_id'], data)

            return redirect(url_for('.profile'))
        else:
            flash('资料修改失败', 'red')
    return render_template('profile_edit.html', user=user, form=form, title='编辑资料')

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/static/avatar/<oid>')
def avatar(oid):
    if oid is None:
        return ''
    try:
        fs = GridFS(mongo.db, "avatar")
        img = fs.get(bson_obj_id(oid))
        response = make_response(img.read())
        response.headers['Content-Type'] = img.content_type
        return response
    except NoFile:
        abort(404)
