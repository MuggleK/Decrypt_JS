import urllib
from copyheaders import headers_raw_to_dict
import execjs,time,requests,re,json,base64

# 获取nonce,pcid,publickey
def get_item():
    url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=MTUyMjMxNzcyMTk%3D&rsakt=mod&client=ssologin.js(v1.4.19)'
    res = requests.get(url=url)
    # print(res.text)
    item = {}
    item['pcid'] = json.loads(re.findall('(?<=\().*(?=\))',res.text)[0])['pcid']
    item['nonce'] = json.loads(re.findall('(?<=\().*(?=\))',res.text)[0])['nonce']
    item['pubkey'] = json.loads(re.findall('(?<=\().*(?=\))',res.text)[0])['pubkey']
    item['rsakv'] = json.loads(re.findall('(?<=\().*(?=\))',res.text)[0])['rsakv']
    item['servertime'] = json.loads(re.findall('(?<=\().*(?=\))',res.text)[0])['servertime']
    return item

def get_captcha():
    """验证码识别，Zok验证码识别工具"""
    url = 'https://login.sina.com.cn/cgi/pin.php?'
    downpicture = urllib.request.urlopen(url).read()
    local = open('captcha.png', 'wb')
    local.write(downpicture)
    local.close()

    with open('captcha.png', 'rb') as f_new:
        img = f_new.read()
    ret = requests.post('http://127.0.0.1:1000', data={"img": base64.b64encode(img)})
    print(ret.text)
    return re.findall('识别结果：(.*) ',ret.text)[0]
captcha = get_captcha()

item = get_item()
with open('weibo.js','r',encoding='utf8') as f:
    get_js = execjs.compile(f.read().replace('\xa0',''),cwd=r'C:\Users\MuggleK\node_modules')

timec_ = int(time.time())
_su = get_js.call('get_su',"15223177219")
_sp = get_js.call('get_sp',item['pubkey'],timec_,item['nonce'],"775847312..aa")
print(_su + '\n' + _sp)

def login():
    login_url = 'https://login.sina.com.cn/signup/signin.php?'
    form_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from':'',
        'savestate': '7',
        'qrcode_flag': 'false',
        'useticket': '1',
        'pagerefer':'',
        'wsseretry': 'servertime_error',
        'pcid': item['pcid'],
        'door': get_captcha(),
        'vsnf': '1',
        'su': _su,
        'service': 'miniblog',
        'servertime': item['servertime'],
        'nonce': item["nonce"],
        'pwencode': 'rsa2',
        'rsakv': item["rsakv"],
        'sp': _sp,
        'sr': '1920 * 1080',
        'encoding': 'UTF - 8',
        'cdult': '2',
        'domain': 'weibo.com',
        'prelt': '46',
        'returntype': 'TEXT'
    }
    headers = headers_raw_to_dict(b'''
    Accept: */*
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Content-Length: 613
    Content-Type: application/x-www-form-urlencoded
    Cookie: SINAGLOBAL=106.91.209.232_1579146295.789444; Apache=106.91.209.232_1579146295.789445; login=6ec7f45fe2ef20765c00bb7efc116593; U_TRS1=00000036.f4b94bb5.5e20083b.9d21c035; U_TRS2=00000036.f4c14bb5.5e20083b.39aa7d6d; ULOGIN_IMG=gz-4dbbdb6eda12f62d45b33c227fe2ad378491
    Host: login.sina.com.cn
    Origin: https://weibo.com
    Referer: https://weibo.com/login.php
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: cross-site
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
    ''')
    res = requests.post(url = login_url,data = form_data,headers = headers)
    print(res.status_code)

login()







