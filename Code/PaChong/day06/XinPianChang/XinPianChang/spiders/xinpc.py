# -*- coding: utf-8 -*-
import json
import random
import re
import string

import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

from XinPianChang.items import PostItem, CopyrightItem, CommentItem, ComposerItem

cookies = dict(
    Authorization='A6223C02E5173BBB4E51734747E5173859FE5173BC9D182D93F0'
)
def strip(s):
    if s:
        return s.strip().replace('\n', ',')
    return ''

def str_int(s):
    if isinstance(s, str):
        return int(s.replace(',',''))
    return 0

def gen_sessionid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))

class XinpcSpider(RedisSpider):
    name = 'xinpc'
    allowed_domains = ['xinpianchang.com',
                       'openapi-vtom.vmovier.com']
    # start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']
    page_count = 0

    def parse(self, response):
        print('-----------')
        self.page_count += 1
        if self.page_count >= 100:
            cookies.update(PHPSESSID=gen_sessionid())
            self.page_count = 0
        post_list = response.xpath('//div/ul[@class="video-list"]/li')
        url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            post_url = url % pid
            request = response.follow(post_url, self.parse_post)
            request.meta['pid'] = pid
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            yield request
        pages = response.xpath('//div[@class="page"]/a/@href').extract()
        for page in pages:
            yield response.follow(page, self.parse, cookies=cookies)

    def parse_post(self, response):
        pid = response.meta['pid']
        post = PostItem(pid=pid)
        post['thumbnail'] = response.meta['thumbnail']
        post['title'] = response.xpath(
            '//div[@class="title-wrap"]/h3/text()').get()
        vid = response.selector.re_first('vid: \"(\w+)\"\,')
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource,resource_origin?'
        cates = response.xpath('//span[contains(@class, "cate")]//text()').extract()
        post['category'] = ''.join([cate.strip() for cate in cates])
        post['created_at'] = response.xpath('//span[contains(@class, "update-time")]/i/text()').get()
        post['play_counts'] = str_int(
            response.xpath('//i[contains(@class, "play-counts")]/@data-curplaycounts').get())
        post['like_counts'] = str_int(response.xpath('//span[contains(@class, "like-counts")]/@data-counts').get())
        post['description'] = strip(response.xpath('//p[contains(@class, "desc")]/text()').get())
        request = Request(video_url % vid, callback=self.parse_video)
        request.meta['post'] = post
        # yield request

        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&page=1'
        request = Request(comment_url % pid, callback=self.parse_comment)
        # yield request

        creator_list = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li')
        composer_url = 'http://www.xinpianchang.com/u%s?from=articleList'
        for creator in creator_list:
            cid = creator.xpath('./a/@data-userid').get()
            request = response.follow(composer_url % cid, self.parse_composer)
            request.meta['cid'] = cid
            request.meta['dont_merge_cookies'] = True
            # yield request

            cr = CopyrightItem()
            cr['pcid'] = '%s_%s' % (pid, cid)
            cr['pid'] = pid
            cr['cid'] = cid
            cr['roles'] = creator.xpath('./div[@class="creator-info"]/span/text()').get()
            # yield cr


    def parse_video(self, response):
        post = response.meta['post']
        result = json.loads(response.text)
        data = result['data']
        if 'resource' in data:
            post['video'] = data['resource']['default']['url']
        else:
            d = data['third']['data']
            post['video'] = d.get('iframe_url', d.get('swf', ''))
        post['preview'] = result['data']['video']['cover']
        post['duration'] = result['data']['video']['duration']
        yield post

    def parse_comment(self, response):
        result = json.loads(response.text)

        for c in result['data']['list']:
            comment = CommentItem()
            comment['uname'] = c['userInfo']['username']
            comment['avatar'] = c['userInfo']['face']
            comment['cid'] = c['userInfo']['userid']
            comment['commentid'] = c['commentid']
            comment['pid'] = c['articleid']
            comment['created_at'] = c['addtime_int']
            comment['like_counts'] = c['count_approve']
            comment['content'] = c['content']
            if c['reply']:
                comment['reply'] = c['reply']['commentid'] or 0
            yield comment
        next_page = result['data']['next_page_url']
        if next_page:
            yield response.follow(next_page, self.parse_comment)

    def parse_composer(self, response):
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer = ComposerItem()
        composer['cid'] = response.meta['cid']
        composer['banner'], = re.findall('background-image:url\((.+?)\)', banner)
        composer['avatar'] = response.xpath(
            '//span[@class="avator-wrap-s"]/img/@src').get()
        composer['name'] = response.xpath(
            '//p[contains(@class, "creator-name")]/text()').get()
        composer['intro'] = response.xpath(
            '//p[contains(@class, "creator-desc")]/text()').get()
        composer['like_counts'] = str_int(response.xpath(
            '//span[contains(@class, "like-counts")]/text()').get())
        composer['fans_counts'] = str_int(response.xpath('//span[contains(@class, "fans-counts")]/text()').get())
        composer['follow_counts'] = str_int(
            response.xpath('//span[@class="follow-wrap"]/span[last()]/text()').get())
        composer['location'] = response.xpath(
            '//span[contains(@class,"icon-location")]/'
            'following-sibling::span[1]/text()').get() or ''
        composer['career'] = response.xpath(
            '//span[contains(@class,"icon-career")]/'
            'following-sibling::span[1]/text()').get() or ''
        yield composer



