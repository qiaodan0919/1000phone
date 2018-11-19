# -*- coding: utf-8 -*-
import scrapy

from ..items import QianmuItem


class SpiderQianmuSpider(scrapy.Spider):
    name = 'spider_qianmu'
    allowed_domains = ['qianmu.iguye.com']
    start_urls = ['http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D']

    def parse(self, response):
        links = response.xpath('//div[@id="content"]//tr[position()>1]/td[2]/a/@href').extract()
        for link in links:
            if not link.startswith('http://qianmu.iguye.com'):
                link = 'http://qianmu.iguye.com/%s' % link
            yield response.follow(link, self.parse_university)


    def parse_university(self, response):
        response = response.replace(body=response.text.replace('\t', '').replace('\r\n', ''))
        item = QianmuItem()
        data = {}
        item['name'] = response.xpath('//div[@id="wikiContent"]/h1/text()').extract_first()
        table = response.xpath('//div[@id="wikiContent"]/div[@class="infobox"]/table')
        if table:
            table = table[0]
            keys = table.xpath('.//td[1]/p/text()').extract()
            cols = table.xpath('.//td[2]')
            values = [' '.join(col.xpath('.//text()').extract_first()) for col in cols]
            if len(keys) == len(values):
                data.update(zip(keys, values))
        item['rank'] = data.get('排名')
        item['country'] = data.get("国家")
        item['state'] = data.get('州省')
        item['city'] = data.get('城市')
        item['undergraduate_num'] = data.get('本科生人数')
        item['postgraduate_num'] = data.get('研究生人数')
        item['website'] = data.get('网址')
        yield item