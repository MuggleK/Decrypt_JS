from urllib import request
import requests,time,json,execjs,random,math
from urllib.parse import quote,unquote



class BaiduDegree:

    def __init__(self,ak,referer):
        self.ak = ak
        self.referer = referer
        self.start_time = int(time.time() * 1000)
        self.headers = {
            'Referer': self.referer,
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        self.session = requests.session()

    def get_trace(self,distance):
        '''轨迹'''
        start_point = [random.randint(45,50),random.randint(483,491),int(time.time() * 1000)]
        # end_point = [0,random.choice([random.randint(40,50),random.randint(100,115)]),random.randint(176,192),random.randint(532,792)]
        point_len = math.ceil(distance / 10)
        trace = []
        x_list = []
        time_list = []
        i = 0
        j = 0
        for n in range(point_len):
            x = random.randint(3, 7)  # x像素偏移
            i += x
            x_list.append(i)

            time_ = random.randint(123,221)   # 时间偏移
            j += time_
            time_list.append(j)

        for m in range(len(x_list)):
            points = {'fx':start_point[0]+x_list[m],'fy':start_point[1] + random.randint(-1,1),'t':start_point[2] + time_list[m]}   # y像素偏移
            trace.append(points)
        return trace

    def validate(self):
        log_url = f'https://wappass.baidu.com/viewlog?callback=jQuery110209384861307250785_{self.start_time}&ak={ak}&_={self.start_time + 1}'

        log_res = self.session.get(url = log_url,headers = self.headers).text
        res1 = json.loads(log_res.split('(')[1].split(')')[0])
        # print(res1)

        config_url = f'https://wappass.baidu.com/viewlog/getstyle?callback=jQuery110209384861307250785_{self.start_time + 5}&ak={ak}&tk={res1.get("tk")}&type=spin&_={self.start_time + 6}'
        config_res = self.session.get(url = config_url,headers = self.headers).text
        res2 = json.loads(config_res.split('(')[1].split(')')[0])
        # print(res2)

        img_url = unquote(res2.get('data').get('ext').get('img'))
        request.urlretrieve(img_url,'a.png')

        with open('./slide.js','r') as f:
            js_ = execjs.compile(f.read())
        
        degree = int(input('请输入旋转角度：'))
        distance = degree * 0.82   # 距离
        trace = self.get_trace(int(distance))
        percentage = format(degree / 360,'.2f') # 旋转角度/360，保留两位小数

        fs = js_.call('get_fs',trace,res2.get('data').get('backstr'),percentage,res1.get('data').get('as'))

        verify_url = f'https://wappass.baidu.com/viewlog?callback=jQuery110208207300409912506_{int(time.time() * 1000)}&ak={ak}&as={res1.get("data").get("as")}&fs={quote(fs)}&tk={quote(res1.get("data").get("tk"))}&cv=submit&_={int(time.time() * 1000)}'
        verify_res = self.session.get(url = verify_url,headers = self.headers).text
        result = json.loads(verify_res.split('(')[1].split(')')[0]).get('data')
        if result.get('op') == 1:
            print('验证成功')
            return result
        else:
            return None
if __name__ == '__main__':
    ak = '2ef521ec36290baed33d66de9b16f625'
    referer = 'https://wappass.baidu.com/static/captcha/tuxing.html?ak=2ef521ec36290baed33d66de9b16f625&backurl=http%3A%2F%2Ftieba.baidu.com%2Fp%2F4205446313%3Fpid%3D80375962508%26cid%3D0&timestamp=1604996082&signature=ba55ceeec0f9065f2bf990f05427ba61#80375962508'
    Bd = BaiduDegree(ak,referer)
    result = Bd.validate()
    print(result)
