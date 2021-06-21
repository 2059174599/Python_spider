from setting import DY_URLS
from base import BaseRequest, readFile, checkStartUrl
from parameter import get_encryption_obj
import requests, urllib.parse
import json
from collections import defaultdict
import datetime
import logging


class DouyinSpider(object):
    """
    抖音爬虫
    """
    def __init__(self, url, files='result.json'):
        # https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6974611041405717764
        # https://www.amemv.com/share/video/6974611041405717764/?mid=6974611041405717764
        # self.url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'.format(url.split('mid=')[-1])
        self.files = files
        self.start_url = url
        self.url = '{}?aweme_id={}'.format(DY_URLS['dy_share_url'], url.split('mid=')[-1])

    def linkAnaly(self):
        """
        链接页信息
        点赞 评论 sec_uid等
        :return:
        """
        base = BaseRequest(url=self.url)
        res_json = json.loads(base.request())
        logging.info('链接页url:{} {}'.format(self.url, res_json))
        item = res_json['aweme_detail']['statistics']
        item['sec_uid'] = res_json['aweme_detail']['author']['sec_uid']
        return item

    def personAnaly(self, item):
        """
        主页信息
        粉丝 关注 作品等
        :param item:
        :return:
        """
        person_url = '{}?sec_uid={}'.format(DY_URLS['dy_person_url'], item['sec_uid'])
        base = BaseRequest(url=person_url)
        res_json = json.loads(base.request())['user_info']
        logging.info('个人页url:{} {}'.format(person_url, res_json))
        item['nickname'] = res_json['nickname']
        item['following_count'] = res_json['following_count']
        item['follower_count'] = res_json['follower_count']
        item['total_favorited'] = res_json['total_favorited']
        return item

    def saveResult(self, item):
        """
        存储结果
        :param item:
        :return:
        """
        # sql or files
        with open(self.files, 'a', encoding='utf-8') as f:
            res = json.dumps(item) + '\n'
            f.write(res)

    def getResult(self, item):
        """
        | diggCount      | String   | 否   | 点赞数     
        | commentCount   | String   | 否   | 评论数     
        | followingCount | String   | 否   | 粉丝数     
        | forwardCount   | String   | 否   | 转发量(微博)        
        | playCount      | String   | 否   | 播放量/浏览量(快手) 
        | readCount      | String   | 否   | 阅读量（微信公众号）
        | stayReadCount  | String   | 否   | 再看量（微信公众号） 
        :param item: 
        :return: 
        """
        result = defaultdict(str)
        result['crawlTime'] = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        result['relationUrl'] = self.start_url
        result['source'] = 1
        result['diggCount'] = item['digg_count']
        result['commentCount'] = item['comment_count']
        result['followingCount'] = item['digg_count']
        return result

    def main(self):
        linkDetail = self.linkAnaly()
        item = self.personAnaly(linkDetail)
        result = self.getResult(item)
        self.saveResult(result)
        # return result

if __name__ =='__main__':
    # logging.basicConfig(level=logging.INFO,
    #                     filename='output.log',
    #                     datefmt='%Y/%m/%d %H:%M:%S',
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler('output.log',encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger = logging.getLogger(__name__)
    for urlname_key in readFile('抖音.txt'):
        try:
            if checkStartUrl(urlname_key):
                douyin = DouyinSpider(urlname_key)
                douyin.main()
            else:
                logging.error('起始url不符合规范：{}'.format(urlname_key))
        except Exception as e:
            logging.error('异常请求:{}'.format(urlname_key))
            continue

    # douyin = DouyinSpider(DY_URLS['ir_urlname_key'])
    # print(douyin.main())
