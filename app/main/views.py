#-*- coding:utf-8 -*-
from app.forms import LoginForm, BaseEntryForm
from app.models import Item
from app.util import TypeRender
from collections import defaultdict
from flask import render_template, request, flash, url_for, abort, redirect, jsonify
from flask.ext.login import current_user, login_required
from .. import users
from app.util import bson_obj_id

from . import main
import re

@main.route('/')
def index():
    lg_form = LoginForm()
    return render_template('index.html', lg_form=lg_form, title='首页')

pk_regx = re.compile(r'(\w+)\s+(pk|Pk|pK|PK)\s+(\w+)', re.IGNORECASE)

@main.route('/pk', methods=['GET', 'POST'])
def pk():
    if request.method == 'POST':
        pk_str = request.form.get('pk').strip()
        g = pk_regx.match(pk_str)
        if g:
            pk1_title = g.groups()[0]
            pk2_title = g.groups()[2]
            pk1_regx = re.compile(pk1_title, re.IGNORECASE)
            pk2_regx = re.compile(pk2_title, re.IGNORECASE)
            pk1_item = Item.find_item(pk1_regx)
            pk2_item = Item.find_item(pk2_regx)
            if pk1_item and pk2_item:
                # 按首字母大小排序
                rows_by_name = defaultdict(list)
                for attr in pk1_item['attributes']:
                    rows_by_name[attr['attr_name']].append(attr)
                for attr in pk2_item['attributes']:
                    # 保证顺序
                    if not attr['attr_name'] in rows_by_name.keys():
                        rows_by_name[attr['attr_name']].append({})
                    rows_by_name[attr['attr_name']].append(attr)

                for key, attrs in rows_by_name.items():
                    if len(attrs) == 1:
                        attrs.append({})

                return render_template('pk.html', pk1=pk1_item, pk2=pk2_item,\
                                       rows=rows_by_name, TypeRender=TypeRender)
            else:
                if not pk1_item:
                    flash('搜索不到%s'%pk1_title, 'red')
                if not pk2_item:
                    flash('搜索不到%s'%pk2_title, 'red')
        else:
            flash('输入格式有误', 'red')
    return redirect(url_for('.index'))


@main.route('/explore')
def explore():
    items = Item.find_items()
    return render_template('explore.html', items=items, title='发现')

@main.route('/lucky')
def lucky():
    # 总条数
    item = Item.get_random_item()
    if item:
        return redirect(url_for('.item', title=item['title']))
    return redirect(url_for('.index'))

@main.route('/search')
def search():
    q = request.args.get('q', None)
    if q is None:
        abort(404)
    keyword = q.strip()
    regx = re.compile(r'%s' %keyword, re.IGNORECASE)
    list = Item.find_items(regx)
    if list.count() == 0:
        flash('没有找到结果', 'search')
    return render_template('explore.html', items=list, title='搜索')

@main.route('/item/<title>')
def item(title):
    item = Item.find_item(title)
    if not item:
        abort(404)
    Item.inc_view(title)
    return render_template('item.html', item=item, TypeRender=TypeRender)

@main.route('/item/edit_attr', methods=['POST'])
def edit_attr():
    if request.method == 'POST':
        title = request.json['title']
        attr_name = request.json['attr_name'].strip()
        attr_type = request.json['attr_type']
        attr_value = request.json['attr_value'].strip()

        user = users.views.User.find_by_id(bson_obj_id(current_user.id))
        if not user:
            return jsonify(status=False, reason="权限不足")
        if not attr_name:
            return jsonify(status=False, reason="属性名不能为空")
        if not attr_value:
            return jsonify(status=False, reason="属性值不能为空")
        status = Item.edit_attr(title, attr_name, attr_value, attr_type)
        if status:
            if current_user.is_authenticated:
                current_user.add_edit()
            return jsonify(status=True, reason="修改属性成功")
        else:
            return jsonify(status=True, reason="修改失败")

@main.route('/item/del_attr', methods=['POST'])
@login_required
def del_attr():
    if request.method == 'POST':
        title = request.json['title']
        attr_name = request.json['attr_name']
        status = Item.del_attr(title, attr_name)
        if status:
            return jsonify(status=True, reason="删除属性成功")
        else:
            return jsonify(status=True, reason="删除失败")

@main.route('/item/add_attr', methods=['POST'])
def add_attr():
    if request.method == 'POST':
        title = request.json['title']
        attr_name = request.json['attr_name'].strip()
        attr_type = request.json['attr_type']
        attr_value = request.json['attr_value'].strip()
        if not attr_name:
            return jsonify(status=False, reason="属性名不能为空")
        if not attr_value:
            return jsonify(status=False, reason="属性值不能为空")
        if Item.find_attr(title, attr_name) is not None:
            return jsonify(status=False, reason="属性已存在")
        status = Item.add_attr(title, attr_name, attr_value, attr_type)
        if status:
            if current_user.is_authenticated:
                current_user.add_edit()
        html = TypeRender.render_html(attr_name, attr_value, attr_type)
        return jsonify(status=True, reason="添加属性成功", html=html)

@main.route('/create_entry', methods=['GET', 'POST'])
def create_entry():
    entry_form = BaseEntryForm()
    if entry_form.validate_on_submit():
        title = request.form['title'].strip()
        type = request.form['type'].strip()
        if not title:
            flash('属性不能为空', 'red')
        elif not type:
            flash('类型不能为空', 'red')
        elif Item.find_item(title):
            flash('词条已存在', 'yellow')
        else:
            status = Item.create_item(title, type)
            if status:
                Item.add_type(type)
                if current_user.is_authenticated:
                    current_user.add_create()
            return redirect(url_for('.item', title=title))
    else:
        for field, errors in entry_form.errors.items():
            for error in errors:
                flash("%s: %s" %(getattr(entry_form, field).label.text, error), 'red')
    types = Item.types()
    return render_template('create.html', entry_form=entry_form, title='创建条目', types=types)

