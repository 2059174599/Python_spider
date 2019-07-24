# -*- coding: utf-8 -*-
#from scrapy.conf import settings
from tutorial.items import InnoItem
import scrapy
import re


class InnoSpider(scrapy.Spider):
    name = 'Inno'
    allowed_domains = ['www.innotree.cn']
    start_urls = ['https://www.innotree.cn/inno/search/ajax/getAllSearchResult?query=&tagquery=&st=1&ps=10&areaName=&rounds=&show=0&idate=&edate=&cSEdate=-1&cSRound=-1&cSFdate=1&cSInum=-1&iSNInum=1&iSInum=-1&iSEnum=-1&iSEdate=-1&fchain=']
    headers = {
    'Connection': 'keep - alive',  # 保持链接状态
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Cookie': '__user_identify_=18258542-375d-38f1-8b0e-c9157b813a91; JSESSIONID=aaa-Ve0-_gmsPcmbcdXBw; uID=436669; sID=3f9a676b7694fa692fbe77baf844cc8f; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1541642366,1541666637,1541671095,1541730075; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1541642366,1541666637,1541671095,1541730075; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1541730079; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1541730079'
    }
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],headers=self.headers)
    def parse(self, response):
        url = re.findall(r'''ncid\\":\\"(.*?)\\",\\"address''',response.text,re.S)
        for i in url:
            i = 'https://www.innotree.cn/inno/company/' + i + '.html'
            #print(i)
            yield scrapy.Request(url=i,callback=self.cont_parse,headers=self.headers)
        #print(i)    
    def cont_parse(self, response):
        item = InnoItem()
        #res = requests.get(response.url, headers=self.headers)
        company_infor = response.xpath('//div[@class="de_170822_d01_d"]//span/text()').extract() # 基本信息
        com_brief = response.xpath('////div[@class="de_170822_d01_d02"]/p/text()').extract() # 公司简介
        imge = response.xpath('//div[@class="mech_170525_nav"]//tr/td/img/@src').extract()
        if 'http' not in imge[0]:
            imge = ['https://www.innotree.cn' + imge[0]]
        item['url'] = response.url
        item['company_name'] = company_infor[1]
        item['company_money'] = company_infor[3]
        item['company_location'] = company_infor[5]
        item['company_person'] = company_infor[7]
        item['company_abstract'] = com_brief[0]
        item['imge'] = imge[0]
        yield item