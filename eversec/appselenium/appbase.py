from airtest.core.api import *
auto_setup(__file__)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

class Appsimulate(object):
    """
    app simulate
    """
    def __init__(self, appname='微信'):
        self.appname = appname

    def logIn(self):
        """
        1.唤醒屏幕
        2.home页
        3.打开app
        :return:
        """
        wake()
        home()
        poco(text=self.appname).click()

    def logOut(self):
        """
        退出
        :return:
        """
        pass

    def closeInform(self):
        """
        关掉通知
        :return:
        """
        pass

    def clickIntoName(self, name):
        """
        点击
        :return:
        """
        if poco(name=name).exists():
            print('元素纯在，开始点击 {}'.format(name))
            poco(name=name).click()
        else:
            print('元素不纯在，请确认：{}'.format(name))

    def clickIntoText(self, text):
        """
        点击
        :return:
        """
        if poco(text=text).exists():
            print('元素存在，开始点击 {}'.format(text))
            poco(text=text).click()
        else:
            print('元素不存在，请确认：{}'.format(text))

    def checkElement(self,name):
        """
        判断元素是否纯在
        :return:
        """
        if exists(Template(name)):
            return True
        return False

    def setText(self,name,text):
        """
        输入文本
        :return:
        """
        if poco(name=name).exists():
            poco(name=name).set_text(text)

    def waitElement(self, name):
        """
        等待某元素出现
        :param name:
        :return:
        """
        poco(name=name).wait_for_appearance()

    def getText(self, name):
        """
        返回页面元素 name 属性
        :param name:
        :return:
        """
        return poco(name=name).get_text()
    
    def operateMouse(self):
        """滑动鼠标"""
        dev = device()
        dev.mouse.scroll(coords=(0, 0), wheel_dist=-1)