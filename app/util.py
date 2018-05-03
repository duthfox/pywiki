#-*- coding:utf-8 -*-
from flask import json
from bson import json_util, ObjectId

def bson_to_json(data):
    return json.dumps(data, default=json_util.default)

def bson_obj_id(id):
    return ObjectId(id)

class AllowFile:
    IMG_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'bmp'])

    @classmethod
    def is_img(cls, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in cls.IMG_EXTENSIONS

class TypeRender:

    _template = '''
        <tr class="center aligned" data-type="{type}">
          <td>{name}</td>
          {content}
        </tr>
    '''

    _content = '<td class="attr {attr_cls}">{attr_content}</td>'

    _type = {
        'text': '{v}',
        'img': '<img src={v} width=200 height=150 />',
        'url': '<a href="{v}" target="_blank">{v}</a>',
        'num': '{v}',
        'star': '<div class="ui massive star rating">{v}</div>'
    }

    _star_tmp = '<i class="icon active"></i>'

    @classmethod
    def _content_of_type(cls, value, type):
        if type == 'star':
            attr_content = cls._type['star'].format(v=int(value) * cls._star_tmp)
        elif type == 'bool':
            if type is True or value == 1:
                attr_content = '是'
            else:
                attr_content = '否'
        else:
            attr_content = cls._type[type].format(v=value)
        content = cls._content.format(attr_cls=cls._class_of_type(value, type),\
                                      attr_content=attr_content)
        return content

    @classmethod
    def _class_of_type(cls,value, type):
        if type == 'bool':
            if type is True or value == 1:
                return 'positive'
            else:
                return 'negative'
        return ''

    @classmethod
    def render_html(cls, attr_name, attr_value, attr_type):
        content = cls._content_of_type(attr_value, attr_type)
        return cls.render(attr_name, content, attr_type)

    @classmethod
    def render_many(cls, attr_name, attr_list):
        td_arr = []
        for attr in attr_list:
            if not attr:
                td_arr.append(cls._content.format(attr_content='?', attr_cls=''))
            else:
                td_arr.append(cls._content_of_type(attr['attr_value'], attr['attr_type']))

        return cls.render(attr_name, ''.join(td_arr) )

    @classmethod
    def render(cls, name, content, type=None):
        return cls._template.format(name=name, content=content, type=type)
