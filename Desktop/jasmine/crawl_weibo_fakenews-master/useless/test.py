# coding=utf-8
import random

import re
import string
import zipfile

import requests
import time

from bs4 import BeautifulSoup
import xlrd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from requests.cookies import RequestsCookieJar
from ipPool import GetIP


class WXSpider:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                      'KHTML, '
                      'like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    # cookie = {
    #     'ABTEST': '7|1556169078|v1',
    #     'IPLOC': 'CN1200',
    #     'JSESSIONID': 'aaaTg91-Ud8On9YBP2oPw',
    #     'SUID': '753788751E24940A000000005CC14176',
    #     'SUID': '753788752013940A000000005CC14176',
    #     'SUV': '006E51C0758837755CC14177C7A22475',
    #     'ppinf': '5|1556169097|1557378697'
    #
    # '|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTYlOTclQkElRTYlOTclQkElRTYlOTclQkF8Y3J0OjEwOjE1NTYxNjkwOTd8cmVmbmljazoyNzolRTYlOTclQkElRTYlOTclQkElRTYlOTclQkF8dXNlcmlkOjQ0Om85dDJsdU8xZExfcUowY1lvYlVERXR0ZkM0X2tAd2VpeGluLnNvaHUuY29tfA',
    #     'ppmdig': '1556169097000000e501ccd8ed9b782c668b5b2234089be8',
    #     'pprdig': 'r1Kig4lVKUeO7oXUBkT8OdVD0KAdDORO9DtvBS4FfJQBwA8'
    #
    # '-cD0GvJLwHxSMNn6B115MKYspjr3wJkHPNdSNJHnmE6gun4GZHCcPiQfBgmkWJEa9tgQj1UoKYNGuI2nyfywwwUyRcQkdy92Uprif4w-JOFLOsfOS71lOr1AayzU',
    #     'sgid': '21-40247397-AVzBQYnMumnqWtia83EDgtfs',
    #     'weixinIndexVisited': '1'
    # }

    cookie = []

    # cookies = [
    #     {
    #         'name': 'ABTEST',
    #         'value': '0|1555308291|v1'
    #     },
    #     {
    #         'name': 'IPLOC',
    #         'value': 'CN1200'
    #     },
    #     {
    #         'name': 'JSESSIONID',
    #         'value': 'aaa4UKxq5WomqfDrM2qOw'
    #     },
    #     {
    #         'name': 'PHPSESSID',
    #         'value': 'r2ukmqs9uc32h3c391trqtq6s5'
    #     },
    #     {
    #         'name': 'SNUID',
    #         'value': '8D3788754631990A000000005CBDCE1D',
    #     },
    #     {
    #         'name': 'SUID',
    #         'value': '2FB071CA232C940A000005CB41F03'
    #     },
    #     {
    #         'name': 'SUID',
    #         'value': '2FB071CA541C900000005CB41F03'
    #     },
    #     {
    #         'name': 'SUV',
    #         'value': '0017755C2A50C8855CAB43DDC2B5C203'
    #     },
    #     {
    #         'name': 'ppinf',
    #         'value':
    #             '5|1555932691|1557142291'
    #
    # '|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTYlOTclQkElRTYlOTclQkElRTYlOTclQkF8Y3J0OjEwOjE1NTU5MzI2OTF8cmVmbmljazoyNzolRTYlOTclQkElRTYlOTclQkElRTYlOTclQkF8dXNlcmlkOjQ0Om85dDJsdU8xZExfcUowY1lvYlVERXR0ZkM0X2tAd2VpeGluLnNvaHUuY29tfA'
    #     },
    #     {
    #         'name': 'ppmdig',
    #         'value': '155593584100000018f13d69ca7e59ef45c48282cf554f72'
    #     },
    #     {
    #         'name': 'pprdig',
    #         'value':
    #
    # 'em1Yk6z3fJ6EyR
    # -WV6f_RYqgMCZNQTLG36PD7yWEEHwZ3CHyYbM9rghk6fW025p3b_gZpW2D8Hj75lcSnNeLwBak1ILNIiOIsZfr
    # -jurDUNg2OeJvnQs0eN2KYJ-AEzZFx-leCh6CWppF68N7KC2E8HypoTVHiP1UE1sm_mRtYI'
    #     },
    #     {
    #         'name': 'sct',
    #         'value': '31'
    #     },
    #     {
    #         'name': 'sgid',
    #         'value': '21-40247397-AVy9phOkEdicsUUFMF7oEV8M'
    #     },
    #     {
    #         'name': 'weixinIndexVisited',
    #         'value': '1'
    #     },
    #     {
    #         'name': 'success',
    #         'value': '1'
    #     },
    #     {
    #         'name': 'successCount',
    #         'value': '1|Mon, 22 Apr 2019 14:05:54 GMT'
    #     },
    # ]
    url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query='
    wb = xlrd.open_workbook(filename='天津大学校园新媒体备案登记统计表.xlsx')  # 打开文件
    weixin = wb.sheet_by_index(0)
    weixin_user_list = weixin.col_values(2, 1)
    user_list = []

    # proxy = random.choice(self.proxy_list).strip()
    # chrome_options = webdriver.ChromeOptions()
    # proxy = 'http://127.0.0.1:1080'
    # chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    # browser = webdriver.Chrome(chrome_options=chrome_options)


    # browser = webdriver.Chrome()
    # browser.set_script_timeout(10)
    # browser.set_page_load_timeout(10)
    #
    # browser.get('https://weixin.sogou.com/weixin')

    def __init__(self):
        try:
            with open('proxies.txt', 'r') as f:
                self.proxy_list = f.readlines()
        except:
            ip = GetIP('http://www.hiyd.com/dongzuo/', 10)
            ip.run()
            self.proxy_list = ip.success_list

    def send_request(self, url, headers=headers, allow_redirects=True):
        proxy = random.choice(self.proxy_list).strip()
        protocal = 'https' if 'https' in proxy else 'http'
        proxies = {
            protocal: proxy
        }
        try:
            response = requests.get(url, timeout=3, headers=headers,
                                    proxies=proxies, allow_redirects=allow_redirects)
        except:
            print('[requests]正在更换代理')
            time.sleep(1)
            return self.send_request(url)
        else:
            # if response.status_code == 200:
            return response
            # else:
            #     print(response)
            #     print('此IP被封，[requests]正在更换代理')
            #     time.sleep(1)
            #     return self.send_request(url)

    def create_proxy_auth_extension(self, proxy_host, proxy_port,
                                    proxy_username, proxy_password,
                                    scheme='http', plugin_path=None):
        if plugin_path is None:
            plugin_path = r'D:/{}_{}@http-cla.abuyun.com_9030.zip'.format(proxy_username,
                                                                          proxy_password)

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Abuyun Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                }
              };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

    def getCleanCookie(self):
        chrome_options = webdriver.ChromeOptions()

        # 代理服务器
        proxyHost = "http-pro.abuyun.com"
        proxyPort = "9010"
        # 代理隧道验证信息
        proxyUser = "H61SU35AM8RH793P"
        proxyPass = "D422E37A037A9FE9"
        proxy_auth_plugin_path = self.create_proxy_auth_extension(
            proxy_host=proxyHost,
            proxy_port=proxyPort,
            proxy_username=proxyUser,
            proxy_password=proxyPass)
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument(
        #     'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
        #     'KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"')
        # chrome_options.add_extension(proxy_auth_plugin_path)

        proxy = random.choice(self.proxy_list).strip()
        # proxy = 'http://127.0.0.1:1080'

        chrome_options.add_argument('--proxy-server={0}'.format(proxy))
        browser = webdriver.Chrome(chrome_options=chrome_options)

        browser.set_script_timeout(8)
        browser.set_page_load_timeout(8)
        try:
            browser.get(
                'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%A4%A9%E6%B4'
                '%A5%E5'
                '%A4%A7%E5%AD%A6')
        except Exception:
            print('正在更换代理')
            print(browser.get_cookies())
            browser.quit()
            return self.getCleanCookie()
        else:
            if '无法访问此网站' in browser.page_source or '未连接到互联网' in browser.page_source or \
                            'antispider' in browser.page_source or '请输入验证码' in \
                    browser.page_source:
                print('正在更换代理')
                time.sleep(0.5)
                browser.quit()
                return self.getCleanCookie()
                # else:
                #     browser.find_element_by_id('query').send_keys('天津大学')
                #     browser.find_element_by_class_name('swz2').click()
                #     browser.switch_to.window(browser.window_handles[-1])
        print(browser.get_cookies())
        SUV = browser.get_cookie("SUV")
        SNUID = browser.get_cookie("SNUID")
        browser.quit()

        self.cookie = 'SUV=%s;SNUID=%s' % (SUV['value'], SNUID['value'])

        #     return self.getCleanCookie(url)
        # else:
        #     if '无法访问此网站' in browser.page_source or '未连接到互联网' in browser.page_source:
        #         print('正在更换代理')
        #         time.sleep(0.5)
        #         browser.quit()
        #         return self.getCleanCookie(url)
        #     cookies = browser.get_cookies()
        #     browser.quit()
        #     return cookies

        #
        # try:
        #     self.browser.get(url)
        # except TimeoutException:
        #     print(url)
        #     self.browser.close()
        #     self.browser.switch_to.window(self.browser.window_handles[-1])
        #     # self.browser.execute_script('window.stop()')
        # except Exception as e:
        #     print(e.args)
        #     return self.send_request(url)
        # else:
        #     ul = self.browser.find_elements_by_class_name('news-list2')
        #     if ul:
        #         img = ul[0].find_element_by_class_name('img-box')
        #         img.click()
        #         if len(self.browser.window_handles) > 8:
        #             self.browser.close()
        #         self.browser.switch_to.window(self.browser.window_handles[-1])
        #         print(self.browser.current_url)
        #         self.user_list.append(self.browser.current_url)
        #     else:
        #         print('没找到该用户:' + url)
        #         # time.sleep(5)

    def run(self):
        cookies = self.getCleanCookie('https://weixin.sogou.com/weixin')
        print(cookies)
        self.browser.delete_all_cookies()
        for each in cookies:
            if each['name'] == 'IPLOC':
                each['value'] = 'CN1200'
            print(each)
            self.browser.add_cookie(each)
        for each in self.weixin_user_list:
            self.mainPageSpider(self.url + each)

    def getCookie(self):
        response = self.send_request(
            'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%A4%A9%E6%B4%A5%E5'
            '%A4%A7%E5%AD%A6', allow_redirects=True)
        if 'antispider' in response.url or '请输入验证码' in \
                response.text:
            print('此IP被封，正在更换代理')
            return self.getCookie()
        print(response.status_code)
        cookies = response.cookies.get_dict()
        print(cookies)
        self.cookie.append('SNUID=%s;SUV=%s' % (cookies['SNUID'], cookies['SUV']))

    def re_run(self, url):
        response = self.send_request(url)
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find('div', class_='img-box')
        if div:
            a = div.a
            href = a['href']
            b = int(random.random() * 100) + 1
            c = href.find('url=')
            c = href[c + 30 + b]
            href = 'https://weixin.sogou.com' + href + '&k=' + str(b) + '&h=' + c
            headers = self.headers
            headers['Referer'] = response.url
            headers['Cookie'] = random.choice(self.cookie)
            tempResponse = self.send_request(href, headers=headers, allow_redirects=False)
            if tempResponse.status_code == 302:
                self.getCookie()
                return self.re_run(url)
            tempUrl = re.findall('url \+= \'(.*?)\';', tempResponse.text, re.S)
            tempUrl = ''.join(tempUrl).replace('@', '')
            print(tempUrl)
            self.user_list.append(tempUrl)
        elif '您的访问出错了' in response.text:
            print('正在更换cookie')
            self.getCookie()
            return self.re_run(url)
        else:
            print('该用户未找到：' + url)
            # def mainPageSpider(self, url):
            #     try:
            #         self.browser.get(url)
            #     except TimeoutException:
            #         print('没找到该用户:' + url)
            #         self.browser.close()
            #         self.browser.switch_to.window(self.browser.window_handles[-1])
            #         # self.browser.execute_script('window.stop()')
            #     except Exception as e:
            #         print(e.args)
            #         return self.send_request(url)
            #     else:
            #         ul = self.browser.find_elements_by_class_name('news-list2')
            #         if ul:
            #             img = ul[0].find_element_by_class_name('img-box')
            #             img.click()
            #             if len(self.browser.window_handles) > 8:
            #                 self.browser.close()
            #             self.browser.switch_to.window(self.browser.window_handles[-1])
            #             print(self.browser.current_url)
            #             self.user_list.append(self.browser.current_url)


if __name__ == '__main__':
    spider = WXSpider()
    for i in range(0, 10):
        spider.getCleanCookie()
    for each in spider.weixin_user_list:
        spider.re_run('https://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8'
                      '' % each)
        # spider.run()
