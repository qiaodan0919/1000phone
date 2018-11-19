import requests
from lxml import etree

status_200 = []
status_other = []
status_none = []
def fetch(url):
    r = requests.get(url)
    if r.status_code != 200:
        r.raise_for_status()
    return r.text.replace('\t', '')

def parse_univerity(link):
    try:
        status = requests.get(link).status_code
        if status != 200:
            status_other.append(link)
        else:
            status_200.append(link)
    except Exception:
        status_none.append(link)


if __name__ == '__main__':
    selector = etree.HTML(fetch('http://www.hao123.com'))
    links = selector.xpath('//a/@href')
    for link in links:
        # if not link.startswith('http'):
        print(link)
        data = parse_univerity(link)
    print(status_200)
    print(status_other)
    print(status_none)