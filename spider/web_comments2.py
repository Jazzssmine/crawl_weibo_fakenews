import pandas as pd
import math
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import urllib
import re
import unidecode
import time
import requests
from requests import Request, Session

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari / 537.36'
}
cookie = {
    'ALF': '1569558716',
    'SCF': 'Am7Jt7ySAY5qGVf-9s3G4Of_Q9InAuL_1ZZY7JWBEh1EiWnBRLXtcSh1nR4wbrIyDDff11BLAnQju0tu2lJWWvw.',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJcHiLLQYmQJX._sM6GNLg5JpX5KzhUgL.FoeX1h-7ehMcehM2dJLoIN-LxKMLB.zL1hnLxKBLB.2L12-LxK-L12qLB-qLxKBLB.zLBK-LxKqL1KBLBo.LxK-L1K5L12BLxKBLB.2L1hqLxK-L12qL1hnLxKnLBKqL1h2LxK-L1K5L12-LxKqL1hzL1KBLxKBLBonL1h5LxK-LBo.LBoBt',
    '_T_WM': '61257250789',
    'SUB': '_2A25wYnR2DeRhGeVK41cR8CnKyzuIHXVTrRw-rDV6PUJbkdBeLVeskW1NTCdnposyBx280rTF2p9x6qqSkZWoX8eQ',
    'SUHB': '0YhRmMMZUqsJLt'
}

crawl_path = []
for i in range(0, 50):
    crawl_path.append('crawl_data/text_data' + str(i) + '.csv')

for j in range(0, 5):
    crawl_data = pd.read_csv(crawl_path[j])
    weibo_content = []
    repost_num = []
    thumbs_num = []
    comment_num = []
    comments_all = []
    for i in range(0, 20):
        print(i)
        url = crawl_data['link_to_post'][i]
        if url != 'nn':
            r = requests.get(url, cookies=cookie)
            content = r.text
            soup = BeautifulSoup(content, 'lxml')

            ##微博内容
            for item in soup.select('div[class="c"] div span[class="ctt"]'):
                weibo_content.append(item.get_text())
                # print(weibo_content)

            ##转发
            for item in soup.findAll("a", {"href": re.compile("\/repost\/(.+)")}):
                repost = re.findall(r'[0-9]+', str(item.get_text()))
                if len(repost) == 0:
                    repost_num.append('0')
                else:
                    repost_num.append(repost[0])
                # print(repost_num)

            ##赞
            for item in soup.findAll("a", {"href": re.compile("\/attitude\/(.+)\?\#")}):
                thumbs = re.findall(r'[0-9]+', str(item.get_text()))
                thumbs_num.append(thumbs[0])

            ##评论数
            for item in soup.findAll('span', {'class': 'pms'}):
                comment = re.findall(r'[0-9]+', str(item.get_text()))
                if len(comment) == 0:
                    comment_num.append('0')
                else:
                    comment_num.append(comment[0])

            if len(soup.select('div[class="c"] div span[class="ctt"]')) == 0:
                weibo_content.append('no access')
                repost_num.append('no access')
                thumbs_num.append('no access')
                comment_num.append('no access')

        else:
            print('deleted')
            weibo_content.append('deleted')
            repost_num.append('deleted')
            thumbs_num.append('deleted')
            comment_num.append('deleted')

    ##评论
    for i in range(0, 20):
        url = crawl_data['link_to_post'][i]
        comments = []
        if url != 'nn':
            r = requests.get(url, cookies=cookie)
            content = r.text
            soup = BeautifulSoup(content, 'lxml')
            # print(url)
            ## 页数
            if len(soup.select('div[class="pa"] form div input')) == 0:
                comments.append('no comment accessible')
            else:
                page_une = soup.select('div[class="pa"] form div input')[0]
                page_num = re.findall(r"\d+", str(page_une))

                for p in range(1, min(4, int(page_num[0]) + 1)):
                    comment_web = url + '?page=' + str(p)
                    comment_r = requests.get(comment_web, cookies=cookie)
                    comment = comment_r.text
                    comment_soup = BeautifulSoup(comment, 'lxml')
                    for item in comment_soup.select('div[class="c"] span[class="ctt"]'):
                        cc = item.get_text()
                        comments.append(cc)

        else:
            print("deleted")
            comments.append('deleted')

        comments_all.append(comments)

    crawl_data['comments'] = comments_all
    crawl_data['weibo_content'] = weibo_content
    crawl_data['repost_num'] = repost_num
    crawl_data['thumbs_up'] = thumbs_num
    crawl_data['comment_num'] = comment_num
    crawl_data.to_csv('crawl_data/crawl_' + str(j) + '.csv')

    comments_all = []
    for i in range(0, 20):
        url = crawl_data['link_to_post'][i]
        comments = []
        if url != 'nn':
            r = requests.get(url, cookies=cookie)
            content = r.text
            soup = BeautifulSoup(content, 'lxml')
            print(url)        
            ## 页数
            if len(soup.select('div[class="pa"] form div input')) == 0:
                comments.append('no comment accessible')
            else:
                page_une = soup.select('div[class="pa"] form div input')[0]
                page_num = re.findall(r"\d+",str(page_une))

                for p in range(1, min(4, int(page_num[0]) + 1)):
                    comment_web = url + '?page=' + str(p)
                    comment_r = requests.get(comment_web, cookies=cookie)
                    comment = comment_r.text
                    comment_soup = BeautifulSoup(comment, 'lxml')
                    for item in comment_soup.select('div[class="c"] span[class="ctt"]'):
                        cc = item.get_text()
                        comments.append(cc)

        else:
            print("deleted")
            comments.append('deleted')

        comments_all.append(comments)
    crawl_data['comments'] = comments_all

