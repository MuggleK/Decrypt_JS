import execjs,time,requests,re

# 第一次请求,获取arg1
def get_arg1():
    url = 'https://jobs.zhaopin.com/CC120564550J00080758708.htm'
    res = requests.get(url=url)
    arg1 = re.findall("var arg1='(.*)';",res.text)[0]
    return arg1
# print(get_arg1())
with open('智联.js','r',encoding='utf8') as f:
    get_js = execjs.compile(f.read().replace('\xa0',''),cwd=r'C:\Users\MuggleK\node_modules')

arg1 = get_js.call('l',get_arg1())
print(arg1)

url = 'https://jobs.zhaopin.com/CC120564550J00080758708.htm'
headers = {
'cookie': 'acw_sc__v2=' + arg1,
# 'referer': 'https://jobs.zhaopin.com/CC120564550J00080758708.htm',
# 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
print(requests.get(url = url).text)




