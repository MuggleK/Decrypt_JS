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


def get_arg(arg1):
    """
    acw_sc__v2算法
    :param arg1:
    :return:
    """
    list1 = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21, 32,
                 26, 2, 30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
    dict1 = {}
    for i in range(len(arg1)):
        strs = arg1[i]
        for j in range(len(list1)):
            if list1[j] == i + 1:
                dict1[j] = (strs)
    str1 = ''.join([dict1.get(i) for i in range(40)])

    str1_list = list(str1)
    str2 = "3000176000856006061501533003690027800375"
    str2_list = list(str2)
    str4 = ''
    for m in range(0,len(str1_list),2):
        int1 = int(''.join(str1_list[m:m + 2]),16)
        int2 = int(''.join(str2_list[m:m + 2]),16)
        str3 = str(hex(int1 ^ int2))[2:]
        if len(str3) == 1:
            str3 = '0' + str3
        str4 += str3
    return str4
