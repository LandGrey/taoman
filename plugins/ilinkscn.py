#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import requests
from lib.fun import get_head
from lib.config import timeout, ilinkscn_pattern, ilinkscn_fake_dom_len_switcher


def get_ilinkscn_results(domain):
    domains = []
    data = {'domain': domain, 'b2': '1', 'b3': '1', 'b4': '1'}
    req = requests.post('http://i.links.cn/subdomain/', data=data, headers=get_head(), timeout=timeout)
    match = ilinkscn_pattern.findall(req.text)
    for m in match:
        dom = m.split(':')[0]
        if len(dom) <= ilinkscn_fake_dom_len_switcher:
            domains.append(dom)
    if len(domains) < 200:
        return domains
    else:
        return domain
