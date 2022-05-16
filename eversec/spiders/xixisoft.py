from collections import defaultdict
import scrapy
import re
import time
import logging

from eversec.items import SoftItem

logger = logging.getLogger(__name__)


class XiaoMiGameSpider(scrapy.Spider):
    """
    默认新数据在前页
    """
    name = 'xixi'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    def __init__(self):
        # self.name = 'xixi'
        self.start_urls = ['https://www.cr173.com/new/']
        self.page_urls = 'https://game.xiaomi.com/api/classify/getCategory?firstCategory=&secondCategory=&apkSizeMin=0&apkSizeMax=0&language=&network=-1&options=&page={}&gameSort=1'
        self.down_url = 'https://gyxz2.243ty.com/{}'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        获取软件、游戏
        """
        softIds = re.findall('</a><a href="/soft/(.*?).html', response.text)
        softIds = ['https://www.cr173.com/soft/{}.html'.format(i) for i in softIds]
        gameIds = re.findall('</a><a href="/azyx/(.*?).html', response.text, re.S)
        gameIds = ['https://www.cr173.com/azyx/{}.html'.format(i) for i in gameIds]
        urls = softIds + gameIds
        for url in urls[:5]:
            logger.info('url'.format(id))
            yield scrapy.Request(url=url, callback=self.shop_html)

    def fit_platform(self, response):
        """
        获取详情页url规则
        """
        platfrom = re.search('应用平台:</span><b>(.*?)</b>', response.text, re.S).group(1)
        print(platfrom)
        # ids = set(re.findall(r'gameId":(.*?),', response.text))
        # urls = [self.html_url.format(i) for i in ids]
        # for url in urls:
        #     logger.info('详情页url：{}'.format(url))
        #     yield scrapy.Request(url=url, callback=self.shop_html)

    def getRe(self, strs, html):
        try:
            return re.search(strs, html).group(1)
        except:
            return ''

    def shop_html(self, response):

        """
        http://192.168.101.31:8181/docs/app-security/app-security-1ci4upcotsua0
        """
        platfrom = re.search('应用平台:</span><b>(.*?)</b>', response.text, re.S).group(1).strip()
        if platfrom.upper() == 'ANDROID':
            item = SoftItem()
            # sceenshot_html = re.search(r'<div class="current-view__view-wrap">(.*?)<div id="pic_border', response.text).group(1)
            item['name'] = response.xpath('//h1/text()').get().strip()
            item['apksize'] = self.getRe(r'软件大小:</span><b class="m-size">(.*?)</', response.text)
            item['downloadUrl'] = self.down_url.format(re.search(r'Address:"(.*?)"', response.text).group(1))
            item['version'] = ''
            item['introduce'] = response.xpath('//*[@id="content"]/p[1]/text()').get()
            item['developer'] = re.search(r'软件厂商:</span><b>(.*?)</', response.text).group(1)
            item['category'] = '游戏'
            item['updatetime'] = re.search(r'更新时间:</span><b>(.*?)</', response.text).group(1)
            item['icon_url'] = response.xpath('//*[@id="content"]/p[2]/img/@src').get()
            item['sceenshot_url'] = response.xpath('//*[@id="screen_show"]/div/a/@href').getall()
            # item['sceenshot_url'] = ['https:' + i for i in re.findall(r'src="(.*?)"', sceenshot_html)]
            item['shop'] = '西西软件园'
            item['dlamount'] = 0
            item['system'] = 'android'
            item['url'] = response.url
            item['jsonObject'] = {'time': time.strftime("%Y-%m-%d", time.localtime())}
            logger.info('数据：{}'.format(item['name']))
            yield dict(item)