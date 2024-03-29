# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Field

class EversecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DouyuItem(scrapy.Item):
    title = Field()
    typeId = Field()
    authorId = Field()
    pubdate = Field()
    comments = Field()
    favorCount = Field()
    id = Field()
    author = Field()
    videoPlayNum = Field()
    name = Field()
    fans = Field()
    price = Field()
    products = Field()
    publisher = Field()
    spiderTime = Field()
    source = Field()
    url = Field()
    type = Field()
    hashVid = Field()
    share = Field()

class HuyaItem(scrapy.Item):
    title = Field()
    typeId = Field()
    authorId = Field()
    pubdate = Field()
    comments = Field()
    favorCount = Field()
    id = Field()
    author = Field()
    videoPlayNum = Field()
    name = Field()
    fans = Field()
    price = Field()
    products = Field()
    publisher = Field()
    spiderTime = Field()
    source = Field()
    url = Field()
    type = Field()


class SoftItem(scrapy.Item):
    name = Field()
    apksize = Field()
    downloadUrl = Field()
    version = Field()
    introduce = Field()
    developer = Field()
    category = Field()
    updatetime = Field()
    icon_url = Field()
    sceenshot_url = Field()
    dlamount = Field()
    shop = Field()
    url = Field()
    jsonObject = Field()
    system = Field()
    province = Field()
    city = Field()
    source = Field()

