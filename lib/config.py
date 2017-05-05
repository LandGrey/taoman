#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import re

domains = []
sub_domains = []

threads = 20
timeout = 10
pr_2_page_num = 8
max_pages = dict()
plug_max_retries = 2
pr_fake_switcher = 7
ilinkscn_use_pr_switcher = 1
ilinkscn_fake_dom_len_switcher = 25

baidu_base_url = 'http://www.baidu.com/s?'
bing_base_url = 'http://www.bing.com/search?'

# match pattern
self_pattern = re.compile(r'href="http://(.*?)"')
ilinkscn_pattern = re.compile(r'<div class=domain><input type=hidden name=domain\d{1,3}'
                              r' id=domain\d{1,3} value="https?://(.*?)">')
ip_pattern = re.compile(r'(\d{1,3}[.]){3}\d{1,3}')
baidu_first_item_pattern = re.compile('<div class="f13"><a target="_blank" href=.*class="c-showurl" '
                                      'style="text-decoration:none;">(.*?)&nbsp;</a><div class=.*id'
                                      '=.*data-tools=.{"title":"(.*?)".*>')

aizhan_pr_pattern = re.compile(r'<img src="http://static\.aizhan\.com/images/br/(\d{1,2})\.gif"/></td>')
aizhan_domain_pattern = re.compile(r'<a  title=".*?" href="http://baidurank[.]aizhan[.]com/baidu/(.*?)/">')

# no localhost, raw match pattern written by myself
intranet_ip_pattern = re.compile(r'(^10\.((\d){1,3}\.){2}(\d){1,3})|'
                                 r'(^127\.((\d){1,3}\.){2}(\d){1,3}$)|'
                                 r'(^172\.([1][6-9]|[2][0-9]|[3][0-1])\.(\d){1,3}\.(\d){1,3})|'
                                 r'(^192\.168\.(\d){1,3}\.(\d){1,3})')


def set_max_page(domain, new_page_value):
    global max_pages
    if not domain in max_pages.keys():
        max_pages[domain] = new_page_value


def get_max_page(domain):
    global max_pages
    if domain in max_pages.keys():
        return (max_pages[domain] + 1) * pr_2_page_num
    else:
        return 10
