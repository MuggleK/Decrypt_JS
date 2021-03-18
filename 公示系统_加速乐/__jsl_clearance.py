import json,re,hashlib,time,execjs

def get_clearance(html):
    data = json.loads(re.findall('go\((.*?)\)', html)[1])
    chars_length = len(data.get('chars'))
    for i in range(chars_length):
        for j in range(chars_length):
            result = data.get('bts')[0] + data.get('chars')[i] + data.get('chars')[j] + data.get('bts')[1]
            b = eval('hashlib.{}()'.format(data.get('ha')))
            b.update(result.encode(encoding='utf-8'))
            res = b.hexdigest()
            if res == data.get('ct'):
                return result


def js_fuck(html):
    data = re.findall('document.cookie=(.*?)location.href',html)[0]
    fuck_encrypt = execjs.compile('''
    function js_fuck(){
        var result = eval(%r)
        return result
    }
    '''%data)
    result = fuck_encrypt.call('js_fuck').split(';')[0].split('__jsl_clearance=')[1]
    return result
