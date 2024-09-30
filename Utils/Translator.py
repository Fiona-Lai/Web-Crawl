import hashlib
import random
from time import sleep

import requests

#使用百度开放API完成翻译模块
class Translator:
    def __init__(self):
        self.appid = '20220613001247137'
        self.from1 = 'en'
        self.to = 'zh'
        self.q = ''
        self.salt = str(random.randint(32768, 65536))
        self.appkey = 'XjQgyms8Hw3mNDjUsn7E'

    def encry(self):
        self.text = self.appid + self.q + self.salt + self.appkey
        hl = hashlib.md5()
        hl.update(self.text.encode(encoding='utf8'))
        md5 = hl.hexdigest()
        return md5

    def translate(self, text):
        # print("翻译内容为：", text)
        self.q = text
        sign = self.encry()
        # url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=" + self.q + "&from=" + self.from1 + "&to=" + self.to + "&appid=" + self.appid + "&salt=" + self.salt + "&sign=" + sign
        url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
        params = {
            "q": self.q,
            "from": self.from1,
            "to": self.to,
            "appid": self.appid,
            "salt": self.salt,
            "sign": sign
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        re = requests.post(url, params=params, headers=headers)
        # 限制get方法的访问频率
        sleep(1)
        # print(re.text)
        res = re.json()["trans_result"][0]["dst"]
        return res


if __name__ == '__main__':

    s = 'Only once since 2000 has the Fed raised rates by that much, last month.Surging prices and expectations about Fed policy have sent the two-year Treasury yield to its highest level since 2008 and the S&P 500 down 18.7% from its record set in early January.'


    translator = Translator()

    for i in range(1, 2):
        print(translator.translate(s))

