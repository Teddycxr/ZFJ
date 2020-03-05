from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            # static_url_path='/666', 可以重写路径名
            static_folder='static',  # 表示静态文件存放的目录，默认值是 static
            template_folder='templates'  # 表示模板文件存放的目录
            )
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@127.0.0.1:3306/zfj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'vaxaxaxv^%$@(*'  # 用来加密我们存储的数据

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

db = SQLAlchemy(app)

from app.api import api as api_blueprint

app.register_blueprint(api_blueprint)