# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http.cookies import CookieJar
from scrapy_splash import SplashRequest

from mafw.items import MafwItem


class SpiderMafwSpider(scrapy.Spider):
    name = 'spider_mafw'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = ['https://www.mafengwo.cn/mdd/']

    def start_requests(self):
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "www.mafengwo.cn",
            'Referer': "https://www.mafengwo.cn/mdd/",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
            'Cache-Control': "no-cache",
        }
        cookies = {
            'Cookie': 'PHPSESSID=j66370h151d5744losn00m77i3; path=/; domain=.mafengwo.cn; HttpOnly'
        }
        payload = "t=1541741963&hn=www.mafengwo.cn&u=https%3A%2F%2Fwww.mafengwo.cn%2Fmdd%2F&r=https%3A%2F%2Fwww.mafengwo.cn%2F&lv=1541740335&vn=2&ws=1085x922&sc=1920x1080&sl=zh-CN&fl=Not%20enabled&cs=UTF-8&dt=%E7%9B%AE%E7%9A%84%E5%9C%B0%E6%97%85%E6%B8%B8%E6%94%BB%E7%95%A5%20-%20%E9%A9%AC%E8%9C%82%E7%AA%9D&sts=31&pid=a9b186bd-a5a7-4281-b737-3f3a5212ae35&brn=Chrome&brv=69&dev=unknown&os=Linux&os_ver=Linux_unknow&sid=0&ver=1.2&rdm=863790163&_nocache=15417419632030.2551963373019275&_method=post"
        yield scrapy.Request(url=self.start_urls[0], headers=headers, callback=self.parse, cookies=cookies,
                             method='POST', body=payload)

    def parse(self, response):
        countries = response.xpath('//div[@class="row-list"]//li/a')
        for country in countries:
            country_name, = country.xpath('./text()').extract()
            country_html, = country.xpath('./@href').extract()
            country_url = 'https://www.mafengwo.cn'+ country_html
            print(country_name, country_html)
            request = SplashRequest(url=country_url, callback=self.parse_country)
            request.meta['country'] = country_name
            yield request

    def parse_country(self,response):
        div_list = response.xpath('//div[contains(@class,"tn-item")]')
        data_div = MafwItem()
        for div in div_list:
            data_div['country'] = response.meta['country']
            data_div['title'] = div.xpath('.//dt/a/text()').get()
            data_div['img'] = div.xpath('./div/a/img/@data-original').get()
            data_div['content'] = div.xpath('.//dd/a/text()').get()
            data_div['user'] = div.xpath('.//span[@class="tn-user"]//text()').get()
            data_div['look_num'] = div.xpath('.//span[@class="tn-nums"]//text()').get()
            yield data_div
        next_url = response.xpath('//div[@class="_pagebar"]//a[contains(@class,"pg-next")]/@href').get()
        if next_url:
            url = 'https://www.mafengwo.cn' + next_url
            request = SplashRequest(url=url, callback=self.parse_next)
            request.meta['country'] = response.meta['country']
            yield request

    def parse_next(self, response):
        li_list = response.xpath('//li[contains(@class,"post-item")]')
        data_div = MafwItem()
        for li in li_list:
            data_div['country'] = response.meta['country']
            data_div['title'] = li.xpath('./h2/a/text()').get()
            data_div['img'] = li.xpath('./div/a/img/@data-original').get()
            data_div['content'] = li.xpath('.//div[@class="post-content"]/text()').get()
            data_div['user'] = li.xpath('.//span[@class="author"]/a[2]/text()').get()
            data_div['look_num'] = li.xpath('.//span[@class="status"]/text()[1]').get()
            yield data_div



