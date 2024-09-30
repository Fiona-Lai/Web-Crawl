# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import concurrent.futures

def def_response(url_s):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(url_s, headers=headers)
    return response

def save(title_li, text):
	# 声明编码，不然会报错
    with open('./x.text', mode='a', encoding='utf-8')as f:
        f.write(title_li + '\n\n')
        f.write(text + '\n\n')
        # 因为保存在一个文件中，所以这里用*号进行隔开
        f.write('*' * 50 + '\n\n')#

def main(html_url):
    response = def_response(html_url)
    href = re.findall('data-id="(.*?)"', response.text)
    title = re.findall('alt="(.*?)"', response.text)
    for url_li, title_li in zip(href, title):
    	# 拼接链接
        url_ = f'https://www.thepaper.cn/newsDetail_forward_{url_li}'
        res = def_response(url_)
        etrees = etree.HTML(res.text)
        # 这里用xpath提取文本内容，但是格式有点乱，所以用'\n\n'.join进行换行
        text = '\n\n'.join(etrees.xpath('.//div[@class="news_txt"]/text()'))
        save(title_li, text)

if __name__ == '__main__':
    # ThreadPoolExecutor 线程池的对象 max_workers  任务数 这里开了3个
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    for page in range(0, 4):
        url = f'https://www.thepaper.cn/load_index.jsp?nodeids=25462&topCids=&pageidx={page}&isList=true'
        # main(url)
        # submit  往线程池里面添加任务
        executor.submit(main, url)
    executor.shutdown()
