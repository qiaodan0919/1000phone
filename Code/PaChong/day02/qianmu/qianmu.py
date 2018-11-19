import time

import requests
from lxml import etree

start_url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
download_pages = 0

#请求下载网站
def fetch(url):
    r = requests.get(url)
    if r.status_code != 200:
        r.raise_for_status()
    global download_pages
    download_pages += 1
    return r.text.replace('\t', '')

def parse_univerity(link):
    selector = etree.HTML(fetch(link))
    data = {}
    data['name'] = selector.xpath('//div[@id="wikiContent"]/h1/text()')[0]
    table = selector.xpath('//div[@id="wikiContent"]/div[@class="infobox"]/table')
    if not table:
        return None
    table = table[0]
    keys = table.xpath('.//td[1]/p/text()')
    cols = table.xpath('.//td[2]')
    values = [''.join(col.xpath('.//text()')) for col in cols]
    if len(keys) != len(cols):
        return None
    data.update(zip(keys, values))
    return data


def process_data(data):
    if data:
        print(data)


if __name__ == '__main__':
    start_time = time.time()
    selector = etree.HTML(fetch(start_url))
    links = selector.xpath('//div[@id="content"]//td[2]/a/@href')
    for link in links:
        if not link.startswith('http://qianmu.iguye.com'):
            link = 'http://qianmu.iguye.com/%s' % link

        data = parse_univerity(link)
        process_data(data)