import glob,os,cv2
import requests,json,time,execjs,random
from urllib import request
from PIL import Image

'''2020.9.18顶象ua现版本1632#,之前1553#的点选可以通过'''
'''问题1：算法在初始化时会调用多个函数，在其中检测浏览器环境，来加密形成ua和_ua；但最后对轨迹的加密算法未改变'''

'''问题2：在计算滑块距离时，结果为最左端到目标位置的距离。实际上提交为滑块到目标位置的距离，所以需在识别结果后的基础上-15px'''

class SlideCrack(object):
    def __init__(self, gap, bg, out):
        """
        init code
        :param gap: 缺口图片
        :param bg: 背景图片
        :param out: 输出图片
        """
        self.gap = gap
        self.bg = bg
        self.out = out

    @staticmethod
    def clear_white(img):
        # 清除图片的空白区域，这里主要清除滑块的空白
        img = cv2.imread(img)
        rows, cols, channel = img.shape
        min_x = 255
        min_y = 255
        max_x = 0
        max_y = 0
        for x in range(1, rows):
            for y in range(1, cols):
                t = set(img[x, y])
                if len(t) >= 2:
                    if x <= min_x:
                        min_x = x
                    elif x >= max_x:
                        max_x = x

                    if y <= min_y:
                        min_y = y
                    elif y >= max_y:
                        max_y = y
        img1 = img[min_x:max_x, min_y: max_y]
        return img1

    def template_match(self, tpl, target):
        th, tw = tpl.shape[:2]
        result = cv2.matchTemplate(target, tpl, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵(一维数组当作向量,用Mat定义) 中最小值和最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tw, tl[1] + th)
        # 绘制矩形边框，将匹配区域标注出来
        # target：目标图像
        # tl：矩形定点
        # br：矩形的宽高
        # (0,0,255)：矩形边框颜色
        # 1：矩形边框大小
        cv2.rectangle(target, tl, br, (0, 0, 255), 2)
        cv2.imwrite(self.out, target)
        return [tl[0], tl[1]]

    @staticmethod
    def image_edge_detection(img):
        edges = cv2.Canny(img, 100, 200)
        return edges

    def discern(self):
        img1 = self.clear_white(self.gap)
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        slide = self.image_edge_detection(img1)

        back = cv2.imread(self.bg, 0)
        back = self.image_edge_detection(back)

        slide_pic = cv2.cvtColor(slide, cv2.COLOR_GRAY2RGB)
        back_pic = cv2.cvtColor(back, cv2.COLOR_GRAY2RGB)
        x, y = self.template_match(slide_pic, back_pic)
        # 输出横坐标, 即 滑块在图片上的位置
        return [x, y]

def distance():
    # 滑块图片
    image1 = "p2.png"
    # 背景图片
    image2 = "p1.png"

    # 处理结果图片,用红线标注
    image3 = "p3.png"
    sc = SlideCrack(image1, image2, image3)
    return sc.discern()

def img_recover(lists):
    image_names = glob.glob('*.webp')
    for p in image_names:
        if 'p2' in p:
            img = cv2.imread(p)
            cv2.imwrite('p2_.png', img)
            image = Image.open('p2_.png')
            update_img = image.resize((50, 50))
            update_img.save('p2.png', quality=100)
            os.remove('p2_.png')
        else:
            img = cv2.imread(p)
            cv2.imwrite('p1_.png', img)
            img = Image.open('p1_.png')
            new_image = Image.new('RGB', (384, 200))
            for i in range(32):
                x = lists[i] * 12
                temp_img = img.crop((x, 0, x + 12, 200))
                new_image.paste(temp_img, (i * 12, 0, i * 12 + 12, 200))
            deform_img = new_image.resize((300, 150))
            deform_img.save('p1.png', quality=100)
            os.remove('p1_.png')
        os.remove(p)

def get_trace(point_,distance):
    '''轨迹'''
    i = 0
    i_list = []
    distance_1 = int(distance * 1/3 + random.randint(-5,5))  # 1/3处停顿
    distance_2 = int(distance * 1/3 + random.randint(-5,5))  # 2/3处停顿
    time_1 = random.randint(5,25)
    time_2 = random.randint(200,300)

    while i <= distance:
        x = random.randint(1,3)   # x像素偏移
        i += x
        i_list.append(i)

    x_list = [point_[0] + j for j in i_list]
    trance = []
    for ind in x_list:
        trance.append([ind,point_[1] + random.randint(-5,5),random.randint(5,25)])   # y像素偏移

    trance[distance_1][2] = random.randint(200,300)
    trance[distance_2][2] = random.randint(200,300)
    trance[-1][2] = random.randint(200,300)
    point_.append(time_1)
    trance.insert(0,point_)
    return trance


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

def Dx_slide(ak):
    time_ = int(time.time() * 1000)
    # 第一次请求，head头里需带Param，获取data
    sec_url = 'https://constid.dingxiang-inc.com/udid/c1?'

    with open(r'Param.js', 'r', encoding='utf8') as f_new:
        param = execjs.compile(f_new.read())
    headers['Param'] = param.call('get_Param')
    res1 = requests.get(url = sec_url,headers = headers)
    data1 = json.loads(res1.text)
    # print(data1)

    # 第二次请求 获取sid，滑块三组图片，坐标y(未知)
    first_url = f'https://cap.dingxiang-inc.com/api/a?w=300&h=150&s=50&ak={ak}&c={data1.get("data")}&jsv=1.3.75.612&aid=dx-{time_}-50472931-3&wp=1&de=0&uid=&lf=0&tpc=&_r=0.734449162883293'
    res2 = requests.get(url = first_url,headers = headers)
    data2 = json.loads(res2.text)
    # print(data2)

    # 还原图片 + 计算距离   网页大小300*150，实际返回图片大小400*200。0.75等比例缩放
    for i in ['p1', 'p2']:
        path = data2[i]
        request.urlretrieve('https://static.dingxiang-inc.com/picture' + path, i + '_' + path.rsplit('/', 1)[1])

    pic_id = data2.get('p1').split('/')[-1].split('.webp')[0]   # 缺口图id
    with open(r'slide.js', 'r', encoding='utf8') as f_new:
        ac = execjs.compile(f_new.read())
    pic_list = ac.call('img_array',pic_id)  # 唯一id缺口图对应一个图片还原数组
    img_recover(pic_list)
    x,y = distance()    # x为距离，y为纵向距离
    x = x - 15  # 大坑：识别出来的x坐标需再-15px才是真实距离。y坐标识别不准确，则使用上层即first_url返回的y参数

    '''滑块算法,通过率70%'''
    # with open('calAc.js','r',encoding='utf-8') as f:
    #     track_encrypt = execjs.compile(f.read())
    # final_trance = track_encrypt.call('generateTrace',x)

    '''自写算法,通过率50%'''
    # 初始坐标，可随机即滑块上任意点或拖动块上任意点
    ponit = [1410, 502]
    final_trance = get_trace(ponit,x)  # 这里提交的x可再加5-15来延长轨迹

    # 第三次请求
    item = ac.call('get_slide',data2.get('sid'),final_trance,x,data2.get('y'))
    # print(item)

    third_url = 'https://cap.dingxiang-inc.com/api/v1'
    param = {
        'ac':item['ua'],
        'ak': ak,
        'c': data1.get('data'),
        'jsv': '1.3.75.612',
        'sid': data2.get('sid'),
        'aid': 'dx-{}-42606613-2'.format(time_),
        'uid':'',
        'x': item['x'],
        'y': item['y']
    }
    res3 = requests.post(url = third_url,data = param,headers = headers).json()
    print(res3)

if __name__ == '__main__':
    ak = '99de95ad1f23597c23b3558d932ded3c'  # 站点ak
    Dx_slide(ak)