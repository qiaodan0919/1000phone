import requests

r = requests.get('http://httpbin.org/get', params={'a': 1})
print(r.json())

r = requests.post('http://httpbin.org/post', data={'a': 1})
print(r.json())

cookies = dict(userid='123456', token='999999999999999999999')
r = requests.get('http://httpbin.org/cookies', cookies=cookies)
print(r.json())

r = requests.get('http://httpbin.org/basic-auth/qiao/123456', auth=('qiao', '123456'))
print(r.text)

s = requests.Session()
s.get('http://httpbin.org/cookies/set/userid/123')
r = s.get('http://httpbin.org/cookies')
print(r.json())


print(requests.get('http://httpbin.org/ip').json())
print(requests.get('http://httpbin.org/ip', proxies={'http': 'http://iguye.com:41801'}).json())

r = requests.get('http://httpbin.org/delay/4', timeout=3)
print(r.text)