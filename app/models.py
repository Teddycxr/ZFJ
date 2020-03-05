# -*- coding: UTF-8 -*-
from datetime import datetime

from app import db


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    info = db.Column(db.String(1500))
    sender_name = db.Column(db.String(255))
    sender_url = db.Column(db.String(1000))
    admin_address = db.Column(db.String(100))
    admin_pubkey = db.Column(db.String(255))
    verifier_address = db.Column(db.String(1000))
    verifier_pubkey = db.Column(db.String(1000))
    point_token_symbol = db.Column(db.String(255))
    point_token_num = db.Column(db.String(20))
    reward_token_symbol = db.Column(db.String(100))
    reward_token_num = db.Column(db.String(20))
    exchange_time = db.Column(db.String(100))
    budget = db.Column(db.String(20))
    rate = db.Column(db.String(30))
    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))
    contract = db.Column(db.String(255))

    addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def to_full_dict(self):
        """将详细信息转换为字典数据"""
        project_dict = {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "sender_name": self.sender_name,
            "sender_url": self.sender_url,
            "admin_address": self.admin_address,
            "admin_pubkey": self.admin_pubkey,
            "verifier_address": self.verifier_address.split(","),
            "verifier_pubkey": self.verifier_pubkey.split(","),
            "point_token_symbol": self.point_token_symbol,
            "point_token_num": self.point_token_num,
            "reward_token_symbol": self.reward_token_symbol,
            "reward_token_num": self.reward_token_num,
            "exchange_time":self.exchange_time,
            "budget": self.budget,
            "rate": self.rate,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "contract": self.contract,
        }

        return project_dict

    def __repr__(self):
        return 'Project:%s' % self.name


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(10))
    project_name = db.Column(db.String(255))
    contributer_wallet = db.Column(db.String(255))
    contributer_info = db.Column(db.String(400))
    submit_time = db.Column(db.String(30))
    task_info = db.Column(db.String(1000))
    files = db.Column(db.String(1000))
    verifier_pubkey = db.Column(db.String(1000))
    verifier_wallet = db.Column(db.String(1000))
    verifier_sign = db.Column(db.String(1000))
    status = db.Column(db.String(20))
    tx_hash = db.Column(db.String(100))
    tx_time = db.Column(db.String(30))
    tx_token_num = db.Column(db.String(20))

    addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def to_full_dict(self):
        """将详细信息转换为字典数据"""
        task_dict = {
            "id": self.id,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "contributer_wallet": self.contributer_wallet,
            "contributer_info": self.contributer_info,
            "submit_time": self.submit_time,
            "task_info": self.task_info,
            "files": self.files.split(","),
            "verifier_pubkey": self.verifier_pubkey.split(","),
            "verifier_wallet": self.verifier_pubkey.split(","),
            "verifier_sign": self.verifier_sign.split(","),
            "status": self.status,
            "tx_hash": self.tx_hash,
            "tx_time": self.tx_time,
            "tx_token_num": self.tx_token_num,
        }

        return task_dict

    def __repr__(self):
        return 'Task:%s' % self.name
