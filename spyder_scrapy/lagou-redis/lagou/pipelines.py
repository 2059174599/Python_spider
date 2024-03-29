# -*- coding: utf-8 -*-

# Define your item pipelines here
import scrapy
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import json
import codecs
from scrapy.exceptions import DropItem
import re
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class LagouPipeline(ImagesPipeline):
#     # def process_item(self, item, spider):
#     #     # item = request.meta['item']
#     #     # # return item
#     #     # print(item)
#     #     return item
#     def get_media_requests(self, item, info):
#     	# item = request.meta['item']
#     	print(item)


class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 下载图片，如果传过来的是集合需要循环下载
        # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
        img_url = item['img_log']
        if '?' in img_url:
        	sub = re.search(r'\?(.*)',img_url).group() 
        	item['img_log'] = img_url.replace(sub,'')
        yield Request(url=item['img_log'],meta={'item':item})

    def item_completed(self, results, item, info):
        # 是一个元组，第一个元素是布尔值表示是否成功
        if not results[0][0]:
            raise DropItem('下载失败')
        return item

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        # name = request.meta['name']
        # # 提取url前面名称作为图片名
        # image_name = request.url.split('/')[-1]
        # # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        # folder_strip = re.sub(r'[？\\*|“<>:/]', '', str(name))
        # # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        # filename = u'{0}/{1}'.format(folder_strip, image_name)
        filename = request.url.split('/')[-1] 
        return filename