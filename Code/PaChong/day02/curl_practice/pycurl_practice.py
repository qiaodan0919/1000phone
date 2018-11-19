import os
import re
from io import BytesIO
from urllib.parse import urlparse

from pycurl import Curl

buffer = BytesIO()
c = Curl()
c.setopt(c.URL, 'http://www.xiachufang.com/')
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()
body = buffer.getvalue()
text = body.decode('utf-8')

img_list = re.findall(r'src=\"(http://i2\.chuimg\.com/\w+\.jpg)', text)

img_dir = os.path.join(os.curdir, 'images')
print(len(img_list))

for img in img_list:
    o = urlparse(img)
    print(img)
    filename = o.path[1:]
    filepath = os.path.join(img_dir, filename)
    if not os.path.isdir(os.path.dirname(filepath)):
        os.mkdir(os.path.dirname(filepath))
    with open(filepath, 'wb') as f:
        c = Curl()
        c.setopt(c.URL, img)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()
