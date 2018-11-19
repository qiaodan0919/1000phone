import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

r = requests.get('http://www.xiachufang.com/')
soup = BeautifulSoup(r.text)

img_list = []
for img in soup.select('img'):
    if img.has_attr('data-src'):
        img_list.append(img.attrs['data-src'])
    elif img.has_attr('src'):
        img_list.append(img.attrs['src'])

img_dir = os.path.join(os.curdir, 'images')
if not os.path.isdir(img_dir):
    os.mkdir(img_dir)

# for img in img_list:
#     o = urlparse(img)
#     url = img.split('@')[0].split('?')[0]
#     print(url)
#     filepath = os.path.join(img_dir, url)
#     # if not os.path.isdir(os.path.dirname(filepath)):
#     #     os.mkdir(os.path.dirname(filepath))
#     resp = requests.get(url)
#     with open(filepath, 'wb') as f:
#         for chunk in resp.iter_content(1024):
#             f.write(chunk)

for img in img_list:
    o = urlparse(img)
    print(o)
    filename = o.path[1:].split('@')[0]
    filepath = os.path.join(img_dir, filename)
    if not os.path.isdir(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))
    url = '%s://%s/%s' % (o.scheme, o.netloc, filename)
    resp = requests.get(url)
    with open(filepath, 'wb') as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)