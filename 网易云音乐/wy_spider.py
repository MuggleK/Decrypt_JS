import pymongo,time
from lxml import etree
from copyheaders import headers_raw_to_dict
import random,requests,os,json,re
from binascii import hexlify
from Crypto.Cipher import AES
import base64


class ProxyMiddleware(object):
    '''
    设置Proxy
    '''

    def __init__(self):
        url_daili = 'http://elements.v4.dailiyun.com/query.txt?key=NP469FF1DE&word=&count=80&rand=true&detail=false'
        res = requests.get(url_daili)
        result = res.text
        ip_list = result.split('\r\n')
        print(ip_list)
        self.ip = ip_list
        self.start = time.time()
        #
        # self.ip = ['134.175.187.209:8089', '118.89.44.219:8089', '140.143.140.196:8089', '140.143.33.121:8089',
        #            '129.28.68.157:8089',
        #            '132.232.45.158:8089', '94.191.9.189:8089', '94.191.4.160:8089', '115.159.209.40:8089',
        #            '118.89.156.161:8089',
        #            '106.12.192.6:8089', '106.12.203.241:8089', '106.12.88.84:8089', '182.61.58.206:8089',
        #            '106.12.120.235:8089',
        #            '106.12.192.251:8089', '106.12.10.251:8089', '106.12.85.4:8089', '182.61.22.107:8089',
        #            '182.61.30.128:8089',
        #            '106.12.199.35:8089', '106.12.199.151:8089', '106.12.199.161:8089', '106.12.128.78:8089',
        #            '106.12.128.102:8089',
        #            '106.12.31.86:8089', '106.12.83.54:8089', '106.12.133.155:8089', '106.12.128.176:8089',
        #            '106.12.89.102:8089',
        #            '106.12.199.170:8089', '106.12.128.179:8089', '106.12.133.218:8089', '106.12.133.222:8089',
        #            '106.12.199.214:8089',
        #            '106.12.134.168:8089', '106.12.134.175:8089', '106.12.85.211:8089', '106.12.133.224:8089',
        #            '106.12.101.33:8089',
        #            '106.12.210.101:8089', '106.12.202.115:8089', '106.12.101.239:8089', '106.12.89.250:8089',
        #            '106.12.90.57:8089',
        #            '182.61.27.83:8089', '106.12.204.18:8089', '106.12.90.3:8089', '182.61.49.100:8089',
        #            '106.12.204.65:8089',
        #            '182.61.30.168:8089', '106.12.199.181:8089', '106.12.8.69:8089', '106.12.199.193:8089',
        #            '106.12.128.100:8089',
        #            '106.12.128.202:8089']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip=crawler.settings.get('PROXIES'))

    def process_request(self):
        if time.time() - self.start>180 or not self.ip:
            url_daili = 'http://elements.v4.dailiyun.com/query.txt?key=NP469FF1DE&word=&count=80&rand=true&detail=false'
            res = requests.get(url_daili)
            result = res.text
            ip_list = result.split('\r\n')
            print(ip_list)
            self.ip = ip_list
            self.start = time.time()

        ip = random.choice(self.ip)
        print("正在使用的代理IP为", ip)
        proxy = 'http://elements:Elements-123.@' + ip +'/'
        return ip
        # request.meta['proxy'] = 'http://' + ip +'/'

headers = headers_raw_to_dict(b'''
        authority: music.163.com
        method: GET
        path: /playlist?id=3067940465
        scheme: https
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
        accept-encoding: gzip, deflate, br
        accept-language: zh-CN,zh;q=0.9
        cookie: _iuqxldmzr_=32; _ntes_nnid=40628453377a692b79b9949c973a3a6e,1576029829667; _ntes_nuid=40628453377a692b79b9949c973a3a6e; WM_TID=A3Ka4Jz7gDBFEFVBVEcs%2Fb3dQue9MekO; WM_NI=veQvE%2B%2BRC%2FX63UaCZ5o%2FJWtCRu6LExMEfI72EIb6Wz%2BZbghyjgL3HUfR%2BhQXe6Z%2F1QLU2ArCo9uiUUv0GyC%2B33R6Wp8gANd2GiLd1D2ad0oDfAXr2ZkbEeasusCtn36sVEU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea7fc6186efa7a3cb5bb6ac8bb6c45f968b8b85bc7f90ec9692dc3db1b7a5a8f42af0fea7c3b92ab6bb9f97c821e98e8dd0db3ef18bafa4d93fadf186b8f74992abfaadc8748f9baaaab63a8797aed7d672e986ae88eb73aab984d4cb5fa68ee589d454a7ea96d0b45b908bfea2f149ade7bb8ad85fb6f0899ac221f1ed9ed7d67cfcb98fafe73a85b78485b450f2bfacd1ee50a69f9893b152a9be8b86e479b7ad8d95ed39f6ad9aa6d837e2a3; JSESSIONID-WYYY=kxQ0I6t2Oi8VbthZeydZc7q%5CgSKoUiyfFAxNpxZjjQSSmjjXkoOUHR6zFVAQQeUWZSrsyKg2ApVH8mr2HV%5Cam58US7D0mlyCt0kGcpCoPAyfpnA9C3jRHp2IvBlQ9OEPfjvEZbUeUF%2B1Dp%2BH%5CTFitCh5YKvUA96JsDbj35v79%2BaEpgav%3A1576052518201        referer: https://music.163.com/
        sec-fetch-mode: nested-navigate
        sec-fetch-site: same-origin
        upgrade-insecure-requests: 1
        user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36''')

def rsa_encrpt(text, pubKey, modulus):
	text = text[::-1]
	rs = pow(int(hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
	return format(rs, 'x').zfill(256)


def aes_encrypt(text, secKey):
	pad = 16 - len(text) % 16
	text = text + chr(pad) * pad
	encryptor = AES.new(secKey.encode('utf-8'), AES.MODE_CBC, b'0102030405060708')
	ciphertext = encryptor.encrypt(text.encode('utf-8'))
	ciphertext = base64.b64encode(ciphertext).decode('utf-8')
	return ciphertext

def get_sheet_list(page):
    # Proxy = ProxyMiddleware()
    # proxy = Proxy.process_request()
    # proxies = {
    #     'http': 'http://' + proxy,
    #     'https': 'https://' + proxy,
    # }
    # list = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
    # for i in range(page):
    num = page
    # print(num)
    try:
        next_num = num + 1
        print(num, next_num)
        while num < next_num:
            url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}'.format(str(num * 35))
            res = requests.get(url=url, headers=headers)
            # print(res.text)
            if res.status_code == 200:
                doc = etree.HTML(res.text)
                song_sheet_dict = {}
                lists = doc.xpath('//*[@id="m-pl-container"]/li/p[1]')
                for list in lists:
                    song_sheet_dict['name'] = ''.join(list.xpath('./a/text()'))
                    song_sheet_dict['url'] = 'https://music.163.com' + list.xpath('./a/@href')[0]
                    song_sheet_dict['id'] = list.xpath('./a/@href')[0].split('id=')[1]
                    yield song_sheet_dict
                num += 1
                print('已抓取到第{}页，共{}张歌单'.format(num,num*35))
            else:
                print('代理失效,重新请求')
                get_sheet_list(page)
    except:
        pass
def create_secret_key(size):
	return hexlify(os.urandom(size))[:16]

def get_song_list(page):
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pub_key = '010001'
    song_sheet_dicts = get_sheet_list(page)
    # song_dict = {}
    song_sheet_list = []
    song_total_dict = {}
    song_total_dict['songs'] = {}
    for song_sheet_dict in song_sheet_dicts:
        # print(song_sheet_dict)
        url = song_sheet_dict['url']
        res = requests.get(url = url,headers = headers)
        doc = etree.HTML(res.text)
        song_sheet_dict['name'] = re.findall('<title>(.*)</title>',res.text)[0].split('-')[0]
        song_sheet_dict['create_time'] = ''.join(doc.xpath("//span[contains(text(),'创建')]//text()")).split('\xa0')[0]
        song_sheet_dict['tags'] = doc.xpath('//b[contains(text(),"标签")]/../a//text()')
        song_sheet_dict['description'] = ''.join(doc.xpath("//b[contains(text(),'介绍：')]/../text()")).replace('\n',' ')
        song_sheet_dict['bf_num'] = ''.join(doc.xpath("//div[contains(text(),'播放')]/strong//text()"))
        song_sheet_dict['total_num'] = ''.join(doc.xpath("//span[contains(text(),'首歌')]/span//text()"))
        song_sheet_dict['url'] = res.url

        song_sheet_dict['song_detail'] = {}
        lists = doc.xpath('//ul[@class="f-hide"]/li')
        global create_secret_key
        song_detail_list = []
        for list in lists:
            song_detail = {}
            song_detail_url = 'https://music.163.com' + list.xpath('./a/@href')[0]

            # Proxy = ProxyMiddleware()
            # proxy = Proxy.process_request()

            song_detail_res = requests.get(url = song_detail_url,headers = headers)
            if song_detail_res.status_code == 200:
                song_detail['song_name'] = ''.join(etree.HTML(song_detail_res.text).xpath('//em[@class="f-ff2"]//text()'))
                song_detail['song_singer'] = ''.join(etree.HTML(song_detail_res.text).xpath('//p[contains(text(),"歌手")]/span/a/text()'))
                song_detail['song_edition'] = ''.join(etree.HTML(song_detail_res.text).xpath('//p[contains(text(),"所属专辑：")]/a/text()'))
                # print(song_detail)

                song_id = list.xpath('./a/@href')[0].split('id=')[1]
                secKey = {
                    'csrf_token': "",
                    'encodeType': "music",
                    'ids': "[{}]".format(song_id),
                    'level': "standard"
                }
                secKey_dumps = json.dumps(secKey)
                # print(secKey_dumps)
                create_secret_key1 = create_secret_key(16)
                enc_sec_key = rsa_encrpt(create_secret_key1, pub_key, modulus)
                enc_text = aes_encrypt(aes_encrypt(secKey_dumps, nonce), create_secret_key1.decode('utf-8'))
                # print(enc_text + '\n' + enc_sec_key)
                data = {'params': enc_text, 'encSecKey': enc_sec_key}
                url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token= '
                res = requests.post(url=url, headers=headers, data=data)
                song_detail['song_url'] = json.loads(res.text)['data'][0]['url']
                song_detail_list.append(song_detail)
            else:
                print('代理失效,重新请求')
                get_song_list(page)

        for i in range(len(song_detail_list)):
            song_sheet_dict['song_detail'][i] = song_detail_list[i]
            song_sheet_list.append(song_sheet_dict)
        print(song_sheet_dict)
        print('已抓取{}首歌'.format(len(song_sheet_list)))
    for j in range(len(song_sheet_list)):
        song_total_dict['songs'][j] = song_sheet_list[j]
        # save_mongo(song_total_dict)
    print(len(song_total_dict))
    time_ = int(time.time())
    jsondata = json.dumps(song_total_dict, ensure_ascii=False)
    with open('{}.json'.format(str(time_)), 'a', encoding='utf-8') as f:
        f.write(jsondata + '\n')
        f.close()
    print('在{}时间戳位置文件已保存'.format(time_))
    # print(song_total_dict)
    # return song_total_dict
def save_json(data):
    # print(jsondata)
    time_ = int(time.time())
    jsondata = json.dumps(data, ensure_ascii=False)
    with open('{}.json'.format(str(time_)), 'a',encoding='utf-8') as f:
        f.write(jsondata+'\n')
        print('在{}时间戳位置文件已保存'.format(time_))
            # f.close()

def save_mongo(data):
    # 指定MongoDB数据库信息
    mongocli = pymongo.MongoClient(host='localhost', port=27017)
    # 创建数据库名
    db = mongocli['mydb']
    # 创建空间
    sheet = db['wy_spider']
    sheet.insert(data)
    try:
        print(u"Processing: %(name)s <%(link)s>" % data)
    except KeyError:
        print(u"Error procesing: %r" % data)

for page in range(39):
    get_song_list(page)