# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MafwItem(scrapy.Item):
    table_name = 'mafw'
    country = Field()
    title = Field()
    img = Field()
    content = Field()
    user = Field()
    look_num = Field()
