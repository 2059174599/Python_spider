import scrapy
import re
from tutorial.items import TutorialItem

class DmozSpider(scrapy.Spider):
    name = 'quotes'
    #allowed_domains = ['quotes.toscrape.com']
    pag = 1
    baseurl = 'http://quotes.toscrape.com/page/'
    start_urls = [
        baseurl + str(pag)
    ]
    def parse(self, response):
        #print(type(response.text))
        #url = re.findall(r'''<h1>(.*?)</h1>''',response.body.decode(),re.S)
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
            # f.write(response.body)
        # self.log('Saved file %s' % filename)
        for i in response.xpath('//div[@class="quote"]'):
            item = TutorialItem()
            item['title'] = i.xpath('span[@class="text"]/text()').extract()[0]
            item['link'] = i.xpath('span/a/@href').extract()[0]
            item['tag'] = str(i.xpath('div/a/text()').extract())
        # item['tag'] = url
        #print(url)
            yield item  
        if self.pag < 3:
            self.pag += 1
            url = self.baseurl + str(self.pag)
            yield scrapy.Request(url,callback=self.parse)