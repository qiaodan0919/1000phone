# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


def str_deal(string):
    if string:
        exp_str = string.strip()
        return exp_str

headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            "User-Agent": "Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36",
            'Host':'www.lagou.com',
            'Referer': "https://www.lagou.com/zhaopin/Python/?filterOption=3",
        }

class SpiderLagouSpider(scrapy.Spider):
    name = 'spider_lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/?labelWords=label']

    def start_requests(self):

        return [Request(url=self.start_urls[0], headers=headers, callback=self.parse)]

    def parse(self, response):
        li_list = response.xpath('//ul[@class="item_con_list"]/li')
        data = {}
        for li in li_list:
            data["job"] = li.xpath('./@data-positionname').get()
            data["address"] = li.xpath('.//span[@class="add"]/em/text()').get()
            data["format-time"] = li.xpath('.//span[@class="format-time"]/text()').get()
            data['salary'] = li.xpath('./@data-salary').get()

            exp_origin_str = "".join(li.xpath('.//div[@class="p_bot"]/div/text()').extract())
            exp_str = str_deal(exp_origin_str)
            data["experience"] = exp_str

            data['company'] = li.xpath('./@data-company').get()
            print(data)
        next_page = response.xpath('//div[@class="item_con_pager"]//a[last()]/@href').get()

        if next_page:
            request = Request(url=next_page, callback=self.parse, headers=headers)
            yield request
