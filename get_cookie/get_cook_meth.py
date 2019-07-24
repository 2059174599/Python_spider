# 方法1
from selenium import webdriver
import requests
import time
# 有界面
def get_cookies(url):
    chrom = webdriver.Chrome()
    # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
    cookie_dict = {}
    try:
        chrom.get(url)
        time.sleep(10)
        page_contrnt = chrom.page_source # 源码
        cookie_list = chrom.get_cookies() # cookie
        for cookie in cookie_list:
            cookie_dict[cookie['name']] = cookie['value'
        print(cookie_dict)
    except:
        pass
    finally:
        chrom.quit()
# 无界面
def get_cookies(url):
    driver = webdriver.PhantomJS()
    # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
    cookie_dict = {}
    driver.get(url)
    page_contrnt = driver.page_source # 源码
    cookie_list = driver.get_cookies() # cookie
    for cookie in cookie_list:
        cookie_dict[cookie['name']] = cookie['value']
    print(cookie_dict)
    
# 方法2
from urllib import request
from http import cookiejar
def get_cookies(url):
    # 声明一个CookieJar对象实例来保存cookie
    cookie_list = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler=request.HTTPCookieProcessor(cookie_list)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
    # 此处的open方法打开网页
    response = opener.open(url)
    # 打印cookie信息
    for cookie in cookie_list:
        cookie_dict[cookie['name']]=cookie['value']
    print(cookie_dict)
    
    
# selenium反爬问题
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


app = QApplication([])
view = QWebEngineView()
view.load(QUrl("http://www.taobao.com/"))
view.show()
page = view.page()
print(page)