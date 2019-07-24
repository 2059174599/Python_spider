# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy.conf import settings
import pymongo
import pymysql
import pymysql.cursors
import json 
class TutorialPipeline(object):
    # def __init__(self):
        # self.f = open('quotes.json','w')
    def __init__(self, dbpool):
        self.dbpool = dbpool
        port = settings['MONGODB_PORT']
        host = settings['MONGODB_HOST']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    #链接数据库
    @classmethod
    def from_settings(cls, settings):
        param = dict(
            host = 'localhost',
            db = 'sys',
            user = 'wxy',
            password = '66357070',
            port = 3306,
            charset = "utf8",
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("pymysql",**param)
        return cls(dbpool)  
    def process_item(self, item, spider):
        if spider.name == 'Inno':
            print('已执行' + spider.name)
            #使用twisted将mysql插入异步化
            query = self.dbpool.runInteraction(self.do_insert,item)
            query.addErrback(self.handle_error) #处理异常
            return item
        else:
            book_info = dict(item)
            self.post.insert(book_info)
            print('已执行' + spider.name)
            return item
    def handle_error(self, failure):
        #处理异步插入错误
        print(failure)
    def do_insert(self, cursor, item):
        print('开始执行mysql')
        insert_sql = "insert into Inno(company_name,company_abstract,imge,url) \
                      values (%s,%s,%s,%s)"
        cursor.execute(insert_sql, (item["company_name"],item["company_abstract"],item["imge"],item["url"]))
    # def close_spider(self, spider):
        # self.f.close()    