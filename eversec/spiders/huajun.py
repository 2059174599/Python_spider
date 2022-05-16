from collections import defaultdict
import scrapy
import re
import time
import logging


logger = logging.getLogger(__name__)


class HuaJunSpider(scrapy.Spider):
    """
    默认新数据在前页
    """

    name = 'huajun_pc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    def __init__(self):
        self.page = 2
        self.start_urls = ['https://www.onlinedown.net/new/android/' + str(i) for i in range(self.page)]
        self.page_urls = 'https://www.onlinedown.net/new/android/{}'
        self.start_page_url = 1
        self.local_url = 'https://app.eversaas.cn/service/app-ops/gaodeinfo?str={}'
        self.html_url = 'https://shouji.baidu.com/{}'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.list_url)

    def parse(self, response):
        """
        获取类别规则
        """
        for url in response.xpath('//div[@class="g-map"]/div[2]/div[2]/div/a/@href').getall()[:2]:
            logger.info('链接：{}'.format(url))
            yield scrapy.Request(url=url, callback=self.page_url)

    def page_url(self, response):
        """
        获取页码规则
        """
        ids = response.xpath('//div[@class="g-pages"]/a[last()-1]/text()').get()
        if ids:
            ids = int(ids)
        else:
            ids = 1
        ids = self.page if self.page else ids
        logger.info('页码：{}'.format(ids))
        for i in range(1, ids+1):
            url = response.url + '/{}/'.format(i)
            logger.info('列表页url：{}'.format(url))
            yield scrapy.Request(url=url, callback=self.list_url)

    def list_url(self, response):
        """
        获取列表页规则
        """
        for url in response.xpath('//tbody/tr/td[2]/a/@href').getall():
            logger.info('详情页url：{}'.format(url))
            yield scrapy.Request(url=url, callback=self.shop_html)

    def shop_html(self, response):

        """
        http://192.168.101.31:8181/docs/app-security/app-security-1ci4upcotsua0
        """
        item = defaultdict(str)
        item['name'] = response.xpath('//h1/text()').get().strip().replace('\xa0\xa0', ' ')
        item['apksize'] = re.search(r'软件大小.*?<span>(.*?)</', response.text, re.S).group(1)
        item['downloadUrl'] = response.xpath('//*[@id="downBox"]/div/div[1]/p/a[1]/@href').get()
        item['version'] = re.search(r'安卓版(.*?)</', response.text).group(1).strip()
        item['introduce'] = response.xpath('//*[@id="ItemRJJS"]/div[2]/div/text()').get().strip()
        item['developer'] = ''
        item['category'] = '游戏'
        item['updatetime'] = re.search(r'更新时间.*?<span>(.*?)</', response.text, re.S).group(1).strip()
        item['icon_url'] = response.xpath('//*[@id="ItemRJJS"]/div[2]/div/p[1]/img/@src').get()
        item['sceenshot_url'] = []
        item['shop'] = '华军软件园'
        item['system'] = 'android'
        item['dlamount'] = 0
        item['url'] = response.url
        item['jsonObject'] = {'time': time.strftime("%Y-%m-%d", time.localtime())}
        logger.info('数据：{}'.format(item['name']))
        # print(item)
        yield item