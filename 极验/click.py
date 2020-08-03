import requests,json,time,execjs,random
from copyheaders import headers_raw_to_dict
import spider_tools as t
import base64

start = time.time()

def get_cc(url):
    captcha = requests.get(url).content
    with open('1.jpg','wb')as f:
        f.write(captcha)
    image = base64.b64encode(captcha).decode()
    res = requests.post(url='http://handi.datasup.cn:5000/captcha', data=json.dumps({'img': image}))
    data = res.json().get('data')
    print(f'极验文字点选识别结果： {data}')
    points = [str(int(round(v.get('x') / 344 * 10000, 0))) + '_' + str(
        int(round(v.get('y') / 344 * 10000, 0))) for v in data.values()]
    points = ','.join(points)
    return points


headers = headers_raw_to_dict(b'''
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
''')
conn = requests.Session()

# 获取 gt,challenge GeeTestUser
base_url = 'https://www.geetest.com/demo/gt/register-click?t={}'.format(time.time()*1000)
data = json.loads(conn.get(url = base_url,headers = headers).text)
sec_url = 'https://api.geetest.com/gettype.php?gt={}&callback=geetest_{}'.format(data.get('gt'),time.time()*1000)
cookie = conn.get(url = sec_url,headers = headers).cookies.get_dict()
print(data)
# # print(cookie)

timestamp = int(time.time()*1000)
with open('first_w.js', 'r', encoding='utf8') as f_new:
    first_w = execjs.compile(f_new.read())

# 解密第一个w，获取第一个字典，其中包含固定数组c和s随机数，下一个解密需要用到
dict = first_w.call('first_w',data.get('gt'),data.get('challenge'),timestamp)   # 这里将aeskey和first_w存与一个字典。以便后期直接使用

params1 = {'gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn', 'pt': 0, 'w': dict['first_w'], 'callback': 'geetest_%s' %timestamp}
resp2=conn.get(url='http://api.geetest.com/get.php', params=params1)
data_first = json.loads(resp2.text.split('(', 1)[-1].split(')')[0])
print(data_first)


# 解密第二个w，获取GeeTestAjaxUser，用于下次请求获取第二个字典
sec_w_ = first_w.call('sec_w',timestamp,data_first,dict['aeskey'])
# print(len(sec_w_))
params = {'gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn', 'pt': 0, 'w': sec_w_, 'callback': 'geetest_%s' % timestamp}
resp3 = requests.get(url='http://api.geetest.com/ajax.php', params=params)
print(resp3.text)
# print(resp3.cookies.get_dict())

# 获取第二个字典，其中包含固定数组c，s随机数，图片url。用于最终w解密
params3 = {'is_next': 'true','type': 'click','gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn','https': 'true','protocol': 'https://','offline': 'false','product': 'embed','api_server': 'api.geetest.com','timeout': 5000,'isPC': 'true','width': '100%', 'callback': 'geetest_%s' %timestamp}
headers['Cookie'] = 'GeeTestUser={}; GeeTestAjaxUser={}'.format(cookie.get('GeeTestUser'),resp3.cookies.get_dict().get('GeeTestAjaxUser'))
resp4 = requests.get(url='https://api.geetest.com/get.php', params=params3,headers = headers)
# print(resp4.text)

'''注意：一共三次解密w，必须用到一个aeskey'''

# 最后w，提交点选字符坐标*32，通过时间，pic，c，s等

data_sec = json.loads(resp4.text.split('(', 1)[-1].split(')')[0]).get('data')
pic = data_sec.get('pic')
url_pic = 'https://static.geetest.com{}'.format(pic)
points = get_cc(url_pic)    # 获取坐标
c = data_sec.get('c')
s = data_sec.get('s')

# start_time = int(time.time()*1000)
# x_y = input('坐标:')
# end_time = int(time.time()*1000)

# passtime = end_time - start_time
# print(x_y,passtime)
with open('click.2.9.2_check.js', 'r', encoding='utf8') as f_new:
    final_w = execjs.compile(f_new.read())
time.sleep(1)
final_w_ = final_w.call('get_w',points,'0',pic,c,s,data.get('gt'),data.get('challenge'),dict.get('aeskey'))
print(final_w_)
# print(headers)

params_ = {'gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn', 'pt': 0, 'w': final_w_, 'callback': 'geetest_%s' % timestamp}
# headers['Cookie'] = 'GeeTestUser={}; GeeTestAjaxUser={}'.format(cookie.get('GeeTestUser'),resp3.cookies.get_dict().get('GeeTestAjaxUser'))
res5 = requests.get(url='https://api.geetest.com/ajax.php', params=params_,headers = headers)
# print(res5.status_code)
# print(res5.text)

# validate 值验证
final_data = json.loads(res5.text.split('(', 1)[-1].split(')')[0]).get('data')
print(final_data)
print(time.time() - start)
# final_params = {'geetest_challenge':data.get('challenge'),'geetest_validate':final_data.get('validate'),'geetest_seccode':final_data.get('validate') + "|jordan"}
#
# resp_final = conn.post(url='https://www.geetest.com/demo/gt/validate-click', params=final_params,headers = headers)
# print(resp_final.text)















