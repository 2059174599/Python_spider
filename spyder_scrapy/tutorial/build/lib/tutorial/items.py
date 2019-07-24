# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    tag = scrapy.Field()
# 因果树
class InnoItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    company_money = scrapy.Field()
    url = scrapy.Field()
    company_person = scrapy.Field()
    company_abstract = scrapy.Field()
    imge = scrapy.Field()
    company_location = scrapy.Field()