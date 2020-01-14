import hmac
from _sha1 import sha1
from urllib.parse import urlencode
from PIL import Image
from requests_html import HTMLSession   # 集成了requests和各种解析库
import execjs,time,json,base64,requests


session = HTMLSession()
#先获取cookie
session.get('https://www.zhihu.com/signin?next=%2F')


def __get_code():
    # 获取验证码类型
    res = session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en')
    print(res.text)
    show_captcha = res.json()['show_captcha']

    if show_captcha:
        # 获取验证的二进制
        res = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en')
        img_base64 = res.json().get('img_base64')
        img_content = base64.b64decode(img_base64)

        # 保存
        with open('captcha.png', 'wb') as f:
            f.write(img_content)

        # 手动处理验证码
        img_obj = Image.open('captcha.png')
        img_obj.show()
        captcha = input('输入验证码：')

        r = session.post(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en', data={'input_text': captcha})

        # 验证是否通过
        susssion_msg = r.json().get('success')

        if susssion_msg:
            print('验证通过')
        else:
            __get_code()
        return captcha

# 抠的signature，未成功
with open('signature.js','r',encoding='utf8') as f:
    get_js = execjs.compile(f.read().replace('\xa0',''))
    f.close()

signature = get_js.call('get_signature')
print('signature：{}'.format(signature))

#复写hamc算法
r = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=sha1)
r.update(b'password')
r.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
r.update(b'com.zhihu.web')
r.update(str(int(time.time() * 1000)).encode('utf-8'))
signature_new = r.hexdigest()
print('signature_new：{}'.format(signature_new))

login_form_data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'timestamp': str(int(time.time() * 1000)),
            'source': 'com.zhihu.web',
            'signature': signature_new,
            'username': '17723842238',
            'password': '111111',
            'captcha': __get_code(),
            'lang': 'en',
            'utm_source': '',
            'ref_source': 'other_https://www.zhihu.com/signin?next=%2F'
        }

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'x-zse-83':'3_2.0',
            'content-type':'application/x-www-form-urlencoded',
        }

# 调用最外层加密算法
with open('知乎.js', 'r', encoding='utf8') as f_new:
    get_js_ = execjs.compile(f_new.read().replace('\xa0', ''))
    # f.close()
#js代码中是  return __g._encrypt(encodeURIComponent(e)) ,所有我们要对login_form_data进行url编码
res = get_js_.call('b',urlencode(login_form_data))
print(urlencode(login_form_data))
print(res)
r = session.post(url='https://www.zhihu.com/api/v3/oauth/sign_in',data=res,headers=headers)
print(json.loads(r.text))


#参考 ：'https://gitee.com/pythonywy/ZhiHu'；https://www.jianshu.com/p/e5be52363bad