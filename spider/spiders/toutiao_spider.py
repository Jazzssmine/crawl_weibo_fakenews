# coding=utf-8
import json
import re
import requests
import scrapy
import time
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from spider.spiders.sentiment import Sentiment


class XuanchuanbuSpider(scrapy.Spider):
    name = 'toutiao'
    start_urls = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    splash_args = {
        'wait': 2
    }
    article_list = []
    monitor_user_list = []

    user_list = ['天津大学',
                 '南开大学',
                 '北京大学',
                 '清华大学',
                 '上海交通大学',
                 '浙江大学',
                 '电子科技大学',
                 '吉林大学',
                 '大连理工大学',
                 '重庆大学']

    # user_list = ['清华大学']

    def start_requests(self):
        self.monitor_user_list = []
        self.toutiao_user_spider()
        Sentiment([]).insert_into_user(self.monitor_user_list)
        self.article_list = []
        for each in self.monitor_user_list:
            url = 'https://www.toutiao.com/c/user/' + each[0] + '/'
            r = SplashRequest(url, self.toutiao_parse, endpoint='render.html',
                              args=self.splash_args, headers=self.headers)
            r.meta['uid'] = each[0]
            yield r
        self.monitor_user_list = []
        self.zhihu_user_spider()
        Sentiment([]).insert_into_user(self.monitor_user_list)
        for each in self.monitor_user_list:
            r = scrapy.Request(url='https://www.zhihu.com/api/v4/members/' + each[0] + \
                                   '/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment' \
                                   '%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail' \
                                   '%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count' \
                                   '%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings' \
                                   '%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time' \
                                   '%2Creview_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Clabel_info' \
                                   '%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked' \
                                   '%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.author.badge'
                                   '%5B%3F(' \
                                   'type%3Dbest_answerer)%5D.topics&offset=0&limit=20&sort_by=created',
                               callback=self.zhihu_article_spider, headers=self.headers)
            r.meta['uid'] = each[0]
            yield r

    def zhihu_user_spider(self):
        for each in self.user_list:
            soup = BeautifulSoup(
                requests.get('https://www.zhihu.com/search?type=people&q=' + each,
                             headers=self.headers).text,
                'lxml')
            a = soup.find_all('a', class_='UserLink-link')[0]
            href = 'https:' + a['href']
            uid = href[href.find('/', 23) + 1:]
            mid = 3
            img_url = a.img['src']
            userSoup = BeautifulSoup(requests.get(href, headers=self.headers).text, 'lxml')
            jData = json.loads(userSoup.find('script', id='js-initialData').text)
            data = jData['initialState']['entities']['users'][uid]
            name = data['name']
            v_flag = 1 if len(data['badge']) > 0 else 0
            if v_flag == 1:
                v_info = data['badge'][0]['description']
            else:
                v_info = ''
            if data['gender'] == 1:
                gender = '男'
            elif data['gender'] == 0:
                gender = '女'
            else:
                gender = '未知'
            introduction = data['description']
            fan_num = data['followerCount']
            follow_num = data['followingCount']
            type = ''
            if 'name' in data['business'].keys():
                type = data['business']['name']
            address = ''
            if len(data['locations']) > 0:
                address = data['locations'][0]['name']
            school = ''
            if len(data['educations']) > 0:
                school = data['educations'][0]['school']['name']
            line = [uid, mid, name, gender, type, follow_num, fan_num, 0, address, school,
                    introduction,
                    v_flag, v_info, img_url]
            print(line)
            self.monitor_user_list.append(line)

    def zhihu_article_spider(self, response):
        # data = json.loads(requests.get(url, headers=self.headers).text)
        data = json.loads(response.text)
        uid = response.meta['uid']
        mid = 3
        if 'data' in data.keys():
            for every in data['data']:
                aid = every['id']
                rdate = time.strftime('%Y-%m-%d %H:%M:%S',
                                      time.localtime(every['created_time']))
                title = every['question']['title']
                url = every['url'].replace('answers', 'answer')
                full_text = BeautifulSoup(every['content'], 'lxml').text
                relate_tju = 1 if '天津大学' in full_text else 0
                line = [aid, uid, mid, title, rdate, '', full_text, url, relate_tju]
                print(line)
                self.article_list.append(line)

    def toutiao_user_spider(self):
        lines = []
        for each in self.user_list:
            url = 'https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search' \
                  '&offset=0&format=json&keyword=' \
                  + each + '&autoload=true&count=20&en_qc=1&cur_tab=4' \
                           '&from=media&pd=user'
            data = json.loads(requests.get(url, headers=self.headers).content)[
                'data'][0]
            uid = data['id']
            mid = 4
            source_url = data['source_url']
            fan_num = data['follow_count']
            introduction = data['description']
            name = data['name']
            v_flag = data['user_auth_info']['auth_type']
            if v_flag == 1:
                v_info = data['user_auth_info']['auth_info']
            else:
                v_info = ''
            img_url = data['avatar_url']
            if data['gender'] == 0:
                gender = '女'
            elif data['gender'] == 1:
                gender = '男'
            else:
                gender = '未知'
            text = requests.get(source_url, headers=self.headers).text
            follow_num = re.findall("guanzhu:'(.*?)'", text)[0]
            line = [uid, mid, name, gender, '', follow_num, fan_num, 0, '', '', introduction,
                    v_flag, v_info, img_url]
            print(line)
            lines.append(line)
        self.monitor_user_list = lines

    def toutiao_parse(self, response):
        print(u'----------使用splash爬取头条异步加载内容-----------')
        uid = response.meta['uid']
        for each in response.xpath('//div[@class="relatedFeed"]/ul/li['
                                   '@ga_event="feed_item_click"]'):
            div = each.xpath('.//div[@class="rbox-inner"]')
            href = div.xpath('.//a[@class="link title"]/@href')[0].extract()
            aid = href.split('/')[2]
            href = 'https://www.toutiao.com/i' + aid
            title = div.xpath('.//a[@class="link title"]/text()')[0].extract()
            rdate = div.xpath('.//span[@class="lbtn"]/text()')[0].extract()[2:]
            url = href
            line = [aid, uid, 4, title, rdate, '', url]
            r = SplashRequest(href, callback=self.parse_toutiao_article,
                              args=self.splash_args, headers=self.headers)
            r.meta['line'] = line
            yield r

    def parse_toutiao_article(self, response):
        line = response.meta['line']
        full_text = response.xpath('.//div[@class="article-content"]//text()').extract()
        full_text = ''.join(full_text)
        relate_tju = 1 if '天津大学' in full_text else 0
        line.insert(6, full_text)
        line.append(relate_tju)
        print(line)
        self.article_list.append(line)

    def close(self, reason):
        print(len(self.article_list))
        sentiment = Sentiment(self.article_list)
        sentiment.analyze_article()
