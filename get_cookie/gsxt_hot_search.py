from selenium import webdriver
import requests
import datetime
import time
import re

def get_cookies(url):
    try:
        driver = webdriver.PhantomJS()
        # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
        driver.get(url)
        time.sleep(10)
        page_contrnt = driver.page_source.encoding('utf-8') # 婧愮爜
        return page_contrnt
    except:
        return "璇锋眰閿欒" 
        
def get_company_url(html):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d') #时间
    company = re.findall('''<div class="co1 ellipsis fl">(.*?)</div>''',html,re.S).group(1).strip() # 公司名称
    url = re.findall('''<li><i class="top4.*?href='(.*?)'>''',html,re.S).group(1).strip() # url
    print(company,url)
def main(number):
    url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=' + str(number) + '00000'
    html = get_cookies(url)
    get_company_url(html)
    
if __name__=='__main__':
    for number in range(1,2,1):
        url_error = main(number)