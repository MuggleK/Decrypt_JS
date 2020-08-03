import json,requests,re,execjs
from copyheaders import headers_raw_to_dict
import warnings
from urllib import parse
warnings.filterwarnings("ignore")

session = requests.session()
headers = headers_raw_to_dict(b'''
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36
''')
# id 固定, 第一次请求，获取第一个token
first_url = 'https://c.dun.163.com/api/v2/getconf?id=07e2387ab53a4d6f930b8d9a9be71bdf&ipv6=false&runEnv=10&referer=https%3A%2F%2Fdun.163.com%2Ftrial%2Fpicture-click&type=3&loadVersion=2.2.0&callback=__JSONP_onpyxnv_2'
res1 = requests.get(url = first_url,headers = headers,verify = False)
data1 = json.loads(re.findall('(?<=\().*(?=\))',res1.text)[0])
_gid = res1.cookies.get_dict()
print(_gid)
print(data1)

# 第二次请求，解密fp，cb，获取font(待识别字符),bg(图片地址),第二个token和cookie值_ga
with open(r'.\fp_cb.js', 'r', encoding='utf8') as f_new:
    fp_cb = execjs.compile(f_new.read())
dict1 = fp_cb.call('get_fp_cb')

sec_url = 'https://c.dun.163.com/api/v2/get?id=07e2387ab53a4d6f930b8d9a9be71bdf&fp={}&https=true&type=3&version=2.14.0&dpr=1&dev=1&cb={}&ipv6=false&runEnv=10&group=&scene=&width=320&token=&referer=https%3A%2F%2Fdun.163.com%2Ftrial%2Fpicture-click&callback=__JSONP_l6szcf8_6'.format(dict1.get('fp'),dict1.get('cb'))
res2 = requests.get(url = sec_url,headers = headers,verify = False)
data2 = json.loads(re.findall('(?<=\().*(?=\))',res2.text)[0])
print(res2.cookies.get_dict())
print(data2)

# 第三个请求，请求参数：id(易盾分配网站id，固定),token:data2['token'], acToken:data1['token'], data(加密),cb:dict1['cb']
token = data2.get('data').get('token')
acToken = data1.get('data').get('ac').get('token')

bg_url = data2.get('data').get('bg')[0]
print(bg_url,data2.get('data').get('front'))    # 图片和待识别字符

points = [{'x':35,'y':36},{'x':42,'y':67},{'x':51,'y':21}]  # 点选坐标
print(token,points,acToken)

data = fp_cb.call('get_result',token,points)
cb_ = fp_cb.call('get_fp_cb').get('cb')

params = {
    'id': "07e2387ab53a4d6f930b8d9a9be71bdf",
    'token': token,
    'acToken': acToken,
    'data': data,
    'width': 320,
    'type': 3,
    'version': '2.14.0',
    'cb': cb_,
    'extraData': '',
    'runEnv': 10,
    'referer': 'https://dun.163.com/trial/picture-click',
    'callback': '__JSONP_bgmr0q5_9'
        }

third_url = 'https://c.dun.163.com/api/v2/check'
print(third_url)
headers['_gid'] = _gid.get('_gid')
headers['_ga'] = res2.cookies.get_dict().get('_ga')
# print(headers)
res3 = requests.get(url = third_url, params=params,headers = headers)
print(res3.text)

