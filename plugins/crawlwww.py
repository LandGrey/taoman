#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import requests
from lib.fun import get_head, crawl_link_handle, url2domname, url2host
from lib.config import self_pattern, ip_pattern, intranet_ip_pattern, timeout


def crawlwww(url):
    domains = []
    requests.packages.urllib3.disable_warnings()
    h1 = url2host(url)
    host = 'http://' + (h1 if 'www' in h1 else 'www.' + h1)
    domain = url2domname(host)
    reqs = requests.get(host, headers=get_head(), timeout=timeout, verify=False)
    matchs = self_pattern.findall(reqs.text)
    for m in matchs:
        standom = crawl_link_handle(m)
        domains.append(standom if domain in m
                       else (standom
                             if ip_pattern.findall(m) and not intranet_ip_pattern.findall(m)
                             else domain))
    return domains
