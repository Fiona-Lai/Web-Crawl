import datetime
import sys
from Crawl.ABCCrawl import abc_crawl
from Crawl.CNNCrawl import cnn_crawl

if __name__ == '__main__':
    keys = sys.argv
    print("您正在以以下内容为关键词搜索新闻：\n", keys[1:])

    keywords = ""

    for item in keys:
        keywords = keywords + item

    now_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    path = './Data/'
    file_name = path + now_time + keywords + '.doc'
    file = open(file_name, "w", encoding='utf-8')

    index = 0

    cnn_news = cnn_crawl(keys[1:])

    print("CNN 相关新闻搜索完毕，正在写入文件...")
    print("---------------------------------------------------------------------\n\n")

    for items in cnn_news:
        index = index + 1
        file.write("新闻编号：" + str(index) + "\n")
        for item in items:
            file.write(item)

    abc_news = abc_crawl(keys[1:])

    print("ABC 相关新闻搜索完毕，正在写入文件...")
    print("---------------------------------------------------------------------\n\n")

    for items in abc_news:
        index = index + 1
        file.write("新闻编号：" + str(index))
        for item in items:
            file.write(item)

    file.close()

    print("*************************************************************************")

    print("相关新闻搜索完毕！" + "\n搜索结果输出路径为：" + str(file_name))