import requests
import traceback
import random
import re
import json

class BaseRequest(object):
    """
    请求类
    """
    def __init__(self, meth='get', timeout=3, cookies=None, url='https://www.baidu.com/'):
        self.meth = meth
        self.timeout = timeout
        self.url = url
        self.cookies = cookies

    def request(self):
        headers = self.getHeaders()
        try:
            # print(self.url, headers, self.timeout)
            r = requests.get(self.url, headers=headers, timeout=self.timeout)
            # r.raise_for_status()
            # r.encoding = r.apparent_encoding
            return r.text
        except:
            traceback.print_exc()
            return "请求错误"

    def getHeaders(self):
        head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                            # 'okhttp/3.10.0.1',
                            # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
                            ]
        if not self.cookies:
            return {'User-Agent': random.choice(head_user_agent)}
        else:
            return {'User-Agent': random.choice(head_user_agent),
                    'cookies': self.cookies
                    }

def checkStartUrl(url):
    """
    检测分享页url是否符合要求
    :param url:
    :return:
    """
    if re.search('mid=\d{19}|video\/\d{19}',url):
        return True
    return False

def readFile(files):
    with open(files, 'r', encoding='utf-8') as f:
        # for i in f:
        #     yield i
        for i in json.loads(f.read())['hits']['hits']:
            yield i['_source']['ir_urlname_key']
if __name__ =='__main__':
    # base = BaseRequest(url='https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=6923835539430952206')
    # print(base.request())
    for i in readFile('抖音.txt'):
        print(i)