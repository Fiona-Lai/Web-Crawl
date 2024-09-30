import requests
import sys
import json
from Utils.English_Summary import English_Summary

def fox_crawl(keywords):

    url = "https://api.foxnews.com/search/web?q=" + str(keywords) + "+-filetype:amp+-filetype:xml+more:pagemap:metatags-prism.section&siteSearch=foxnews.com&siteSearchFilter=i&callback=__jp0"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }

    resp = requests.get(url=url, headers=headers)
    print(resp.text)
    print(resp.text[22:-2])
    cnn_parse(resp)

def cnn_parse(resp):

    res = json.loads(resp.text[22:-2])['items']
    print(res)
    res_size = len(res)

    cnn_docx_list = []

    print("Fox News 相关新闻已爬取完毕！正在处理新闻内容..")

    for i in range(1,res_size):
        content_list = []

        print("当前正在处理第" + str(i) + "个新闻内容，它的大致信息如下所示：")

        title = res[i]['title']
        print("新闻标题：" + str(title))
        content_list.append("新闻标题：" + str(title) + "\n")

        date = res[i]['pagemap']['metags'][0]['dc.date']
        print("新闻日期：" + str(date))
        content_list.append("新闻日期：" + str(date) + "\n")

        url = res[i]['link']
        print("新闻链接：" + str(url))
        content_list.append("新闻链接：" + str() + "\n\n")

        cnn_docx_list.append(content_list)

    print("***************************************************************")
    print("新闻文本处理完毕！")

    return cnn_docx_list


if __name__ == '__main__':
    # keys = sys.argv
    # print("您正在以以下内容为关键词搜索新闻：\n", keys[1:])

    fox_crawl("Biden")