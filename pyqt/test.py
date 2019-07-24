import bs4 as bs
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        # print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    page = Page('http://www.gsxt.gov.cn/corp-query-entprise-info-hot-search-list.html?province=100000')
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    print(page.html)
    js_test = soup.find('p', class_='line2')
    print(soup)


if __name__ == '__main__':
    main()