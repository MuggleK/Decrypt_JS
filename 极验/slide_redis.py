import json
import redis
'''轨迹存入redis'''
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)

# f=open("./jiyan2.json","r", encoding = 'utf-8')
# distance_list = set([json.loads(line).get('distance') for line in f])
distance_list = ['140', '87', '153', '76', '185', '119', '147', '187', '81', '63', '99', '133', '136', '131', '83', '137', '159', '86', '91', '169', '109', '89', '114', '69', '154', '103', '127', '138', '189', '115', '176', '64', '148', '55', '142', '156', '38', '46', '130', '41', '146', '122', '145', '116', '163', '177', '128', '155', '181', '186', '62', '170', '110', '72', '92', '65', '71', '93', '149', '112', '171', '49', '126', '105', '84', '37', '135', '129', '82', '66', '54', '96', '125', '167', '117', '94', '53', '164', '78', '36', '45', '166', '73', '88', '79', '134', '50', '182', '56', '58', '168', '150', '57', '51', '74', '90', '179', '188', '173', '139', '183', '123', '40', '102', '52', '175', '151', '101', '80', '98', '75', '39', '95', '61', '104', '85', '59', '161', '184', '111', '47', '60', '165', '172', '178', '121', '44', '174', '152', '43', '97', '113', '132', '68', '42', '118', '70', '157', '144', '124', '141', '106', '77', '160', '190', '158', '100', '180', '48', '162', '120', '143', '107', '108', '67']


f_new = open("./jiyan2.json","r", encoding = 'utf-8')
datas_ = [json.loads(data) for data in f_new]
datas = []
for distance in distance_list:
    dict = {}
    lists = []
    for data in datas_:
        if data.get('distance') == distance:
            # print(distance)
            lists.append(data.get('locus'))
            dict[data.get('distance')] = lists
    datas.append(dict)

for data in datas:
    print(str(data.keys()))
    for key,value in data.items():
        for i in value:
            r.lpush(key,i)



