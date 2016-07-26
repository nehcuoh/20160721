# encoding=utf-8
import random
import string
import struct
import socket
import urllib, urllib2, json, requests
from urllib import urlencode
from word import word

websitprefix = ['www.', 'mail.', 'bbs.']
websitpsuffix = ['.com', '.cn', '.org']

import time


def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都需要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # 将"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


#
# if __name__ == '__main__':
#     d = datetime_timestamp('2012-03-28 06:53:40')
#     print d
#     s = timestamp_datetime(1332888820)
#     print s

data_time = datetime_timestamp('2016-07-20 06:53:40')

RANDOM_IP_POOL = ['192.168.10.0/24', '172.16.0.0/16', '192.168.1.0/24', '192.168.2.0/24']


def __get_random_ip(str_ip):
    # str_ip = RANDOM_IP_POOL[random.randint(0, len(RANDOM_IP_POOL) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask |= 1 << i
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))


def randomwebsite():
    web = random.choice(websitprefix) + random.choice(word) + (random.choice(websitpsuffix))
    print web
    return web


def addip(ip_json):
    url = 'http://localhost:8088/20160721/add.php'
    headers = {'Content-Type': 'text/json;charset=UTF-8'}
    # jdata = json.dumps(ip_json)
    # req = urllib2.Request(url, jdata)
    # response = urllib2.urlopen(req)
    # return response.read()
    payload = {'data': ip_json}
    r = urllib2.urlopen(url=url, data=urllib.urlencode(payload))
    # r = requests.post(url, data=payload, headers=headers)
    print r.read()


weblist = open('weblist.txt', 'w')
for i in range(1, 100):
    randomweb = randomwebsite()
    weblist.write(randomweb)
    weblist.write('\n')
    webdata = open(randomweb, 'w')
    ip_str = random.choice(RANDOM_IP_POOL)
    for k in range(1, random.randint(2, 10)):
        randomtime = data_time + random.randint(-259200, 259200)
        rank_str = ''
        for ip in range(random.randint(10, 40)):
            rank_str += '    "' + __get_random_ip(ip_str) + '":' + str(random.randint(100, 5000)) + ',\n'
        rank_str = rank_str[:-2] + '\n'
        json = '{"name":"' + randomweb + '",\n"createTime":' + str(
            randomtime) + ',\n"Rank":{\n' + rank_str + '}}\n\n'
        addip(json)
        webdata.write(json)
    webdata.close()
    # f2.flush()
weblist.close()
