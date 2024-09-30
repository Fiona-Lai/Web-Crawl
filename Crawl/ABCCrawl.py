from time import sleep
import requests
from bs4 import BeautifulSoup
from Utils.English_Summary import English_Summary


def abc_crawl(keywords):
    search_keys = str(keywords[0])

    for i in range(1, len(keywords)):
        search_keys = search_keys + "%20" + str(keywords[i])

    url = "https://abcnews.go.com/meta/api/search?q=" + str(search_keys) + "&limit=10&sort=date&type=&section=&totalrecords=true&offset=0"
    print(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'
    }
    print(headers)
    print(url)
    print("--------------------------------------------------------------")
    resp = requests.get(url=url, headers=headers)
    return abc_parse(resp)

def abc_parse(resp):
    res = resp.json()['item']
    res_size = len(res)

    abc_content_list = []

    print("ABC 相关新闻已爬取完毕！正在处理新闻内容..")

    for i in range(0, res_size):

        content_list = []

        print("正在处理第" + str(i+1) + "号新闻")
        print("---------------------------------------------------------------------")

        title = res[i]['title']
        url = res[i]['link']
        date = res[i]['pubDate'][0:26]
        content = get_content(url)

        if content == "No":
            continue

        print(title)
        print(url)
        print(date)
        print(content)

        content_list.append("新闻标题：" + str(title) + "\n")
        content_list.append("新闻日期：" + str(date) + "\n")
        content_list.append("新闻链接：" + str(url) + "\n\n")
        content_list.append("新闻内容摘要：\n" + str(content[1]) + "\n")
        content_list.append("新闻英文摘要：\n" + str(content[0]) + "\n")
        content_list.append("---------------------------------------------------------------------"
                            "---------------------------------------------------------------------\n"
                            "---------------------------------------------------------------------"
                            "---------------------------------------------------------------------\n\n")
        print("---------------------------------------------------------------------\n")
        abc_content_list.append(content_list)

    print("***************************************************************")
    print("新闻文本处理完毕！")

    return abc_content_list


def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
    }

    print("正在获取以下链接的新闻摘要：", url)
    print("--------------------------------------------------------------")
    # urllib3.disable_warnings()
    resp = requests.get(url=url, headers=headers)
    # print(resp.text)
    bs = BeautifulSoup(resp.text, features="lxml")
    res = bs.find_all(attrs={}, class_=["fnmMv geuMB alqtB wqIGQ"])

    sentence = ""

    for item in res:
        sentence = sentence + str(item.get_text())
        print(sentence)

    if sentence == "":
        print("该新闻内容为视频，请手动进行查看！")
        return "No"
    # print("Sentences:********************************************************")
    sleep(1)
    return English_Summary(sentence)
    # print("******************************************************************")


if __name__ == '__main__':
    abc_crawl('Zero-policy')