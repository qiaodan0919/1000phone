import signal
import sys
import threading
import time
from queue import Queue

import redis
import requests
from lxml import etree

start_url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
link_queue = Queue()
threads_num = 10
threads = []
download_pages = 0
r = redis.Redis(host='127.0.0.1', password='123456')
thread_on = True

def parse_univerity(url):
    """处理大学详情页面"""
    selector = etree.HTML(fetch(url))
    data = {}
    data['name'] = selector.xpath('//div[@id="wikiContent"]/h1/text()')[0]
    table = selector.xpath(
        '//div[@id="wikiContent"]/div[@class="infobox"]/table')
    if table:
        table = table[0]
        keys = table.xpath('.//td[1]/p/text()')
        cols = table.xpath('.//td[2]')
        values = [' '.join(col.xpath('.//text()')) for col in cols]
        if len(keys) != len(values):
            return None
        data.update(zip(keys, values))
        return data


def fetch(url):
    r = requests.get(url)
    if r.status_code !=200:
        r.raise_for_status()
    global download_pages
    download_pages += 1
    return r.text.replace('\t', '')


def download(i):
    while thread_on:
        link = r.lpop('qianmu.queue')
        if link:
            data = parse_univerity(link)
            process_data(data)
            print('remaining queue: %s' % r.llen('qianmu.queue'))
        time.sleep(0.2)
    print('Thread-%s eixt now' % i)


def process_data(data):
    """处理数据"""
    if data:
        print(data)

def sigint_handler(signum, frame):
    print('received Ctrl+C, wait for exit gracefully')
    global thread_on
    thread_on = False


if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
        selector = etree.HTML(fetch(start_url))
        links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')
        for link in links:
            if not link.startswith('http://qianmu.iguye.com'):
                link = 'http://qianmu.iguye.com/' + link
            if r.sadd('qianmu.seen', link):
                r.rpush('qianmu.queue', link)
    else:
        for i in range(threads_num):
            t = threading.Thread(target=download, args=(i+1,))
            t.start()
            threads.append(t)

        signal.signal(signal.SIGINT, sigint_handler)
        link_queue.join()

        # for i in range(threads_num):
        #     link_queue.put(None)

        for t in threads:
            t.join()

        cost_seconds = time.time() - start_time
        print('downloaded %s pages , cost %.2f seconds' %
              (download_pages, cost_seconds))

