# -*- coding: utf-8 -*-
import hmac


def ss(x):
    ii = {
        "n": 20,
        "codes": {
            "0": "W",
            "1": "l",
            "2": "k",
            "3": "B",
            "4": "Q",
            "5": "g",
            "6": "f",
            "7": "i",
            "8": "i",
            "9": "r",
            "10": "v",
            "11": "6",
            "12": "A",
            "13": "K",
            "14": "N",
            "15": "k",
            "16": "4",
            "17": "L",
            "18": "1",
            "19": "8"
        }
    }
    e = x.lower()
    a = e + e
    n = ''
    for jj in a:
        o = str(ord(jj) % ii['n'])
        n += ii['codes'][o]
    return n


def hmac_encrypt(key, msg):
    m = hmac.new(key.encode('utf-8'), msg.encode('utf-8'), digestmod='sha512')
    return str(m.hexdigest())


def header_key(x):
    """
    Encrypt Cookie key
    :param x: 
    :return: 
    """
    s = ss(x)
    i = hmac_encrypt(s, x)
    return i.lower()[10:30]


def header_value(x, y="{}"):
    """
    Encrypt Cookie value
    :param x: 
    :param y: Post Data
    :return: 
    """
    s = ss(x)
    i = hmac_encrypt(s, x + x + y)
    return i
