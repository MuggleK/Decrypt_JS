import re,glob,os,cv2,base64,redis
import requests,json,time,execjs,random
from copyheaders import headers_raw_to_dict
from urllib import request
from PIL import Image

pool = redis.ConnectionPool(host='127.0.0.1', port=6379,db = 0,decode_responses = True)
r = redis.StrictRedis(connection_pool=pool)

start = time.time()

def img_recover():
    for o in glob.glob('*.webp'):
        img = cv2.imread(o)
        cv2.imwrite('a.png', img)

        img = Image.open('a.png')
        serilize = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12
            , 13, 23,22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        target = Image.new('RGB', (260, 160))
        for i in range(52):
            u = serilize[i] % 26 * 12
            c = 80 if 25 < serilize[i] else 0
            box = (u, c, u+10, c+80)
            region = img.crop(box)
            b = 80 if 25 < i else 0
            target.paste(region, (i % 26*10, b))
        target.save(os.path.splitext(o)[0] + '.png')
    # os.remove('a.png')


class SlideCrack(object):
    def __init__(self, gap_img, bg):
        self.gap_img = gap_img
        self.bg = bg

    @staticmethod
    def pixel_is_equal(image1, image2, x, y):
        """
        判断两张图片的像素是否相等,不想等即为缺口位置
        :param image1:
        :param image2:
        :param x:  x坐标
        :param y: y 坐标
        :return:
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60  # 像素色差
        if abs(pixel1[0]-pixel2[0]) < threshold and abs(pixel1[1]-pixel2[1]) < threshold and abs(pixel1[2]-pixel2[2]) <threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """
        获取缺口位置
        :param image1:完整图片
        :param image2: 带缺口的图片
        :return:
        """
        left = 50  # 设置一个起始量,因为验证码一般不可能在左边，加快识别速度
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.pixel_is_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def run(self):
        image1 = Image.open(self.bg)
        image2 = Image.open(self.gap_img)
        # 获取缺口的位置
        gap = self.get_gap(image1, image2)
        return gap


def get_distance():
    img1 = "gap.png"  # 带缺口的背景图
    img2 = "full.png"  # 不带缺口的背景图
    gt = SlideCrack(img1, img2)
    val = gt.run()
    os.remove('full.webp')
    # os.remove('full.png')
    os.remove('gap.webp')
    # os.remove('gap.png')
    return val

# distance_list = ['87', '140', '153', '76', '185', '119', '147', '187', '81', '63', '99', '133', '136', '131', '83','137', '159', '86', '91', '169', '109', '89', '114', '69', '154', '103', '127', '138', '189','115','176', '64', '148', '55', '142', '156', '38', '46', '130', '41', '146', '122', '145', '116', '163','177', '128', '155', '181', '186', '62', '170', '110', '72', '92', '65', '71', '93', '149', '112','171', '49', '126', '105', '84', '37', '135', '129', '82', '66', '54', '96', '125', '167', '117','94','53', '164', '78', '36', '45', '166', '73', '88', '79', '134', '50', '182', '56', '58', '168','150','57', '51', '74', '90', '179', '188', '173', '139', '183', '123', '40', '102', '52', '175', '151','101', '80', '98', '75', '39', '95', '61', '104', '85', '59', '161', '184', '111', '47', '60','165','172', '178', '121', '44', '174', '152', '43', '97', '113', '132', '68', '42', '118', '70', '157','144', '124', '141', '106', '77', '160', '190', '158', '100', '180', '48', '162', '120', '143','107','108', '67']

headers = headers_raw_to_dict(b'''
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
''')


conn = requests.Session()
# 获取 gt,challenge GeeTestUser
base_url = 'https://www.geetest.com/demo/gt/register-slide?t={}'.format(time.time()*1000)
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
# print(dict['aeskey'])

params1 = {'gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn', 'pt': 0, 'w': dict['first_w'], 'callback': 'geetest_%s' %timestamp}
resp2=conn.get(url='http://api.geetest.com/get.php', params=params1)
data_first = json.loads(resp2.text.split('(', 1)[-1].split(')')[0])
print(data_first)


# 解密第二个w，获取GeeTestAjaxUser，用于下次请求获取第二个字典
sec_w_ = first_w.call('sec_w',timestamp,data_first,dict['aeskey'])
# print(len(sec_w_))
params = {'gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn', 'pt': 0, 'w': sec_w_, 'callback': 'geetest_%s' % timestamp}
resp3 = conn.get(url='http://api.geetest.com/ajax.php', params=params)
print(resp3.text)
# print(resp3.cookies.get_dict())

# 获取第二个字典，其中包含固定数组c，s随机数，图片url。用于最终w解密
params3 = {'is_next': 'true','slide3': 'click','gt': data.get('gt'), 'challenge': data.get('challenge'), 'lang': 'zh-cn','https': 'true','protocol': 'https://','offline': 'false','product': 'embed','api_server': 'api.geetest.com','timeout': 5000,'isPC': 'true','width': '100%', 'callback': 'geetest_%s' %timestamp}
headers['Cookie'] = 'GeeTestUser={}; GeeTestAjaxUser={}'.format(cookie.get('GeeTestUser'),resp3.cookies.get_dict().get('GeeTestAjaxUser'))
resp4 = conn.get(url='https://api.geetest.com/get.php', params=params3,headers = headers)
# print(resp4.text)

'''注意：一共三次解密w，必须用到一个aeskey'''

data_sec = json.loads(resp4.text.split('(', 1)[-1].split(')')[0])
print(data_sec)

request.urlretrieve('https://static.geetest.com/' + data_sec["bg"],'gap.webp')
request.urlretrieve('https://static.geetest.com/' + data_sec["fullbg"],'full.webp')
img_recover()   # 还原图片
distance = get_distance() - 5   # 通过像素对比距离
'''redis随机取轨迹'''
slide_str = random.choice(r.lrange(distance,0,-1))
slide_list = []
for i in re.findall('\[(.*?)\]',re.findall('(?<=\[).*(?=\])',slide_str)[0]):
    data_ = i.split(',')
    items = [int(i) for i in data_]
    slide_list.append(items)
print('轨迹：{}'.format(slide_list))

passtime = slide_list[-1][-1]   # 每条轨迹的最后一个数组的最后一个元素为passtime
with open('slide.7.3.3.js', 'r', encoding='utf8') as f_new:
    final_w = execjs.compile(f_new.read())
final_w_ = final_w.call('slide_result',distance,slide_list,passtime,data_sec,dict.get('aeskey'))    # 这里提交的challenge会变，固直接提交整个字典

# print(len(final_w_))

# challenge改变，提交上层字典中的challenge
params_ = {'gt': data.get('gt'),'challenge': data_sec["challenge"],'lang': 'zh-cn','pt': '0','w': final_w_,'callback': 'geetest_' + str(int(time.time() * 1000))}
res5 = requests.get(url='https://api.geetest.com/ajax.php', params=params_,headers = headers)
# print(res5.status_code)
print(res5.text)

print(time.time() - start)

















