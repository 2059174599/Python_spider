# ����1
from selenium import webdriver
import requests
import time
# �н���
def get_cookies(url):
    chrom = webdriver.Chrome()
    # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
    cookie_dict = {}
    try:
        chrom.get(url)
        time.sleep(10)
        page_contrnt = chrom.page_source # Դ��
        cookie_list = chrom.get_cookies() # cookie
        for cookie in cookie_list:
            cookie_dict[cookie['name']] = cookie['value'
        print(cookie_dict)
    except:
        pass
    finally:
        chrom.quit()
# �޽���
def get_cookies(url):
    driver = webdriver.PhantomJS()
    # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
    cookie_dict = {}
    driver.get(url)
    page_contrnt = driver.page_source # Դ��
    cookie_list = driver.get_cookies() # cookie
    for cookie in cookie_list:
        cookie_dict[cookie['name']] = cookie['value']
    print(cookie_dict)
    
# ����2
from urllib import request
from http import cookiejar
def get_cookies(url):
    # ����һ��CookieJar����ʵ��������cookie
    cookie_list = cookiejar.CookieJar()
    # ����urllib.request���HTTPCookieProcessor����������cookie������,Ҳ��CookieHandler
    handler=request.HTTPCookieProcessor(cookie_list)
    # ͨ��CookieHandler����opener
    opener = request.build_opener(handler)
    # url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000'
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
    # �˴���open��������ҳ
    response = opener.open(url)
    # ��ӡcookie��Ϣ
    for cookie in cookie_list:
        cookie_dict[cookie['name']]=cookie['value']
    print(cookie_dict)
    
    
# selenium��������
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


app = QApplication([])
view = QWebEngineView()
view.load(QUrl("http://www.taobao.com/"))
view.show()
page = view.page()
print(page)