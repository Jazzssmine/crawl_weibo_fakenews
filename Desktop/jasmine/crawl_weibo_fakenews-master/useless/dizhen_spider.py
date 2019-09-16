# coding=utf-8
import json
import re
import requests
import scrapy
import time
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from spider.spiders.sentiment import Sentiment
import datetime
import xlrd
import random


class DizhenSpider(scrapy.Spider):
    name = 'dizhen'
    headers = {
        'User-Agent: Mozilla': '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
                               'like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    cookie = {"ALF": "1592395259",
              "Apache": "7641355422360.468.1550545551314",
              "SCF": 'ArgY-i3N6StMP1trO7TWYCPUpY6WmzfHBE7pxahb4EMA8NbGrbHL'
                     '-WD1rtMaTtl5PmeMTzT98iocaCwzKm4KlQ4.',
              "SINAGLOBAL":
                  '7641355422360.468.1550545551314',
              "SSOLoginState": "1560859260",
              "SUB": "_2A25wDKIsDeRhGeNM41UR8yvOyDuIHXVTe5TkrDV8PUNbmtAKLXbTkW9NSfs"
                     "-BKDQ1dSaebjA1745X5U32Ow22PhY",
              'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWN9_YYbKrAOU_0jaRCxHX25JpX5KMhUgL.Fo'
                      '-E1hM7e0-Ee0M2dJLoIpRLxKqL1KMLB.2LxKqL1KMLB.2LxKqL1KMLB.27eh5t',
              'SUHB': '0HThJwW2ufBKi1',
              'ULV': '1550545551318:1:1:1:7641355422360.468.1550545551314:',
              'UOR': ',,www.hailiangxinxi.com',
              '_s_tentry': 'gl.ali213.net',
              'cross_origin_proto': 'SSL',
              'login_sid_t': '34b4689164b0254a9cc5dbe5c2cef7c4',
              'webim_unReadCount': '%7B%22time%22%3A1560924147959%2C%22dm_pub_total%22%3A0%2C'
                                   '%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D',
              'wvr': '6'
              }
    article_list = []
    sentiment = Sentiment()

    def start_requests(self):
        url = 'https://s.weibo.com/weibo/?q=%s&typeall=1&suball=1&timescope' \
              '=custom:2019-06-%s-%s:2019-06-%s-%s&Refer=g&page=%s'
        i = 19
        for j in range(0, 24):
            if i == 19 and j == 14:
                break
            k = i
            if j == 23:
                k += 1
            for page in range(1, 51):
                r = scrapy.Request(url=url % ('地震', i, j, k, (j + 1) % 24, page)
                                   , callback=self.weibo_spider, dont_filter=True)
                yield r

    def weibo_spider(self, response):
        divs = response.xpath("//div[@class='m-con-l']/div[2]//div[@class='card-wrap' and "
                              "@action-type='feed_list_item']")
        for div in divs:
            uid_url = div.xpath("div/div[@class='card-feed']/div[last("
                                ")-1]/a/@href").extract_first()
            uid = re.findall('weibo.com/(.*?)\?refer', uid_url)
            if uid:
                uid = uid[0]
            else:
                uid = ''
            full_text = div.xpath(
                "div/div[@class='card-feed']/div[last()]/p[@class='txt' and "
                "@node-type='feed_list_content_full']")
            if not full_text:
                full_text = div.xpath(
                    "div/div[@class='card-feed']/div[last()]/p[@class='txt' and "
                    "@node-type='feed_list_content']")
            videos = full_text.xpath("a[contains(text(),'的秒拍视频')]/@href").extract_first()
            if not videos:
                videos = ''
            full_text = ''.join(full_text.xpath(".//text()").extract()).strip()
            rdate = div.xpath(
                "div/div[@class='card-feed']/div[last()]/p[@class='from']/a[1]/text("
                ")").extract_first().strip()
            if '今天' in rdate:
                rdate = datetime.datetime.today().strftime('%Y-%m-%d') + ' ' + rdate[3:]
            elif '分钟' in rdate:
                rdate = re.match("\d+", rdate).group(0)
                rdate = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(time.time() - int(rdate) * 60))
            elif '秒' in rdate:
                rdate = re.match("\d+", rdate).group(0)
                rdate = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(time.time() - int(rdate)))
            elif '月' in rdate:
                rdate = time.strptime(str(time.localtime().tm_year) + '年' + rdate.strip(),
                                      '%Y年%m月%d日 %H:%M')
                rdate = time.strftime("%Y-%m-%d %H:%M:%S", rdate)
            aid = div.xpath(
                "div/div[@class='card-feed']/div[last()]/p[@class='from']/a["
                "1]/@href").extract_first()
            aid = re.findall(uid + '/(.*?)\?refer', aid)[0]
            url = 'https://weibo.com/%s/%s' % (uid, aid)
            tool = div.xpath(
                "div/div[@class='card-feed']/div[last()]/p[@class='from']/a[2]/text("
                ")").extract()
            if not tool:
                tool = '未知'
            else:
                tool = tool[0]
            retweet = div.xpath(
                "div/div[@class='card-act']/ul/li[2]/a/text()").extract_first()
            retweet = retweet.split(' ')[2]
            comment = div.xpath(
                "div/div[@class='card-act']/ul/li[3]/a/text()").extract_first()
            comment = comment.split(' ')[1]
            like = div.xpath(
                "div/div[@class='card-act']/ul/li[4]/a/em/text()").extract_first()
            if not retweet:
                retweet = 0
            if not comment:
                comment = 0
            if not like:
                like = 0
            imgs = div.xpath(
                "div/div[@class='card-feed']/div[last()]/div["
                "@node-type='feed_list_media_prev']/div/ul//li/img/@src").extract()
            imgs = '\n'.join(imgs)
            imgs.replace("//", "https://")
            line = [aid, uid, rdate.strip(), like, retweet, comment, full_text, url, imgs,
                    videos,
                    tool]
            self.article_list.append(line)
            print(line)

    def close(self, reason):
        print(len(self.article_list))
        self.sentiment.insert_into_user(self.article_list)
