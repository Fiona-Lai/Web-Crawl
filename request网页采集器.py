#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

if __name__ == "__main__":
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
    }
    url = 'https://www.foxnews.com/search-results/search?'
    keyword = input('Enter a word:')
    param = {
        'q':keyword
    }
    response = requests.get(url=url,params=param,headers=headers)
    page_text = response.text
    FileName = keyword + '.html'
    with open(FileName,'w',encoding='utf-8') as fp:
        fp.write(page_text)
    print(FileName,'保存成功！')