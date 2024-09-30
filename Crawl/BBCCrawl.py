import requests
from bs4 import BeautifulSoup
from lxml.html.builder import HTML


def washingtonpost_crawl():

    url = "https://search.globaltimes.cn/QuickSearchCtrl"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
    }

    print(headers)
    print(url)
    print("--------------------------------------------------------------")
    # urllib3.disable_warnings()
    resp = requests.get(url=url, headers=headers)
    print(resp.text)



if __name__ == '__main__':
    washingtonpost_crawl()
