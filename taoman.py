#!/usr/bin/env python
# coding:utf-8
#
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""

import sys
import time
import Queue
import threading
from lib.fun import init_domain, finish_print, write_result, try_engine, unique, url2domname, cli_parser, fillters
from lib.config import get_max_page, plug_max_retries, domains, sub_domains, threads, ilinkscn_use_pr_switcher, \
    pr_2_page_num
from plugins.aizhan import aizhan
from plugins.crawlwww import crawlwww
from plugins.ilinkscn import get_ilinkscn_results
from plugins.crawlinfocenter import crawlinfocenter


def start():
    queue = Queue.Queue()
    worker_threads = builder(queue, threads)
    for dom_name in unique(domains):
            queue.put(dom_name)
    for worker in worker_threads:
            queue.put('quit')
    for worker in worker_threads:
            worker.join()


def builder(queue, size):
    workers = []
    for _ in range(size):
        worker = Taoman(queue)
        worker.start()
        workers.append(worker)
    return workers


class Taoman(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        retry = 0
        while True:
            element = self._queue.get()
            if isinstance(element, str) and element == 'quit':
                break
            try:
                # domain format: xxx.edu.cn
                domain = url2domname(element)

                # fake domain
                if domain == '':
                    continue

                # use plug: aizhan
                sys.stdout.write('\r[+] Extend: {0:16}  Based on plugin: aizhan'.format(domain))
                sys.stdout.flush()
                try:
                    sub_domains.extend(aizhan(domain))
                except:
                    retry = 0
                    while retry <= plug_max_retries:
                        retry += 1
                        sys.stdout.write("\r[!] plug :aizhan retry -> {0}".format(retry))
                        sys.stdout.flush()
                        try:
                            sub_domains.extend(aizhan(domain))
                            retry += 3
                        except:
                            pass

                # invalid domain
                if fillters(domain):
                    continue

                # # use plug: maindomuri
                try:
                    sub_domains.extend(crawlwww(element))
                except:
                    retry = 0
                    while retry <= plug_max_retries:
                        retry += 1
                        sys.stdout.write("\r[!] Plug: maindomuri retry -> {0}".format(retry))
                        sys.stdout.flush()
                        try:
                            sub_domains.extend(crawlwww(element))
                            retry += 3
                        except:
                            pass

                # use plug: infocenteruri
                try:
                    sub_domains.extend(crawlinfocenter(domain))
                except:
                    retry = 0
                    while retry <= plug_max_retries:
                        retry += 1
                        sys.stdout.write("\r[!] Plug: infocenteruri retry -> {0}".format(retry))
                        sys.stdout.flush()
                        try:
                            sub_domains.extend(crawlinfocenter(domain))
                            retry += 3
                        except:
                            pass

                # # use plug: ilinkscn
                if get_max_page(domain) / pr_2_page_num >= ilinkscn_use_pr_switcher + 1:
                    sys.stdout.write('\r[+] Extend: {0:16}  Based on plugin: ilinkscn'.format(domain))
                    sys.stdout.flush()
                    try:
                        sub_domains.extend(get_ilinkscn_results(domain))
                    except:
                        retry = 0
                        while retry <= plug_max_retries:
                            retry += 1
                            sys.stdout.write("\r[!] plug :ilinkscn retry -> {0}".format(retry))
                            sys.stdout.flush()
                            try:
                                sub_domains.extend(get_ilinkscn_results(domain))
                                retry += 3
                            except:
                                pass

                # use search engine
                for page in xrange(1, get_max_page(domain) + 1):
                    try_engine(domain, page, sub_domains, 'baidu')
                    try_engine(domain, page, sub_domains, 'bing')
            except:
                pass


if __name__ == '__main__':
    start_time = time.time()
    init_domain(cli_parser(), domains)
    if len(domains) > 0:
        print("[+] Init original domains: {0}".format(len(domains)))
    else:
        exit("[!] No domains")
    try:
        start()
    except:
        pass
    finally:
        for line in sub_domains:
            if 'https://' in line.strip():
                sub_domains.remove(line)
                sub_domains.append(line[8:])
        write_result(r'taoman.txt', sub_domains)
        finish_print(domains, sub_domains, start_time)
