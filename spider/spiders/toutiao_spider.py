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


class XuanchuanbuSpider(scrapy.Spider):
    name = 'toutiao'
    headers = {
        'User-Agent: Mozilla': '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
                               'like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    cookie = {"_T_WM": "88510f592e13f85224f5d2cf249680e0",
              "ALF": "1554558588",
              "SSOLoginState": "1551966589",
              "MLOGIN": "1",
              "WEIBOCN_FROM": "1110006030",
              "SCF": "Ag_f8T4qg9uiN-Kts-jmnKjik99qkk417QqWSxUWfuIR7ScQmwdx1ZTv1qNkef9MG"
                     "-iCdmrcB2Ty01KuajDaJ6M.",
              "SUB":
                  "_2A25xhVEtDeRhGeNM6VIS9ynOzz6IHXVShn9lrDV6PUJbktAKLVLEkW1NTi0IEzrDWytbBCrTUWStS9x4Jb4EwctO",
              "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZLIWa7nsxoxkjsm9b5Kyi5JpX5K-hUgL.Fo"
                      "-Eeo50S0MEShz2dJLoIExQwPWLMJiads2LxK-L12qL12eLxKqL1-zLBozLxKMLB.2LB.qt",
              "SUHB": "02MfezNbOQYvsK",
              "XSRF-TOKEN": "5b4193",
              "M_WEIBOCN_PARAMS": "luicode%3D10000011%26lfid%3D1076031699432410%26uicode"
                                  "%3D20000174"}

    splash_args = {
        'wait': 3
    }
    user_list = []
    article_list = []
    monitor_user_list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        wb = xlrd.open_workbook(filename='天津大学校园新媒体备案登记统计表.xlsx')  # 打开文件
        weixin = wb.sheet_by_index(0)
        weibo = wb.sheet_by_index(1)
        self.weixin_user_list = weixin.col_values(2, 1)
        self.weibo_user_list = weibo.col_values(1, 1)
        # self.weibo_user_list = [2728331853]

    # user_list = ['天津大学',
    #              '南开大学',
    #              '北京大学',
    #              '清华大学',
    #              '上海交通大学',
    #              '浙江大学',
    #              '电子科技大学',
    #              '吉林大学',
    #              '大连理工大学',
    #              '重庆大学']

    # user_list = ['清华大学']

    def start_requests(self):
        self.monitor_user_list = []
        self.article_list = []
        # self.weibo_user_search()
        for each in self.weibo_user_list:
            url = 'https://weibo.cn/' + str(int(each))
            r = scrapy.Request(url, callback=self.weibo_spider, cookies=self.cookie,
                               meta={'dont_redirect': True})
            r.meta['uid'] = str(int(each))
            yield r
            # self.toutiao_user_spider()
            # self.zhihu_user_spider()
            # for each in self.monitor_user_list:
            #     if each[1] == 4:
            #         r = SplashRequest('https://www.toutiao.com/c/user/' + each[0] + '/',
            #                           self.toutiao_parse, args=self.splash_args)
            #         r.meta['uid'] = each[0]
            #     elif each[1] == 3:
            #         r = scrapy.Request(url='https://www.zhihu.com/api/v4/members/' + each[
            #             0] + '/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment'
            #                  '%2Creward_info%2Cis_collapsed%2Cannotation_action'
            #                  '%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by'
            #                  '%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent'
            #                  '%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission'
            #                  '%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info'
            #                  '%2Cquestion%2Cexcerpt%2Cis_labeled%2Clabel_info%2Crelationship'
            #                  '.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp'
            #                  '%2Cis_recognized%3Bdata%5B*%5D.author.badge%5B%3F('
            #                  'type%3Dbest_answerer)%5D.topics&offset=0&limit=20&sort_by
            # =created',
            #                            callback=self.zhihu_article_spider)
            #         r.meta['uid'] = each[0]
            #     yield r

    def weibo_spider(self, response):
        uid = response.meta['uid']
        tips = response.xpath("//div[@class='tip2']").xpath('string()').extract_first()
        if not tips:
            return
        tip = re.search("关注\[(\d+)\] 粉丝\[(\d+)\]", tips)
        follow_num = tip.group(1)
        fan_num = tip.group(2)

        r = scrapy.Request(url="https://weibo.cn/%s/info" % uid, cookies=self.cookie,
                           callback=self.weibo_user_spider, dont_filter=True)
        r.meta['uid'] = uid
        r.meta['fan_num'] = fan_num
        r.meta['follow_num'] = follow_num
        yield r

        divs = response.xpath("//div[@class='c' and @id]")
        for div in divs:
            aid = div.xpath('@id').extract_first()
            url = div.xpath("div[last()]/a[last()-1]/@href").extract_first()
            title = div.xpath('.//span[@class="ctt"]/text()').extract_first()
            yield scrapy.Request(url=url, cookies=self.cookie, meta={'uid': uid, 'aid': aid,
                                                                     'title': title},
                                 callback=self.weibo_article_spider, dont_filter=True)

    def weibo_user_spider(self, response):
        # level = response.xpath("/html/body/div[4]//text()").extract_first()
        # level = re.search('会员等级[：:]?(\d)(.*?)', level).group(1)
        level = 0
        tips = response.xpath("/html/body/div[6]//text()").extract()
        tip = ''
        for x in tips:
            tip = tip + x + ","
        name = re.search('昵称[：:]?(.*?),', tip)
        gender = re.search('性别[：:]?(.*?),', tip)
        address = re.search('地区[：:]?(.*?),', tip)
        introduction = re.search('简介[：:]?(.*?),', tip)
        v_info = re.search('认证[：:]?(.*?),', tip)
        img_url = response.xpath("/html/body/div[3]/img/@src").extract_first()

        if name and name.group(1):
            name = name.group(1)
        else:
            name = ''

        if gender and gender.group(1):
            gender = gender.group(1)
        else:
            gender = ''
        if address and address.group(1):
            address = address.group(1)
        else:
            address = ''
        if introduction and introduction.group(1):
            introduction = introduction.group(1)
        else:
            introduction = ''
        if v_info and v_info.group(1):
            v_flag = 1
            v_info = v_info.group(1)
        else:
            v_flag = 0
            v_info = ''

        line = [response.meta['uid'], 1, name, gender, '', response.meta['follow_num'],
                response.meta['fan_num'], level, address, '', introduction, v_flag, v_info,
                img_url]
        print(line)
        self.monitor_user_list.append(line)

    def weibo_article_spider(self, response):
        uid = response.meta['uid']
        aid = response.meta['aid']
        title = response.meta['title']
        url = response.url
        div = response.xpath("//div[@id='M_']/div")
        context = div.xpath('string()').extract_first().replace(" ", "").replace(u"\xa0", "")
        # print(context)
        x = context.split(":", 1)
        full_text = x[1]
        relate_tju = 1 if '天津大学' in full_text else 0
        rdate = response.xpath("//div[contains(@id,'M_')]/div[last()]/span[last()]/text("
                               ")").extract_first()
        # rdate = re.match("\d+", rdate)
        if not title or title == ' ' or title == '' or title.strip() == '':
            title = full_text[0:15]
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
        line = [aid, uid, 1, title, rdate.strip(), '', full_text, url, relate_tju]
        print(line)
        self.article_list.append(line)

    def zhihu_user_spider(self):
        for each in self.user_list:
            soup = BeautifulSoup(
                requests.get('https://www.zhihu.com/search?type=people&q=' + each,
                             allow_redirects=True).text,
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
                gender = u'男'
            elif data['gender'] == 0:
                gender = u'女'
            else:
                gender = u'未知'
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
                relate_tju = 1 if u'天津大学' in full_text else 0
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
                gender = u'女'
            elif data['gender'] == 1:
                gender = u'男'
            else:
                gender = u'未知'
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
                              args=self.splash_args)
            r.meta['line'] = line
            yield r

    def parse_toutiao_article(self, response):
        line = response.meta['line']
        full_text = response.xpath('.//div[@class="article-content"]//text()').extract()
        full_text = ''.join(full_text)
        relate_tju = 1 if u'天津大学' in full_text else 0
        line.insert(6, full_text)
        line.append(relate_tju)
        print(line)
        self.article_list.append(line)

    def close(self, reason):
        print(len(self.monitor_user_list))
        print(len(self.article_list))
        Sentiment().insert_into_user(self.monitor_user_list)
        sentiment = Sentiment()
        sentiment.analyze_article(self.article_list)
