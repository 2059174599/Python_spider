# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tag = scrapy.Field()
    lg_company_url = scrapy.Field()
    company_url = scrapy.Field()
    company_word = scrapy.Field()
    img_log = scrapy.Field()


class JdcomentItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    Comment = scrapy.Field()
    LevelName = scrapy.Field()
    url = scrapy.Field()