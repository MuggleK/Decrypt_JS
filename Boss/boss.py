import requests
from copyheaders import headers_raw_to_dict

base_url = 'https://www.zhipin.com/job_detail/?query=python&city=100010000&industry=&position=100120'

headers = headers_raw_to_dict(b'''
authority: www.zhipin.com
method: GET
path: /job_detail/?query=python&city=100010000&industry=&position=100120
scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6
referer: https://www.zhipin.com/job_detail/?query=python&city=100010000&industry=&position=100120
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
''')


res = requests.get(url = base_url,headers = headers,verify=False,allow_redirects = False)
res_dict = {}
for item in res.headers['location'].split('?')[1].split('&'):
    # print(item.split('=')[1])
    res_dict[item.split('=')[0]] = item.split('=')[1]
print(res_dict)