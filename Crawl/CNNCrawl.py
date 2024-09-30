import sys
import requests
import datetime
from Utils.English_Summary import English_Summary


def cnn_crawl(keywords):

    search_keys = str(keywords[0])

    for i in range(1, len(keywords)):
        search_keys = search_keys + "%20" + str(keywords[i])

    url = 'https://search.api.cnn.com/content?size=10&q=' + str(search_keys)
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }

    resp = requests.get(url=url, headers=headers)

    print_doc(resp, search_keys)
    return cnn_parse(resp)


def cnn_parse(resp):

    res = resp.json()['result']
    res_size = len(res)

    index = 0
    cnn_docx_list = []

    print("CNN 相关新闻已爬取完毕！正在处理新闻内容..")

    for i in range(0, res_size):
        index = index + 1
        content_list = []

        print("当前正在处理第" + str(index) + "个新闻内容，它的大概信息如下所示：")

        title = res[i]['headline']
        print("新闻标题：" + title)
        content_list.append("新闻标题：" + str(title) + "\n")
        date = res[i]['firstPublishDate'][0:10]
        print("新闻日期：" + date)
        content_list.append("新闻日期：" + str(date) + "\n")
        url = res[i]['url']
        print("新闻链接：" + url)
        content_list.append("新闻链接：" + str(url) + "\n\n")
        content = English_Summary(res[i]['body'])
        print(content)
        content_list.append("新闻内容摘要：\n" + str(content[1]) + "\n")
        content_list.append("新闻英文摘要：\n" + str(content[0]) + "\n")
        content_list.append("---------------------------------------------------------------------"
                            "---------------------------------------------------------------------\n"
                            "---------------------------------------------------------------------"
                            "---------------------------------------------------------------------\n\n")
        print("---------------------------------------------------------------------\n")

        cnn_docx_list.append(content_list)

    print("***************************************************************")
    print("新闻文本处理完毕！")

    return cnn_docx_list


def print_doc(resp, keyswords):
    res = resp.json()['result']
    res_size = len(res)
    now_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    path = '../Data/'
    file_name = path + now_time + '_CNN_' + keyswords + '.doc'
    file = open(file_name, "w", encoding='utf-8')
    print("关键词相关新闻搜索完毕，正在处理新闻内容...")
    print("---------------------------------------------------------------------\n\n")
    index = 0
    for i in range(0, res_size):
        index = index + 1
        print("当前正在处理第" + str(index) + "个新闻内容，它的大概信息如下所示：")
        title = res[i]['headline']
        print("新闻标题：" + title)
        file.write("新闻标题：" + str(title) + "\n")
        date = res[i]['firstPublishDate'][0:10]
        print("新闻日期：" + date)
        file.write("新闻日期：" + str(date) + "\n")
        url = res[i]['url']
        print("新闻链接：" + url)
        file.write("新闻链接：" + str(url) + "\n\n")
        content = English_Summary(res[i]['body'])
        print(content)
        file.write("新闻内容摘要：\n" + str(content) + "\n")
        file.write("---------------------------------------------------------------------"
                   "---------------------------------------------------------------------\n"
                   "---------------------------------------------------------------------"
                   "---------------------------------------------------------------------\n\n")
        print("---------------------------------------------------------------------\n")
    print("***************************************************************")
    print("新闻文本处理完毕！" + "\n输出路径为：" + str(file_name))
    file.close()


if __name__ == '__main__':
    keys = sys.argv
    print("您正在以以下内容为关键词搜索新闻：\n", keys[1:])

    cnn_crawl(keys[1:])