# coding=utf-8
import json
import os
import re

import scrapy
from bs4 import BeautifulSoup
import urllib.request as request

class JubaoSpider(scrapy.Spider):
    name = 'jubao'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari / 537.36'
    }
    url = 'https://service.account.weibo.com/index?type=5&status=4&page=%s'
    # url = 'https://service.account.weibo.com/index?type=0&status=4&page=%s'
    max_page_num = 500
    # file_dir = r'E:\jubao'
    file_dir = r'/Users/wangyian/Desktop/spider/spider/text_data'

    def start_requests(self):
        for i in range(self.max_page_num, 0, -1):
            r = scrapy.Request(url=self.url % i, callback=self.get_each_page,
                               dont_filter=True)
            r.meta['page_num'] = i
            yield r
            # break

    def get_each_page(self, response):
        page_num = response.meta['page_num']
        file_name = str(page_num) + '.txt'
        file_path = os.path.join(self.file_dir, file_name)
        f = open(file_path, 'w', encoding="utf-8")

        '''
        tweet_name = 'tweet' + str(page_num) + '.txt'
        tweet_path = os.path.join(self.file_dir, tweet_name)
        t = open(tweet_path, 'w', encoding="utf-8" )'''

        table = response.xpath('//script').extract()[-1]
        data = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\(('
                          '.*?)\)</script>', table, re.S)[0]
        data = json.loads(data)
        html = data['html']

        soup = BeautifulSoup(html, 'lxml')

        divs = soup.find_all('div', class_='m_table_tit')[1:]
        for div in divs:
            url = 'https://service.account.weibo.com' + div.a['href']
            r = scrapy.Request(url=url, callback=self.get_detail, dont_filter=True)
            r.meta['file'] = f
            # r.meta['tweet'] = t
            yield r
            # break







    def get_detail(self, response):
        file = response.meta['file']
        # tweet = response.meta['tweet']

        data = response.xpath('//script').extract()[-6]
        data = re.findall('<script>STK && STK.pageletM && STK.pageletM.view\(('
                          '.*?)\)</script>', data, re.S)[0]
        data = json.loads(data)
        html = data['html']


        html = html.replace('\n', '')
        file.write(html + '\n')

        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        # ===================================
        tweet_soup = BeautifulSoup(html, 'lxml')
        tweet_data = tweet_soup.select('div[class="W_main_half_r"] div div div div[class="item top"] p a')
        if tweet_data == []:
            tweet_link = tweet_soup.select('div[class="W_main_half_r"] div div div div[class="item top"] div div')
            tweet_url = re.findall(r'</a>(.+)</div>', str(tweet_link))
        else:
            tweet_link = re.findall(r'(?<=\/)[\w]*(?=\"\s)', str(tweet_data))
            tweet_url = 'https://weibo.cn/comment/' + tweet_link[0]
            tweet_req = request.Request(url=tweet_url, headers=headers)
            with request.urlopen(tweet_req) as response:
                tweet_url = response.read().decode('UTF-8')  # 默认即为 utf-8
                #tweet_url = json.loads(tweet_url)
                #print(tweet_url)
                tweet.write(tweet_url)
                tweet.write("\n")
        #tweet.write(tweet_url)
        print("\n\n")'''










