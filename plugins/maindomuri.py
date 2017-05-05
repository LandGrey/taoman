#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import requests
from lib.fun import crawl_link_handle
from lib.config import self_pattern, ip_simple_pattern, intranet_ip_pattern, get_head, timeout


def crawlmaindom(domain):
    domains = []
    requests.packages.urllib3.disable_warnings()
    if not (domain.startswith('http') and '//' in domain):
        domain = 'http://' + domain
    reqs = requests.get(domain, headers=get_head(), timeout=timeout, verify=False)
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
