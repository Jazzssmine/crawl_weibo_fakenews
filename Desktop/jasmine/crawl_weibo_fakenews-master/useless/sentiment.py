# coding=utf-8
import copy
import re

import jieba
import jieba.analyse
import numpy as np
import pymysql
import time
from aip import AipNlp
import datetime


class Sentiment:
    def __init__(self):
        self.db = pymysql.connect("localhost", "xuanchuanbu", "xuanchuanbu",
                                  "xuanchuanbu", 3306, charset='utf8mb4')
        self.cursor = self.db.cursor()

    def insert_into_user(self, monitor_user_list):
        sql = "INSERT INTO monitor_user(`uid`, `mid`, `name`, `gender`, `type`, " \
              "`follow_num`, `fan_num`, `level`, `address`, `school`, `introduction`, " \
              "`v_flag`, `v_info`, `img_url`, `last_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE`name`=VALUES(`name`)," \
              "`gender`=VALUES(`gender`),`type`=VALUES(`type`),`follow_num`=VALUES(" \
              "`follow_num`),`fan_num`=VALUES(`fan_num`),`level`=VALUES(`level`)," \
              "`address`=VALUES(`address`),`school`=VALUES(`school`),`introduction`=VALUES(" \
              "`introduction`),`v_flag`=VALUES(`v_flag`),`v_info`=VALUES(`v_info`)," \
              "`img_url`=VALUES(`img_url`),`last_time`=VALUES(`last_time`)"
        self.cursor.executemany(sql, monitor_user_list)
        self.db.commit()

    def insert_into_user(self, articles):
        print(u'正在插入articles表')
        sql = "INSERT INTO test_article(`aid`, `uid`, `rdate`, `likenum`, `retweet`, " \
              "`comment`, " \
              "`full_text`, `url`,`img`,`video`, `tool`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s)"
        self.cursor.executemany(sql, articles)
        self.db.commit()

    def insert_into_articles(self):
        print(u'正在插入articles表')
        sql = "INSERT INTO articles(`aid`, `uid`, `mid`, `title`, `rdate`, `summary`, " \
              "`full_text`, `url`, `relate_tju`,`tool`, `p_or_n`) VALUES (%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s)ON DUPLICATE KEY UPDATE`title`=VALUES(`title`),`rdate`=VALUES(" \
              "`rdate`),`summary`=VALUES(`summary`),`full_text`=VALUES(`full_text`)," \
              "`url`=VALUES(`url`),`relate_tju`=VALUES(`relate_tju`),`tool`=VALUES(`tool`)," \
              "`p_or_n`=VALUES(`p_or_n`)"
        self.cursor.executemany(sql, self.article_list)
        self.db.commit()

    def insert_into_article_keywords(self):
        print(u'正在插入articles_keywords表')
        sql = "REPLACE INTO articles_keywords(aid, word, frequency) VALUES (%s,%s,%s)"
        self.cursor.executemany(sql, self.aid_keyword_list)
        self.db.commit()

    # 提取文本关键字计算权重
    def extract_keyword(self):
        self.aid_keyword_list = []
        jieba.analyse.set_stop_words("./spider/spiders/停用词.txt")
        for i in range(len(self.aid_text_list_process)):
            tags = jieba.analyse.extract_tags(self.aid_text_list[i][1], topK=10,
                                              withWeight=True,
                                              allowPOS=('ns', 'n', 'vn', 'v'))
            for j in range(len(tags)):
                temp = [self.aid_text_list[i][0], tags[j][0], tags[j][1]]
                aid_keyword = copy.copy(temp)
                self.aid_keyword_list.append(aid_keyword)

    # 读取文件，生成三个列表，urls代表生成的全文列表，用作情感分析
    # total_data代表转换格式后的数据（日期，relate_tju）
    # aid_text_list代表文章id和文本的列表，为生成关键字的数据列表
    def output(self, article_list):
        self.article_list = article_list
        self.urls = []
        self.total_data = []
        self.aid_text_list = []
        for row in article_list:
            temp = [row[0], row[6]]
            aid_text = copy.copy(temp)
            self.aid_text_list.append(aid_text)
            self.urls.append(row[6])
            # print(type(row[6]).__name__)
            # str_date = re.search("[0-9]+.*[0-9]$", row[4]).group()
            # row[4] = datetime.strptime(str_date, "%Y-%m-%d %H:%M")  # 转换日期格式
            list1 = copy.copy(row)
            self.total_data.append(list1)

    def sentimentClassify(self):
        """ 你的 APPID AK SK """
        # 利用百度云提供的API接口实现情感分析
        APP_ID = '16021158'  # 用自己申请的百度极性分析api
        API_KEY = 'mHcRxtN067mbZ4fqybaCVtUW'
        SECRET_KEY = 'ElorKISgn0dCP5q2SQjeDe2Ozg5TmO89'
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

        self.pp = []
        self.total_data_process = []
        self.aid_text_list_process = []
        for i in range(0, len(self.urls)):
            text = self.urls[i]
            # print(text)
            # 通过百度提供的接口方法进行情感倾向提取
            try:
                result = client.sentimentClassify(text)
                self.total_data_process.append(self.total_data[i])
                self.aid_text_list_process.append(self.aid_text_list[i])
            except:
                print("数据格式出错,这条数据内容为：")
                self.pp.append(0)
                # print(result)
            else:
                # 如果解析错误则填写上空值,使得程序不会出错而停止运行
                if "error_code" in result.keys():
                    print(result)
                    pp_sentences = []
                    np_sentences = []
                    sentences_list = re.split("。", text)  # 减小句子长度，防止解析错误
                    sentences_size = len(sentences_list) - 1
                    flag = 0
                    for j in range(sentences_size):
                        # print(text)
                        # 通过百度提供的接口方法进行情感倾向提取
                        result = client.sentimentClassify(text[j])
                        if "error_code" in result.keys():
                            flag = 1  # 解析错误直接中断循环
                            break
                        else:
                            data = result['items']
                            items = data[0]
                            pp_sentences.append(items['positive_prob'])
                            np_sentences.append(items['negative_prob'])
                    if flag == 0:
                        positive_prob_result = np.mean(pp_sentences)
                        negative_prob_result = np.mean(np_sentences)
                        if positive_prob_result > negative_prob_result:
                            self.pp.append(1)
                        else:
                            self.pp.append(-1)
                    else:
                        self.pp.append(0)
                else:
                    data = result['items']
                    items = data[0]
                    positive_prob = items['positive_prob']
                    negative_prob = items['negative_prob']
                    if positive_prob > negative_prob:
                        self.pp.append(1)
                    else:
                        self.pp.append(-1)
                time.sleep(0.2)

    def re_combine_data(self):
        for i in range(0, len(self.pp)):
            # total_data_process[i].insert(0, i + 1)  # 向数据列表中插入主键，1,2,3，。。。
            j = self.pp[i]
            self.article_list[i].append(j)  # 向数据列表中插入极性分析的结果

    def getWeiboUsers(self):
        sql = """
        SELECT
		t.uid,
		t.mid,
		`name`,
		gender,
		`type`,
		follow_num,
		fan_num,
		`level`,
		address,
		school,
		introduction,
		v_flag,
		v_info,
		img_url,
      t.last_time,
		ff + af + IFNULL(`if`, 0) AS activity
		FROM
		(
		SELECT
		monitor_user.id,
		monitor_user.uid,
		monitor_user.mid,
		monitor_user.name,
		mname,
		monitor_user.gender,
		monitor_user.type,
		monitor_user.follow_num,
		monitor_user.fan_num,
		monitor_user.level,
		monitor_user.address,
		monitor_user.school,
		monitor_user.introduction,
		monitor_user.v_flag,
		monitor_user.v_info,
		monitor_user.img_url,
      monitor_user.last_time,
		COUNT(aid) AS article_num,
		IFNULL(monitor_user.fan_num - temp_monitor_user.fan_num,0) AS `ff`,
		IFNULL(monitor_user.follow_num - temp_monitor_user.follow_num,0) AS `af`,
		monitor_user.follow_num + monitor_user.fan_num AS `influence`
		FROM
		monitor_user
		JOIN medias ON monitor_user.mid = medias.mid
		LEFT JOIN articles ON monitor_user.uid = articles.uid AND monitor_user.mid =
		articles.mid
		LEFT JOIN temp_monitor_user ON monitor_user.uid = temp_monitor_user.uid AND
		monitor_user.mid = temp_monitor_user.mid
		GROUP BY
		monitor_user.uid,
		monitor_user.mid
		) t
		LEFT JOIN(
		SELECT
		monitor_user.id,
		COUNT(aid) AS `if`
		FROM
		monitor_user
		LEFT JOIN articles ON monitor_user.uid = articles.uid AND monitor_user.mid =
		articles.mid
		WHERE
		DATE(rdate) >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)
		GROUP BY
		monitor_user.id) tt
		ON
		t.id = tt.id
		LEFT JOIN(
		SELECT
		monitor_user.id,
		COUNT(aid) AS `article_negative_num`
		FROM
		monitor_user
		LEFT JOIN articles ON monitor_user.uid = articles.uid AND monitor_user.mid =
		articles.mid
		WHERE
		p_or_n=-1 AND relate_tju=1
		GROUP BY
		monitor_user.id
		) ttt
		ON t.id=ttt.id
		WHERE t.mid=1
		ORDER BY activity DESC
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # userList = []
        # for row in rows:
        #     userList.append(row[0])
        # return userList
        return rows

    def getWeiboArticles(self):
        sql = "SELECT aid FROM articles WHERE mid=1"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        articleList = []
        for row in rows:
            articleList.append(row[0])
        return articleList

    def analyze_article(self, article_list):
        self.output(article_list)
        self.sentimentClassify()
        self.re_combine_data()
        self.extract_keyword()
        self.insert_into_articles()
        self.insert_into_article_keywords()


if __name__ == '__main__':
    sentiment = Sentiment()
    articles = sentiment.cursor.execute(
        'SELECT `rdate`, `likenum`, `retweet`, `comment`, `full_text`, `url`, `img`, '
        '`video`, `tool` FROM `test_article` GROUP BY aid ORDER BY rdate DESC')
    import xlwt

    results = sentiment.cursor.fetchall()
    fields = sentiment.cursor.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet',cell_overwrite_ok=True)

    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    row = 1
    col = 0
    for row in range(1, len(results) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row - 1][col])

    workbook.save('out.xls')
    print(articles)
