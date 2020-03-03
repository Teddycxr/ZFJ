@api.route('/sendmail/', methods=['POST'])
def send_mail():
    if request.method == 'POST':
        temp = request.json.get('data')

        data = temp['text']
        title = temp['title']
        receiver = temp['receiver']

        send_report_mail(data, title, receiver)

        requests.get('http://39.105.68.35/exchange/status/record_report_mail/ok/')

    return 'ok'


# 检查交易文件
@api.route("/stats/", methods=["GET", "POST"])
def check_txn():
    return redirect('http://39.105.68.35/exchange/stats')


@api.route('/api/sendcode', methods=['POST'])
def sendcode():
    if request.method == 'POST':
        temp = request.json.get('data')
        _email = temp['email']

        message = 'ok'
        success = True

        # 生成验证码
        _sendcode = ""
        for i in range(6):
            a = random.randint(0, 9)
            _sendcode += str(a)

        data = "<h3>注册验证码：</h3>" + _sendcode

        try:
            send_report_mail(data, '安全验证', _email)
            cache.set(_email, _sendcode, 300)
        except Exception as e:
            message = e
            success = False

        return {"success": success, "message": message}


@api.route('/api/validatecode', methods=['POST'])
def validatecode():
    if request.method == 'POST':
        temp = request.json.get('data')
        _email = temp['email']
        _captcha = temp['code']
        captcha_cache = cache.get(_email)

        success = True
        if not captcha_cache or _captcha != captcha_cache:
            success = False

        return {"success": success}


@api.route("/api/register", methods=["POST"])
def register():
    if request.method == 'POST':
        temp = request.json.get('data')
        _email = temp['email']
        _password = temp['password']
        _captcha = temp['code']
        captcha_cache = cache.get(_email)
        print(_email, _captcha, _password, captcha_cache)

        success = True
        if not captcha_cache or _captcha != captcha_cache:
            success = False
        else:
            user = _email
            pwd = generate_password_hash(_password)

            _uid = "66"
            for i in range(6):
                a = random.randint(0, 9)
                _uid += str(a)

            user = User(
                uid=_uid,
                name=user,
                email=_email,
                pwd=pwd,
            )
            db.session.add(user)
            db.session.commit()

        return {"success": success, "userinfo": {'uid': _uid, 'username': _email}}


@api.route("/api/dologin", methods=["POST"])
def dologin():
    if request.method == 'POST':
        temp = request.json.get('data')
        _email = temp['username']
        _password = temp['password']

        user = User.query.filter_by(name=_email).first()

        success = True
        message = ''
        if not user:
            success = False
            message = '用户不存在'

        if not user.check_pwd(_password):
            success = False
            message = '密码错误'

        return {"success": success, "message": message, "userinfo": {"uid": user.uid, "username": user.email}}


@api.route("/api/swft/coinlist", methods=["GET", "POST"])
def swft_coinlist():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "supportType": "advanced",
        "cache-control": "no-cache",
    }

    url = 'https://transfer.swft.pro/api/v1/queryCoinList'

    try:
        response = requests.post(url, headers=headers)
        return response.json()
    except Exception as e:
        return {'code': False, 'message': e}


@api.route("/api/swft/baseinfo/<dcoin>/<rcoin>", methods=["GET", "POST"])
def swft_baseinfo(dcoin=None, rcoin=None):
    data = {
        "depositCoinCode": dcoin,
        "receiveCoinCode": rcoin
    }

    headers = {
        'Content-Type': 'application/json',
        "cache-control": "no-cache",
    }

    url = 'https://transfer.swft.pro/api/v1/getBaseInfo'

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {'code': False, 'message': e}


@api.route("/api/swft/order", methods=["GET", "POST"])
def swft_create_order():
    if request.method == 'POST':
        temp = request.json.get('data')
        _equipmentNo = temp['equipmentNo']
        _sourceType = temp['sourceType']
        _depositCoinCode = temp['depositCoinCode']
        _receiveCoinCode = temp['receiveCoinCode']
        _depositCoinAmt = temp['depositCoinAmt']
        _destinationAddr = temp['destinationAddr']
        _refundAddr = temp['refundAddr']

        data = {
            "equipmentNo": _equipmentNo,
            "sourceType": _sourceType,
            "depositCoinCode": _depositCoinCode,
            "receiveCoinCode": _receiveCoinCode,
            "depositCoinAmt": _depositCoinAmt,
            "receiveCoinAmt": '1',
            "receiveSwftAmt": '1',
            "destinationAddr": _destinationAddr,
            "refundAddr": _refundAddr
        }

        headers = {
            'Content-Type': 'application/json',
            "cache-control": "no-cache",
        }

        url = 'https://transfer.swft.pro/api/v2/accountExchange'

        try:
            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            return response.json()
        except Exception as e:
            return e


@api.route("/api/swft/orderinfo", methods=["GET", "POST"])
def swft_get_orderinfo():
    if request.method == 'POST':
        temp = request.json.get('data')
        _equipmentNo = temp['equipmentNo']
        _sourceType = temp['sourceType']
        _orderid = temp['orderId']

        data = {
            "equipmentNo": _equipmentNo,
            "sourceType": _sourceType,
            "orderId": _orderid
        }

        headers = {
            'Content-Type': 'application/json',
            "cache-control": "no-cache",
        }

        url = 'https://transfer.swft.pro/api/v2/queryOrderState'

        try:
            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            return response.json()
        except Exception as e:
            return e

@api.route("/api/invest", methods=["GET", "POST"])
def get_invest():

    user = Invest.query.filter_by().all()

    invest_list = []
    for i in user:
        invest_list.append({'id':i.id,'name':i.name,'wait_time':i.wait_time,'time':i.time,'sdate':i.sdate,
                            'edate':i.sdate,'get_num':i.get_num,'total_num':i.total_num,'rate':i.rate,'info':i.info,'addr':i.addr})

    return invest_list