from flask import Flask
from datetime import timedelta
from flask_mail import Mail
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            # static_url_path='/666', 可以重写路径名
            static_folder='static',  # 表示静态文件存放的目录，默认值是 static
            template_folder='templates'  # 表示模板文件存放的目录
            )
app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://elastos:workwork@192.168.1.5:3306/dab'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = 'vaxaxaxv^%$@(*'  # 用来加密我们存储的数据

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_USERNAME'] = '735652082@qq.com'
app.config['MAIL_PASSWORD'] = 'jahysoqfbtvpbbfc'

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST']= '127.0.0.1'
app.config['CACHE_REDIS_PORT']= 6379
app.config['CACHE_REDIS_DB']= 0
app.config['CACHE_REDIS_PASSWORD'] = ''

mail = Mail(app)
cache = Cache(app,with_jinja2_ext=False)
db = SQLAlchemy(app)

from app.api import api as api_blueprint

app.register_blueprint(api_blueprint)
