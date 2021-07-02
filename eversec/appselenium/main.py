from appbase import Appsimulate
import time

class Wechat(Appsimulate):

    def __init__(self):
        self.appname = '微信'


    def main(self,urls):
        """
        主程序
        :return:
        """
        print(self.appname)
        # 进入微信
        self.logIn()
        # 打开传输助手页面
        self.clickIntoName('com.tencent.mm:id/he6')
        self.setText('com.tencent.mm:id/bxz', '文件传输助手')
        self.waitElement("com.tencent.mm:id/ir3")
        self.clickIntoName('com.tencent.mm:id/ir3')
        # 输入链接 点击发送
        for url in urls:
            try:
                # text(url)
                # 打开链接
                self.clickIntoText(url)
                time.sleep(20)
                self.waitElement("js_read_area3")
                print('*************')
                print('阅读',self.getText(name="js_read_area3"))
                print('点赞',self.getText(name="js_bottom_zan_btn"))
                print('在看',self.getText(name="js_like_btn"))
                # 后退
                self.waitElement("com.tencent.mm:id/ei")
                self.clickIntoName('com.tencent.mm:id/ei')
                time.sleep(5)
            except Exception as e:
                print('error {}'.format(e))
                self.waitElement("com.tencent.mm:id/ei")
                self.clickIntoName('com.tencent.mm:id/ei')
                continue


if __name__ == '__main__':
    chats = [#'http://mp.weixin.qq.com/s?__biz=MzI1OTE2NTA5MQ==&idx=3&mid=2247496338&sn=7763ce1e2576c6f006929e36525ff675',
             'http://mp.weixin.qq.com/s?__biz=MjM5MTE4MzIzNQ==&idx=2&mid=2651089349&sn=b966ef3e998479e8a10e1c6243d82ceb',
             # 'http://mp.weixin.qq.com/s?__biz=Mzg4MzU1ODE5Ng==&idx=1&mid=2247484988&sn=20e9cadb9ebdbcd6c9f0ee01b0f2a167'
             ]
    wechats = Wechat()
    wechats.main(chats)