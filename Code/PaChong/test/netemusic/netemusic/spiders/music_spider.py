# -*- coding: utf-8 -*-
import scrapy


class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/']

    def parse(self, response):
        pass
