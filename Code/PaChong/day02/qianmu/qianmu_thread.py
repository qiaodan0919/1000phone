import threading
import time
from queue import Queue

import requests
from lxml import etree

start_url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
link_queue = Queue()
threads_num = 10
threads = []
download_pages = 0


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


def download():
    while True:
        link = link_queue.get()
        if link is None:
            break
        data = parse_univerity(link)
        process_data(data)
        link_queue.task_done()
        print('remaining queue: %s' % link_queue.qsize())


def process_data(data):
    """处理数据"""
    if data:
        print(data)


if __name__ == '__main__':
    start_time = time.time()
    selector = etree.HTML(fetch(start_url))
    links = selector.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href')
    for link in links:
        if not link.startswith('http://qianmu.iguye.com'):
            link = 'http://qianmu.iguye.com/' + link
        link_queue.put(link)
    for i in range(threads_num):
        t = threading.Thread(target=download)
        t.start()
        threads.append(t)

    link_queue.join()

    for i in range(threads_num):
        link_queue.put(None)

    for t in threads:
        t.join()

    cost_seconds = time.time() - start_time
    print('downloaded %s pages , cost %.2f seconds' %
          (download_pages, cost_seconds))

