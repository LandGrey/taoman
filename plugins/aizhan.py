#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import requests
from lib.config import aizhan_pr_pattern, aizhan_domain_pattern, set_max_page, pr_fake_switcher


def aizhan(domain):
    req = requests.get('http://baidurank.aizhan.com/baidu/' + domain)
    content = req.text
    prmatch = aizhan_pr_pattern.findall(content)
    dommatch = aizhan_domain_pattern.findall(content)
    if prmatch and prmatch[0].isdigit():
        set_max_page(domain, int(prmatch[0]))
        if int(prmatch[0]) < pr_fake_switcher:
            if dommatch:
                return dommatch
            else:
                return domain
        else:
            return domain
    else:
        set_max_page(domain, 1)
        return domain
