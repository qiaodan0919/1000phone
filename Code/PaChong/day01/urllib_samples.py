import urllib.request
import json

# params = urllib.parse.urlencode({'spam':1, 'eggs':2, 'bacon': 2})
# url = 'http://httpbin.org/get?%s' % params
# with urllib.request.urlopen(url) as f:
#     print(json.load(f))
#
#
# data = urllib.parse.urlencode({"name": 'xiaoming', 'age': 2})
# data = data.encode()
# with  urllib.request.urlopen('http://httpbin.org/post', data) as f:
#     print(json.load(f))
#

#使用代理ip请求远程url
# proxy_handler = urllib.request.ProxyHandler({
#     'http': 'http://iguye.com:41801'
# })
# opener = urllib.request.build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(r.read())


#urlparse模块
# o = urllib.parse.urlparse