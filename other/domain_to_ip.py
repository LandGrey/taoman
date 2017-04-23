#!/usr/bin/env python
# coding:utf-8
# A tiny Domain name Parse Ip script
"""
Copyright (c) 2017 LandGrey (https://github.com/LandGrey/taoman)
License: MIT
"""


import os
import sys
import time
import socket
import Queue
import threading


class Parser(threading.Thread):
    global borname

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            element = self._queue.get()
            if isinstance(element, str) and element == 'quit':
                    break
            try:
                ip = socket.gethostbyname(element)
                borname.append(ip)
                sys.stdout.write("\r[+] Parsing {0:20} -> {1:15}".format(element, ip))
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write("\r[-] Parsing %s  error" % element)
                sys.stdout.flush()


def build_worker_pool(queue, size):
    workers = []
    for _ in range(size):
        worker = Parser(queue)
        worker.start()
        workers.append(worker)
    return workers


def urlfillter(url):
    if url.startswith('http') and '//' in url:
        url = (url.split('/')[2]).split(':')[0]
    else:
        url = (url.split('/')[0]).split(':')[0]
    return url


def start():
    global targets, threads, domain_file_path

    with open(domain_file_path, 'r') as f:
        for dom in f.readlines():
            targets.append(urlfillter(dom.strip()))

    queue = Queue.Queue()
    worker_threads = build_worker_pool(queue, threads)
    for url in targets:
            queue.put(url)
    for worker in worker_threads:
            queue.put('quit')
    for worker in worker_threads:
            worker.join()


# order preserving
def unique(seq, idfun=None):
    if idfun is None:
        def idfun(x): return x
    seen = {}
    results = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        results.append(item)
    return results


if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) != 2:
        exit("[-] Usage: python domain_to_ip.py domain_lists_path \n")
    else:
        if not os.path.isfile(sys.argv[1]):
            exit('[-] No file: %s \n' % sys.argv[1])
    print("[+] A tiny Domain name To Ip script start \n"
          "                                    Build By LandGrey\n")
    threads = 50
    borname = []
    targets = []
    domain_file_path = sys.argv[1]
    store_file_path = r'ip_lists.txt'

    start()
    count = 0
    with open(store_file_path, 'a') as _:
        for x in unique(borname):
            try:
                _.write(str(x) + "\n")
                count += 1
            except:
                pass
    print("\n[+] Parsed   : {0}     targets\n"
          "[+] Total of : {1}     ip\n"
          "[+] Cost     : {2:.6} seconds".format(len(targets), count, time.time() - start_time))
