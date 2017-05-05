#!/usr/bin/env python
# coding:utf-8
# A script collect edu src platform school name
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import os
import re
import sys
import time
import Queue
import urllib
import threading
import requests


class Parser(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        global borname, domains
        while True:
            element = self._queue.get()
            if isinstance(element, str) and element == 'quit':
                break
            try:
                name = findename(element, borname)
                if name:
                    name2domain(name, domains, lack)
            except:
                print '\n[-] Not found: ' + original_uri + str(element)
                lack.append(original_uri + str(element))


def build_worker_pool(queue, size):
    workers = []
    for _ in range(size):
        worker = Parser(queue)
        worker.start()
        workers.append(worker)
    return workers


def start():
    global threads, starts, ends
    targets = []

    # 3076 7111
    for _ in xrange(starts, ends + 1):
        targets.append(_)
    queue = Queue.Queue()
    worker_threads = build_worker_pool(queue, threads)
    for d in targets:
            queue.put(d)
    for worker in worker_threads:
            queue.put('quit')
    for worker in worker_threads:
            worker.join()


def findename(page, result):
    req = requests.get('{0}{1}'.format(original_uri, page), headers=header, timeout=15,
                       verify=False)
    match = re.findall(u"<h2>学校名称：(.*?)</h2>", req.text)
    if match:
        sys.stdout.write('\r[+] Find: {0}'.format(match[0].encode('GBK')))
        sys.stdout.flush()
        result.append(match[0].encode('utf-8'))
        return match[0].encode('utf-8')
    else:
        return False


def fillters(name, url, lack):
    TOP_fillter = ('cn', 'net', 'org', 'com', 'cc', 'hk')
    validtopname = ('edu', 'com', 'cn', 'net', 'gov')

    if '...' in url:
        url = url.split('...')[0]
    url = url.replace('<b>', '').replace('</b>', '')

    if url.startswith('http') and '//' in url:
        t = str(url).split('/')[2].split(':')[0]
        url = t if not '/' in t else t.split('/')[0]
    else:
        t = str(url).split('/')[0].split(':')[0]
        url = t if not '/' in t else t.split('/')[0]

    chunk = url.split('.')
    if not chunk[-1] in TOP_fillter:
        lack.append(name)
        return ''
    elif chunk[-2] in fillter_lists:
        lack.append(name)
        return ''
    else:
        if len(chunk) == 2 and not chunk[-2] in validtopname:
            return 'www.' + chunk[0] + '.' + chunk[1]
        elif len(chunk) == 3 and not chunk[0] in validtopname and not chunk[0] in fillter_lists:
            t = chunk[0] + '.' + chunk[1] + '.' + chunk[2]
            if not chunk[-2] in validtopname:
                return t
            else:
                return t if 'www.' in t else 'www.' + t
        elif len(chunk) == 4:
            if chunk[-3] in fillter_lists:
                return ''
            else:
                t1 = chunk[-3] + '.' + chunk[-2] + '.' + chunk[-1]
                t2 = chunk[0] + '.' + chunk[1] + '.' + chunk[2] + '.' + chunk[3]
                return t1 if 'www.' in t1 else (t2 if 'www.' in t2 else t2)
        elif len(chunk) == 5:
            t1 = chunk[-4] + '.' + chunk[-3] + '.' + chunk[-2] + '.' + chunk[-1]
            t2 = chunk[0] + '.' + chunk[1] + '.' + chunk[2] + '.' + chunk[3] + '.' + chunk[4]
            return t1 if 'www.' in t1 else (t2 if 'www.' in t2 else t2)
        else:
            lack.append(name)
            return ''


def name2domain(name, result, lack):
    global pattern
    data = {'wd': '{0}'.format(name)}
    req = requests.get('https://www.baidu.com/s?' + urllib.urlencode(data), headers=header, timeout=15, verify=False)
    match = re.findall(pattern, req.text)
    if match:
        target = match[0][0]
        fillted = fillters(name, target, lack)
        if fillted != '':
            sys.stdout.write('\r[+] Find: {0}'.format(fillted.encode('GBK')))
            sys.stdout.flush()
            result.append(fillted)
    else:
        lack.append(name)


if __name__ == '__main__':
    start_time = time.time()

    # 7112-3076+1=4037
    starts = 3076
    ends = 7112

    threads = 30
    borname = []
    domains = []
    lack = []

    original_uri = r'https://src.edu-info.edu.cn/list/firm/'

    root_path = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
    if not os.path.exists(os.path.join(root_path, 'data')):
        os.mkdir(os.path.join(root_path, 'data'))
    store_name_path = os.path.join(root_path, 'data', 'edusrc_school_name.txt')
    store_domain_path = os.path.join(root_path, 'data', 'edusrc_school_domains.txt')

    requests.packages.urllib3.disable_warnings()
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"}

    fillter_lists = ('1024sj', 'china', '11467', 'qymgc', '54114',
                     'cen114', '027art', 'baidu', 'gaokao', 'zhihu',
                     'chaoxing', 'b2b168', 'chineseall', 'fa08', 'chinacourt',
                     'e-fa', '12580', '360500', 'sohu', 'zhsho',
                     '8671', 'chazidian', '93soso', 'b2bname', '81',
                     'offcn', 'diyifanwen', 'danzhaowang', 'gw99', 'hao315',
                     'qiuxue360', 'peixun360', 'shanghai', 'city8', 'atobo',
                     '365zhaoshen', '71ab', 'sina', 'baike', '11315',
                     'shufa', 'uu456', 'zhaopin', '163', 'zhihu',
                     '360', 'alibole', '58', '5858', 'chinaedunet',
                     '01p', 'qq', 'baidu', 'bing', 'zhihu', 'pvc123', 'fzst',
                     'chinafastener', 'fanshuxueyuan', 'yingjiesheng', 'kaipuyun',
                     'youbian', 'yellowurl', 'gw99', 'maoyidi', 'fa08',
                     '30edu', 'b2bname', 'peixun5', 'snbcedu', 'danzhaowang',
                     'chinaispo', 'chinacourt', '93soso', 'chineseall',
                     'chn0769', 'snbcedu', '000pc', 'xzzsks', '365zhaosheng',
                     '99114', 'wanfangdata', 'szpxe', 'people', 'edutt')

    pattern = re.compile(
        '<div class="f13"><a target="_blank" href=.*class="c-showurl" style="text-decoration:none;">(.*?)'
        '&nbsp;</a><div class=.*id=.*data-tools=.{"title":"(.*?)".*>')

    start()

    count_name = 0
    if len(borname) > 0:
        with open(store_name_path, 'a') as _:
            for x in borname:
                try:
                    _.write(x + '\n')
                    count_name += 1
                except:
                    pass

    count_dom = 0
    if len(domains) > 0:
        with open(store_domain_path, 'a') as _:
            for x in domains:
                try:
                    _.write(x + '\n')
                    count_dom += 1
                except:
                    pass
    print("\n\n[-] All Not Found school:")
    for _ in lack:
        try:
            print(str(_).decode('utf-8'))
        except:
            pass

    print("\n[+] Parsed   : {0}     names\n"
            "[+] Parsed   : {1}     domains\n"
            "[+] Lack     : {2}\n"
            "[+] Cost     : {3:.4}  seconds".format(count_name, count_dom, len(lack), time.time()-start_time))


