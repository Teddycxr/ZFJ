# -*- coding: UTF-8 -*-
from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64))
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    pwd = db.Column(db.String(200))
    addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def __repr__(self):
        return 'User:%s' % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)
