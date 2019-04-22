# coding=utf-8

import requests
import time

import xlrd
from selenium import webdriver


class WXSpider:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                      'KHTML, '
                      'like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Cookie': 'SUV=0017755C2A50C8855CAB43DDC2B5C203; ABTEST=0|1555308291|v1; '
                  'IPLOC=CN1200; '
                  'SUID=2FB071CA232C940A000000005CB41F03; '
                  'SUID=2FB071CA541C940A000000005CB41F03; '
                  'weixinIndexVisited=1; JSESSIONID=aaa4UKxq5WomqfDrM2qOw; '
                  'PHPSESSID=r2ukmqs9uc32h3c391trqtq6s5; wapsogou_qq_nickname=; '
                  'SNUID=7DC67885F1F476E9EBD4CF2CF1254F05; sct=17'
    }
    url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query='
    browser = webdriver.Chrome()
    wb = xlrd.open_workbook(filename='天津大学校园新媒体备案登记统计表.xlsx')  # 打开文件
    weixin = wb.sheet_by_index(0)
    weixin_user_list = weixin.col_values(2, 1)
    user_list = []

    def run(self):
        for name in self.weixin_user_list:
            self.browser.get(self.url + name)
            ul = self.browser.find_elements_by_class_name('news-list2')
            if ul:
                li = ul[0].find_elements_by_tag_name('li')[0]
                img = li.find_element_by_class_name('img-box')
                current_handle = self.browser.current_window_handle
                img.click()
                for each in self.browser.window_handles:
                    if each != current_handle:
                        self.browser.close()
                        self.browser.switch_to.window(each)
                print(self.browser.current_url)
                self.user_list.append([name, self.browser.current_url])
            else:
                print(self.url + name)
                # self.browser.quit()


if __name__ == '__main__':
    spider = WXSpider()
    spider.run()
