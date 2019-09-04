# coding=utf-8
import requests
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import base64


class GetIP:
    '''
    www.66ip.cn
    www.xicidaili.com
    www.goubanjia.com
    '''

    def __init__(self, verify_url, total_page):
        self.total_page = total_page + 1
        self.proxy_list = []
        self.success_list = []
        self.verify_url = verify_url
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                          "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        self.proxies = {
            'https': 'https://127.0.0.1:1080',
            'http': 'http://127.0.0.1:1080'
        }

    def get_proxies_from_xici(self, page_num):
        print('正在从：http://www.xicidaili.com  获取代理')
        try:
            html = requests.get('https://www.xicidaili.com/nn/' + str(page_num),
                                headers={'User-Agent': self.user_agent})
        except:
            print('[www.xicidaili.com]获取失败')
            return
        soup = BeautifulSoup(html.text, 'lxml')
        trs = soup.find(id='ip_list').find_all('tr')[1:]
        for tr in trs:
            scheme = tr.find_all('td', class_='')[-3].string.lower()
            if scheme in ['http', 'https']:
                ip = tr.find_all('td', class_='')[0].string
                port = tr.find_all('td', class_='')[1].string
                proxy = scheme + '://' + ip + ':' + port
                self.proxy_list.append(proxy)

    def get_proxies_from_66(self):
        print('正在从[www.66ip.cn]获取代理')
        url = 'http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=3&start=&ports' \
              '=&export=&ipaddress=&area=1&api=66ip&proxytype='
        for i in range(0, 2):
            try:
                html = requests.get(url + str(i), timeout=5, headers={
                    'User-Agent': self.user_agent,
                    'Cookie':
                        'yd_cookie=2216480e-bd1a-4bd78eedde90079295c126faa272ce30fbc1; '
                        'Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1548774943; '
                        'Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1548856646; '
                        '_ydclearance=8dcd25662b2e346f55071654-40db-4fb8-9201-5b2c84935f42'
                        '-1549773803'
                })
            except:
                print('[www.66ip.cn]失败')
                return
            soup = BeautifulSoup(html.text, 'lxml')
            block = re.findall('\d.*?\.\d.*?\.\d.*?\.\d.*?:\d.*?\n', soup.text)
            for each in block:
                if i == 0:
                    self.proxy_list.append('http://' + each.strip())
                else:
                    self.proxy_list.append('https://' + each.strip())
            print(len(self.proxy_list))

    def search_ip_tag(self, tag):
        if tag.has_attr('class'):
            return False
        if tag.has_attr('style'):
            return tag['style'] != 'display: none;' and tag['style'] != 'display:none;'
        return True

    def search_port_tag(self, tag):
        return tag.has_attr('class')

    def get_proxies_from_goubanjia(self):
        url = 'http://www.goubanjia.com/'
        print('正在从[%s]获取代理', url)
        try:
            html = requests.get(url, timeout=5, headers={
                'User-Agent': self.user_agent
            })
            # assert html.status_code == 200
        except:
            print('[%s]代理获取失败' % url)
            return
        soup = BeautifulSoup(html.text, 'lxml')
        trs = soup.find('table', class_='table table-hover').find_all('tr', class_=[
            'success', 'warning'])
        for tr in trs:
            block = tr.find('td', class_='ip').find_all(self.search_ip_tag)
            ip = ""
            port = tr.find('td', class_='ip').find(self.search_port_tag).text
            for each in block:
                ip += each.text
            ip += ':' + port
            protocal = tr.find_all('td')[2].a.string.strip()
            print(protocal + "://" + ip)
            self.proxy_list.append(protocal + "://" + ip)

    def get_proxies_from_cn_proxy(self):
        url = 'https://cn-proxy.com/archives/218'
        print('正在从[%s]获取代理' % url)
        try:
            html = requests.get(url, timeout=5, headers={
                'User-Agent': self.user_agent
            })
            assert html.status_code == 200
        except:
            print('[%s]获取失败' % url)
            return
        soup = BeautifulSoup(html.text, 'lxml')
        tables = soup.find_all('table', class_='sortable')
        for table in tables:
            trs = table.tbody.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                ip = tds[0].string
                port = tds[1].string
                type = tds[2].string
                region = tds[3].string
                if type == '高度匿名':
                    print('http://%s:%s' % (ip, port))
                    self.proxy_list.append('http://%s:%s' % (ip, port))
                    self.proxy_list.append('https://%s:%s' % (ip, port))
        print(len(self.proxy_list))

    def get_proxies_from_free_proxy(self):
        url = 'http://free-proxy.cz/zh/proxylist/country/US/https/ping/level1/'
        print('正在从[%s]获取代理' % url)
        for i in range(1, 6):
            try:
                html = requests.get(url + str(i), headers={
                    'User-Agent': self.user_agent
                }, timeout=4, proxies={
                    'http': random.choice(self.proxy_list)
                })
                soup = BeautifulSoup(html.text, 'lxml')
                table = soup.find('table', id='proxy_list').tbody
            except:
                continue

            trs = table.find_all('tr')
            for tr in trs:
                if len(tr.find_all('td')) > 3:
                    tds = tr.find_all('td')
                    message = tds[0].script.string
                    ip = bytes.decode(base64.b64decode(
                        re.findall('Base64.decode\("(.*?)"', message)[0])).strip()
                    port = tds[1].span.string
                    protocal = tds[2].small.string.lower()
                    print("%s://%s:%s" % (protocal, ip, port))
                    self.proxy_list.append("%s://%s:%s" % (protocal, ip, port))
        print(len(self.proxy_list))

    def verify_proxies(self, proxy, verify_rul=''):
        protocal = 'https' if 'https' in proxy else 'http'
        proxies = {
            protocal: proxy
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                          'KHTML, '
                          'like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        try:
            if verify_rul == '':
                requests.get(self.verify_url, proxies=proxies, timeout=3, headers=headers)
            else:
                requests.get(verify_rul, proxies=proxies, timeout=3, headers=headers)

        except:
            print('[fail]%s' % (proxy))
        else:
            self.success_list.append(proxy)
            print('[success]%s' % proxy)

    def run(self):
        self.get_proxies_from_xici(self.total_page)
        # self.get_proxies_from_66()
        # self.get_proxies_from_goubanjia()
        # self.get_proxies_from_cn_proxy()
        # self.get_proxies_from_free_proxy()
        with ThreadPoolExecutor(5) as pool:
            [pool.submit(self.verify_proxies, proxy) for proxy in self.proxy_list]
        with open('proxies.txt', 'w') as f:
            for proxy in self.success_list:
                f.write(proxy + '\n')


if __name__ == '__main__':
    ip = GetIP(
        'https://weixin.sogou.com',
        2)
    ip.run()
