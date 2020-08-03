import execjs
import requests,re,json
import spider_tools as t

url = 'http://www.gsxt.gov.cn/index.html'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
# proxies = t.get_ip()

def first_request():
    conn = requests.Session()
    res = conn.get(url = url,headers = headers,verify = False)
    print(res.cookies.get_dict())
    print(res.text)
    cookie1 = res.cookies.get_dict()
    __jsl_clearance = get_clearance(res.text)
    print(__jsl_clearance)
    return conn,__jsl_clearance,cookie1

def get_clearance(html):
    if 'var x=' in html:
        print('other')
    else:
        print(html)
        data = json.loads(re.findall('go\((.*?)\)',html)[1])
        print(data)
        with open('__jsl_clearance.js', 'r', encoding='gbk') as f_new:
            get_js_ = execjs.compile(f_new.read().replace('\xa0', ''))
        res_ = ''
        if 'md5' in data.get('ha'):
            print('本次使用{}加密'.format(data.get('ha')))
            res_ = get_js_.call('go_md5', data)
        elif 'sha1' in data.get('ha'):
            print('本次使用{}加密'.format(data.get('ha')))
            res_ = get_js_.call('go_sha1', data)
        elif 'sha256' in data.get('ha'):
            print('本次使用{}加密'.format(data.get('ha')))
            res_ = get_js_.call('go_sha256', data)
        else:
            print('该算法还未解析')
        print(res_)
        return res_

def sec_request(conn,res_,cookie1):
    conn.cookies.set(name='__jsl_clearance',value=res_)
    conn.cookies.update(cookie1)
    print(conn.cookies.get_dict())
    print(conn.get(url=url, headers=headers).text)
    # print(conn.get(url=url, headers=headers).text)

# while True:
conn,cls,cookie = first_request()
sec_request(conn,cls,cookie)