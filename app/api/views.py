# -*- coding: utf-8 -*-
from flask import request
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from . import api
from app import db
from app.models import Project, Task,Token_addr
from flask import jsonify

import hashlib
import time

@api.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


@api.route("/", methods=["GET"])
def Hello_World():
    return "Hello World"


def deal_multi_data(data):
    a = ""
    for i in data:
        a = a + i + ","

    return a


@api.route("/project", methods=["POST"])
def save_project():
    temp = request.json
    print('temp:', temp)

    id = temp.get('contract')
    name = temp.get('name')
    info = temp.get('info')
    sender_name = temp.get('sender_name')
    sender_url = temp.get('sender_url')
    admin_address = temp.get('admin_address')
    admin_pubkey = temp.get('admin_pubkey')
    verifier_address = temp.get('verifier_address')
    verifier_pubkey = temp.get('verifier_pubkey')
    point_token_symbol = temp.get('point_token_symbol')
    point_token_num = temp.get('point_token_num')
    reward_token_symbol = temp.get('reward_token_symbol')
    reward_token_num = temp.get('reward_token_num')
    exchange_time = temp.get('exchange_time')
    budget = temp.get('budget')
    rate = temp.get('rate')
    start_date = temp.get('start_date')
    end_date = temp.get('end_date')
    contract = temp.get('contract')

    # 校验参数
    if len(temp.keys()) != 18:
        return jsonify(msg="参数不完整")

    # 判断project_id是否存在
    pro = Project.query.get(id)
    if pro:
        return jsonify(msg="该项目ID已存在")

    if not isinstance(verifier_address, list) or not isinstance(verifier_pubkey, list):
        return jsonify(msg="验证人地址或验证人公钥参数格式错误")

    project = Project(
        id=id,
        name=name,
        info=info,
        sender_name=sender_name,
        sender_url=sender_url,
        admin_address=admin_address,
        admin_pubkey=admin_pubkey,
        verifier_address=deal_multi_data(verifier_address),
        verifier_pubkey=deal_multi_data(verifier_pubkey),
        point_token_symbol=point_token_symbol,
        point_token_num=point_token_num,
        reward_token_symbol=reward_token_symbol,
        reward_token_num=reward_token_num,
        exchange_time=exchange_time,
        budget=budget,
        rate=rate,
        start_date=start_date,
        end_date=end_date,
        contract=contract,
    )

    try:
        db.session.add(project)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg="保存数据失败")

    return jsonify(msg="OK", data={"project_id": contract})


@api.route("/project/search", methods=["POST"])
def search_project():
    temp = request.json

    try:
        _Key = temp.get('Key')
        _PageSize = int(temp.get('PageSize'))
        _PageNumber = int(temp.get('PageNumber'))
        _Order = temp.get('Order')
    except Exception as e:
        return jsonify(msg="参数错误" + str(e))

    # 校验参数
    if len(temp.keys()) != 4:
        return jsonify(msg="参数不完整")
    if not _PageSize:
        _PageSize = 1

    if not _Key:
        # 检查页数参数
        _pages = Project.query.paginate(page=1, per_page=_PageSize).pages
        if _pages < _PageNumber:
            _PageNumber = _pages
        if not _PageNumber:
            _PageNumber = 1

        if _Order == "DESC":
            data = Project.query.order_by(
                Project.addtime.desc()
            ).paginate(page=_PageNumber, per_page=_PageSize)
        else:
            data = Project.query.order_by(
                Project.addtime
            ).paginate(page=_PageNumber, per_page=_PageSize)
    else:
        # 检查页数参数
        _data = Project.query.filter(
            or_(Project.id == _Key, Project.name == _Key, Project.sender_name == _Key,
                Project.admin_address == _Key, Project.verifier_address == _Key),
        )
        _pages = _data.paginate(page=1, per_page=_PageSize).pages
        if _pages < _PageNumber:
            _PageNumber = _pages
        if not _PageNumber:
            _PageNumber = 1

        if _Order == "DESC":
            data = _data.order_by(
                Project.addtime.desc()
            ).paginate(page=_PageNumber, per_page=_PageSize)
        else:
            data = _data.order_by(
                Project.addtime
            ).paginate(page=_PageNumber, per_page=_PageSize)

    # 将查询到的房屋信息转换为字典存放到列表中
    project_list = []
    if data:
        for project in data.items:
            project_list.append(project.to_full_dict())

    return jsonify(msg="OK", data={"project": project_list})


@api.route("/task", methods=["POST"])
def save_task():
    temp = request.form

    id = temp.get('id')
    project_id = temp.get('project_id')
    project_name = temp.get('project_name')
    contributer_wallet = temp.get('contributer_wallet')
    contributer_info = temp.get('contributer_info')
    submit_time = temp.get('submit_time')
    task_info = temp.get('task_info')
    # files = temp.get('files')
    verifier_pubkey = temp.get('verifier_pubkey')
    verifier_wallet = temp.get('verifier_wallet')
    verifier_sign = temp.get('verifier_sign')
    status = temp.get('status')
    tx_hash = temp.get('tx_hash')
    tx_time = temp.get('tx_time')
    tx_token_num = temp.get('tx_token_num')

    # 校验参数
    if len(temp) != 14:
        return jsonify(msg="参数不完整")

    # 判断task_id是否存在
    ta = Task.query.get(id)
    if ta:
        return jsonify(msg="该Task_ID已存在")

    # 接收文件
    file_list = []
    for f in request.files:
        _f = request.files[f]
        _file = 'app/static/' + secure_filename(_f.filename)
        _f.save(_file)

        file_list.append(_f.filename)

    task = Task(
        id=id,
        project_id=project_id,
        project_name=project_name,
        contributer_wallet=contributer_wallet,
        contributer_info=contributer_info,
        submit_time=submit_time,
        task_info=task_info,
        files=deal_multi_data(file_list),
        verifier_pubkey=verifier_pubkey,
        verifier_wallet=verifier_wallet,
        verifier_sign=verifier_sign,
        status=status,
        tx_hash=tx_hash,
        tx_time=tx_time,
        tx_token_num=tx_token_num,
    )

    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg="保存数据失败")

    return jsonify(msg="OK", data={"task_id": id})


@api.route("/task/search", methods=["POST"])
def search_task():
    temp = request.json

    try:
        _Key = temp.get('Key')
        _PageSize = int(temp.get('PageSize'))
        _PageNumber = int(temp.get('PageNumber'))
        _Order = temp.get('Order')
    except Exception as e:
        return jsonify(msg="参数错误" + str(e))

    # 校验参数
    if len(temp.keys()) != 4:
        return jsonify(msg="参数不完整")
    if not _PageSize:
        _PageSize = 1

    if not _Key:
        # 检查页数参数
        _pages = Task.query.paginate(page=1, per_page=_PageSize).pages
        if _pages < _PageNumber:
            _PageNumber = _pages
        if not _PageNumber:
            _PageNumber = 1

        if _Order == "DESC":
            data = Task.query.order_by(
                Task.addtime.desc()
            ).paginate(page=_PageNumber, per_page=_PageSize)
        else:
            data = Task.query.order_by(
                Task.addtime
            ).paginate(page=_PageNumber, per_page=_PageSize)
    else:
        # 检查页数参数
        _data = Task.query.filter(
            or_(Task.id == _Key, Task.contributer_wallet == _Key, Task.project_id == _Key,
                Task.project_name == _Key),
        )
        _pages = _data.paginate(page=1, per_page=_PageSize).pages
        if _pages < _PageNumber:
            _PageNumber = _pages
        if not _PageNumber:
            _PageNumber = 1

        if _Order == "DESC":
            data = _data.order_by(
                Task.addtime.desc()
            ).paginate(page=_PageNumber, per_page=_PageSize)
        else:
            data = _data.order_by(
                Task.addtime
            ).paginate(page=_PageNumber, per_page=_PageSize)

    # 将查询到的信息转换为字典存放到列表中
    task_list = []
    if data:
        for t in data.items:
            task_list.append(t.to_full_dict())

    return jsonify(msg="OK", data={"task": task_list})


@api.route("/task/sign", methods=["POST"])
def sign_task():
    temp = request.json

    try:
        _id = temp.get('id')
        _verifier_pubkey = temp.get('verifier_pubkey')
        _verifier_wallet = temp.get('verifier_wallet')
        _verifier_sign = temp.get('verifier_sign')
    except Exception as e:
        return jsonify(msg="参数错误" + str(e))

    # 校验参数
    if len(temp.keys()) != 4:
        return jsonify(msg="参数不完整")

    # 判断task_id是否存在
    ta = Task.query.get(_id)
    if not ta:
        return jsonify(msg="该Task_ID不存在")

    task = Task.query.get_or_404(_id)
    task.verifier_sign = deal_multi_data(_verifier_sign)
    task.verifier_pubkey = deal_multi_data(_verifier_pubkey)
    task.verifier_wallet = deal_multi_data(_verifier_wallet)

    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(msg="失败")

    return jsonify(msg="成功")


@api.route("/hook", methods=["POST"])
def get_hook_msg():
    content = request.json

    rep = content['repository']['name']
    add_content = content['head_commit']['message'].split("\n")

    _add = ""
    for i in add_content:
        _i = i.replace(" ",'')
        if "@" in _i and len(_i) == 43:
            _add = _i[1:]

    if _add:
        id = hashlib.md5(str((rep,_add,time.time())).encode('utf-8')).hexdigest()
        token = Token_addr(
            id = id,
            rep=rep,
            addr = _add,
        )

        try:
            db.session.add(token)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(msg="保存数据失败")

    return "hello world"

@api.route("/hook/search", methods=["GET","POST"])
def search_hook():
    temp = request.json

    try:
        _Key = temp.get('Key')
    except Exception as e:
        return jsonify(msg="参数错误" + str(e))


    if not _Key:
        _data = Token_addr.query.order_by(
            Token_addr.addtime
        ).all()

    if _Key:
        _data = Token_addr.query.filter(
            or_(Token_addr.rep == _Key, Token_addr.addr == _Key)
        ).order_by(
            Token_addr.addtime
        ).all()

    # 将信息转换为字典存放到列表中
    token_list = []
    if _data:
        for t in _data.items:
            token_list.append(t.to_full_dict())

    return jsonify(msg="OK", data={"token_addr": token_list})