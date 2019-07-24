# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
from lagou.items import JdcomentItem
import requests
import random
import scrapy
import time
import json
import re


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['www.jd.com']
    #start_urls = ['https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1106&productId=100002105259&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&fold=1']

    def parse(self, response):
    	item = JdcomentItem()
    	html_comments = re.search(r'"comments":(.*?)}\);',response.text,re.S).group(1)
    	data=json.loads(html_comments)
    	#item['url'] = response.url
    	for html_comment in data:
    		item['name'] = html_comment["nickname"]
    		item['Comment'] = html_comment["showOrderComment"]
    		item['LevelName'] = html_comment["userLevelName"]
    		item['url'] = response.url
    		yield item

    def start_requests(self):
    	for i in range(100,300000):
	    	url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1106&productId=100002105259&score=0&sortType=5&page=1&pageSize='\
	    		   + str(i) + '0&isShadowSku=0&fold=1'
	    	#ip = requests.get('http://localhost:5555/random').text
	    	#print(ip,'*'*10)
	    	headers = {
	    				'UserAgent' : UserAgent().random
	    			}
	    	time.sleep(random.randint(1,5))
	    	yield scrapy.Request(url=url, headers=headers,callback=self.parse)