# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MonitorUser(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    mid = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    type = scrapy.Field()
    follow_num = scrapy.Field()
    fan_num = scrapy.Field()
    level = scrapy.Field()
    address = scrapy.Field()
    school = scrapy.Field()
    introduction = scrapy.Field()
    v_flag = scrapy.Field()
    v_info = scrapy.Field()
    img_url = scrapy.Field()


class Article(scrapy.Item):
    aid = scrapy.Field()
    uid = scrapy.Field()
    mid = scrapy.Field()
    title = scrapy.Field()
    rdate = scrapy.Field()
    summary = scrapy.Field()
    full_text = scrapy.Field()
    url = scrapy.Field()
    relate_tju = scrapy.Field()
