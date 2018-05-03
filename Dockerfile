FROM ubuntu:14.04
# 安装依赖
RUN apt-get update && --fix-missing && apt-get install -y build-essential python python-dev python-setuptools python-pip
RUN apt-get install -y git nginx supervisor mongodb redis-server
# 创建目录
RUN mkdir -p /var/log/gunicorn
RUN mkdir -p /data/db

# 复制项目
RUN mkdir -p /code/pkyx
WORKDIR /code/pkyx
COPY . /code/pkyx

# nginx配置
RUN ln -s /code/pkyx/conf/nginx.conf /etc/nginx/site-enabled

# supervisor配置
RUN service supervisor stop
RUN ln -s /code/pkyx/conf/supervisord.conf /etc/supervisor/conf.d/

# 安装python依赖
ADD requirements.txt /code/pkyx/requirements.txt
RUN pip install -r /code/pkyx/requirements.txt

# 暴露端口
EXPOSE 80

RUN chmod +x /code/pkyx/run_supervisor.sh
CMD /code/pkyx/run_supervisor.sh