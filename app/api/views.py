# -*- coding: utf-8 -*-
from flask import request, redirect
from werkzeug.security import generate_password_hash

from . import api
from app import cache, db
from app.models import User

import requests
import random


@api.route("/", methods=["GET"])
def Hello_World():

    return "Hello World"

@api.route("/get_ticker/<symbol>", methods=["GET"])
def get_ticker(symbol=None):
    url = "https://api.huobi.pro/market/detail/merged?symbol=" + symbol
    res = requests.get(url=url).json()
    price = res['tick']['close']

    return {symbol: price}