#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import urllib
import requests
from lib.fun import crawl_link_handle
from lib.config import baidu_base_url, get_head, timeout, baidu_first_pattern, self_pattern, intranet_ip_pattern, \
    ip_simple_pattern


def crawlinfocenter(domain):
    domains = []
    data = {'wd': 'site:{0} 信息化|网络中心'.format(domain)}
    requests.packages.urllib3.disable_warnings()
    req = requests.get(baidu_base_url + urllib.urlencode(data), headers=get_head(), timeout=timeout, verify=False)
    content = req.text
    match = baidu_first_pattern.findall(content)
    if match:
        info_center_url = crawl_link_handle(match[0][0])
        reqs = requests.get('http://' + info_center_url, headers=get_head(), timeout=timeout, verify=False)
        matchs = self_pattern.findall(reqs.text)
        for m in matchs:
            domains.append(crawl_link_handle(m)
                           if domain in m
                           else (crawl_link_handle(m)
                                 if ip_simple_pattern.findall(crawl_link_handle(m)
                                                              if not intranet_ip_pattern.findall(crawl_link_handle(m))
                                                              else '')
                                 else ''))
    return domains
