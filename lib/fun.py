#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import os
import re
import sys
import time
import random
import urllib
import urlparse
import requests
from lib.config import baidu_base_url, bing_base_url, timeout, get_max_page, pr_2_page_num, pr_fake_switcher


# order preserving
def unique(seq, idfun=None):
    if idfun is None:
        def idfun(x):
            return x
    seen = {}
    results = []
    try:
        for item in seq:
            marker = idfun(item)
            if marker in seen:
                continue
            seen[marker] = 1
            results.append(item)
    except:
        pass
    return results


def get_head():
    heads = (
         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
         'Mozilla/5.0 (X11; U; Linux x86_64; en-US) Gecko Firefox/3.0.8',
         'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.2.15 Version/10.00',
         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    )
    return {"User-Agent": random.choice(heads)}


def crawl_link_handle(url_without_http):
    if '/' in url_without_http:
        return url_without_http.split('/')[0].split(':')[0]
    else:
        return url_without_http.split(':')[0]


def url2host(url):
    if 'http' in url and '//' in url:
        host = urlparse.urlparse(url).netloc
    else:
        host = urlparse.urlparse(url).path
    host = host.split(":")[0]
    if '/' in host:
        host = host.split("/")[0]
    return host


def url2domname(url):
    fillter = ('edu', 'com', 'cn', 'net', 'gov', 'org', 'cc', 'qq', 'baidu', '360', 'bing', 'zhihu', 'edn')
    if url.startswith('http') and '//' in url:
        url = str(url).split('/')[2].split(':')[0]
    else:
        url = str(url).split('/')[0].split(':')[0]
    chunk = url.split('.')
    if len(chunk) >= 2:
        if chunk[-2] not in fillter:
            return chunk[-2] + '.' + chunk[-1]
        elif len(chunk) >= 3 and chunk[-3] not in fillter:
            return chunk[-3] + '.' + chunk[-2] + '.' + chunk[-1]
        elif len(chunk) >= 4 and chunk[-4] not in fillter:
            return chunk[-4] + chunk[-3] + '.' + chunk[-2] + '.' + chunk[-1]
        else:
            return ''
    else:
        return ''


def get_engine_pattern(domain, engine='baidu'):
    if engine == 'baidu':
        return re.compile(r'class="c-showurl" style="text-decoration:none;">(.*?)<b>{0}</b>.*?</a>'.format(domain))
    elif engine == 'bing':
        return re.compile(r'<cite>(.*?)<strong>{0}</strong>'.format(domain))


def get_req_data(domain, page, engine='baidu'):
    if engine == 'baidu':
        return {'wd': 'inurl:{0} site:{0}'.format(domain), 'pn': str(page - 1) + '0'}
    elif engine == 'bing':
        return {'q': 'site:{0}'.format(domain), 'first': str(page - 1) + '0'}


def fillters(domain):
    fillter_lists = ('qq', 'baidu', '360', 'bing', 'zhihu', 'pvc123', 'fzst',
                     'chinafastener', 'fanshuxueyuan', 'yingjiesheng', 'kaipuyun',
                     'youbian', 'yellowurl', 'gw99', 'maoyidi', 'fa08',
                     '30edu', 'b2bname', 'peixun5', 'snbcedu', 'danzhaowang',
                     'chinaispo', 'chinacourt', '93soso', 'chineseall',
                     'chn0769', 'snbcedu', '8671', '000pc')
    if str(domain).split('.')[-2] in fillter_lists or get_max_page(domain) / pr_2_page_num > pr_fake_switcher:
        return True
    else:
        return False


def write_result(file_path, results):
    tmp = []
    for x in unique(results):
        try:
            if len(x.strip()) > 3:
                tmp.append(str(x.strip().split("?")[0]).replace('</strong>', '').replace('<strong>', ''))
        except:
            pass

    with open(file_path, 'a') as _:
        for x in unique(tmp):
            try:
                 _.write(str(x).strip() + "\n")
            except:
                pass


def finish_print(raw, res, start):
    print("\n\n"
          "[+] base  : {0}     \n"
          "[+] gain  : {1}     \n"
          "[+] cost  : {2:.6}  seconds".format(len(raw), len(unique(res)), time.time() - start))


def init_domain(targets, store_list):
    if isinstance(targets, str):
        if not os.path.isfile(os.path.join(targets)):
            exit("[-] Domains file: %s don't exists" % targets)
        with open(targets, 'r') as f:
            for dom in f.readlines():
                if dom.strip():
                    store_list.append(dom.strip())
    else:
        for _ in targets:
            domain = url2host(_)
            store_list.append(domain)


def request_engine(domain, page, engine='baidu'):
    requests.packages.urllib3.disable_warnings()
    if engine == 'baidu':
        data = get_req_data(domain, page, 'baidu')
        req = requests.get(baidu_base_url + urllib.urlencode(data), headers=get_head(), timeout=timeout, verify=False)
    elif engine == 'bing':
        data = get_req_data(domain, page, 'bing')
        req = requests.get(bing_base_url + urllib.urlencode(data), headers=get_head(), timeout=timeout, verify=False)
    else:
        exit("[-] No engine: %s" % engine)
    return req.text


def try_engine(domain, page, results, engine='baidu'):
    try:
        sys.stdout.write('\r[+] Requests: {0:2} pages ==> {1:16}   Based on: {2:5}     Max pages: {3}'.format
                         (page, domain, engine, get_max_page(domain)))
        sys.stdout.flush()
        match = get_engine_pattern(domain, engine).findall(request_engine(domain, page, engine))
        for m in match:
            results.append(m + domain)
    except:
        try:
            sys.stdout.write('\r[+] Requests: {0:2} pages ==> {1:16}   Based on: {2:5}     Max pages: {3}'.format
                             (page, domain, engine, get_max_page(domain)))
            sys.stdout.flush()
            match = get_engine_pattern(domain, engine).findall(request_engine(domain, page, engine))
            for m in match:
                results.append(m + domain)
        except:
            pass


def cli_parser():
    if len(sys.argv) < 3:
        exit('[!] Usage: python taoman.py -t www.example.com,http://www.victim.com\n'
             '                            -f /my/path/targets.txt\n')
    else:
        _ = []
        if sys.argv[1] == '-t':
            chunk = sys.argv[2].split(',')
            for c in chunk:
                _.append(c)
            return _
        elif sys.argv[1] == '-f':
            return sys.argv[2]
        else:
            exit('[!] Usage: python taoman.py -t www.example.com,www.victim.com\n'
                 '                            -f /my/path/targets.txt\n')
