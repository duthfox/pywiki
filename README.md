
#pywiki

pywiki是基于Flask开发的一个wiki系统.


## 安装依赖
pip install -r requirement.txt
`
## 配置文件
app/config.py

## 运行
`
gunicorn wsgi:app -c gunicorn.conf

or
`
python manage.py
