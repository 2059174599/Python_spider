import json
from collections import defaultdict
import scrapy
import re
import time
import logging
import logging.handlers
import requests
import os

logger = logging.getLogger(__name__)


class AnktySpider(scrapy.Spider):
    """
    默认新数据在前页
    """

    name = 'ipinfo'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'referer': 'https://ipinfo.io/',
    }

    def __init__(self):
        self.start_urls = ['https://danger.rulez.sk/projects/bruteforceblocker/blist.php', 'https://myip.ms/files/blacklist/htaccess/latest_blacklist.txt']
        self.page_urls = 'https://shouji.baidu.com/{}'
        self.start_page_url = 1
        self.local_url = 'https://app.eversaas.cn/service/app-ops/gaodeinfo?str={}'
        # 排序
        self.page = None
        self.html_url = 'https://www.hybrid-analysis.com{}'
        self.down_url = 'https://www.xuanbiaoqing.com/api/show_download_url/{}'
        self.name = os.path.basename(__file__).split(".")[0] + '_' + str(time.strftime("%Y-%m-%d", time.localtime())) + '.json'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.get_ip)

    def get_ip(self, response):
        """
        获取类别规则
        """
        pattern = re.compile(r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})')
        ips = pattern.findall(response.text)
        for i in ips[:3]:
            url = 'https://ipinfo.io/widget/demo/{}'.format(i[0])
            yield scrapy.Request(url=url, headers=self.headers, callback=self.shop_html)

    def page_url(self, response):
        """
        获取页码规则
        """
        ids = response.xpath('//ul[@class="pagination"]/li[last()-1]/a/text()').get()
        logger.info('ids:{}'.format(ids))
        if ids:
            ids = int(ids)
        else:
            ids = 1
        ids = self.page if self.page else ids
        for i in range(1, ids+1):
            url = response.url + '?sort=timestamp&sort_order=desc&page={}'.format(i)
            logger.info('列表页url：{}'.format(url))
            yield scrapy.Request(url=url, callback=self.shop_html)

    def list_url(self, response):
        """
        获取列表页规则
        """
        for i in response.xpath('/html/body/div[3]/div/div[1]/div/a/@href').getall():
            url = self.html_url.format(i)
            logger.info('详情页url：{}'.format(url))
            yield scrapy.Request(url=url, callback=self.shop_html)

    def getRe(self, parament, html):
        try:
            res = re.search(parament, html).group(1)
        except Exception as e:
            logging.error('正则：{}, {}'.format(parament, e))
            res = ''
        return res

    def getDown(self, url):
        id = url.split('/')[-1].split('.')[0]
        r = requests.get(self.down_url.format(id), headers=self.headers).text
        downUrl = self.getRe('href="(.*?)"', r)
        return downUrl

    def saveResult(self, path, item):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(item+'\n')

    def shop_html(self, response):
        item = response.json
        self.saveResult('../result/{}'.format(self.name), json.dumps(item, ensure_ascii=False))
