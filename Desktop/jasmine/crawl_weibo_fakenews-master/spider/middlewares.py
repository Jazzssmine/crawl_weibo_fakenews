# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware


class SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(UserAgentMiddleware):
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
        "Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) "
        "Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) "
        "Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) "
        "Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
        "Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) "
        "Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) "
        "Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, "
        "like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) "
        "Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) "
        "Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) "
        "Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/43.0.2357.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]

    def process_request(self, request, spider):
        ua = random.choice(self.USER_AGENT_LIST)
        request.headers.setdefault('User-Agent', ua)


class RandomCookieMiddleware(CookiesMiddleware):
    # cookies = [
    #     {"_T_WM": "88510f592e13f85224f5d2cf249680e0",
    #      "ALF": "1554558588",
    #      "SSOLoginState": "1551966589",
    #      "MLOGIN": "1",
    #      "WEIBOCN_FROM": "1110006030",
    #      "SCF": "Ag_f8T4qg9uiN-Kts-jmnKjik99qkk417QqWSxUWfuIR7ScQmwdx1ZTv1qNkef9MG"
    #             "-iCdmrcB2Ty01KuajDaJ6M.",
    #      "SUB":
    #
    # "_2A25xhVEtDeRhGeNM6VIS9ynOzz6IHXVShn9lrDV6PUJbktAKLVLEkW1NTi0IEzrDWytbBCrTUWStS9x4Jb4EwctO",
    #      "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZLIWa7nsxoxkjsm9b5Kyi5JpX5K-hUgL.Fo"
    #              "-Eeo50S0MEShz2dJLoIExQwPWLMJiads2LxK-L12qL12eLxKqL1-zLBozLxKMLB.2LB.qt",
    #      "SUHB": "02MfezNbOQYvsK",
    #      "XSRF-TOKEN": "5b4193",
    #      "M_WEIBOCN_PARAMS": "luicode%3D10000011%26lfid%3D1076031699432410%26uicode"
    #                          "%3D20000174"
    #      },
    #     {
    #         '_T_WM': 'f6c232c91f608cd2b8f7fe303c4729d5',
    #         'SUHB': '0XDl3MjMdnLi-1',
    #         'SUB': '_2A25xzA9RDeRhGeNM41UR8yvOyDuIHXVTTpEZrDV6PUJbkdBeLRTVkW1NSfs'
    #                '-BA4T1eT4GXhHkrPwnjS8boN5YJqk',
    #         'SSOLoginState': '1556643585',
    #         'SCF': 'AnPdORTgrDn3jz2FARHBqgT0hfDN_LJyW1n3ZjwKUVXkliavjMn'
    #                '-llyIcfu9CM82hRyGDN9zwtNvT7m_tHIi1Tk.'
    #     },
    #     {
    #         '_T_WM': 'd8f682ddd4d2e0bba779aff3c859bc01',
    #         'SUHB': '05iLei6dg8l53m',
    #         'SUB': '_2A25xygmtDeRhGeRM7FYX-SzMyj6IHXVTNJflrDV6PUJbkdAKLXn4kW1NU9lV'
    #                '-mdysVxWn3yxhTnUGIqibcCCVLgA',
    #         'SSOLoginState': '1557035517',
    #         'SCF': 'AqgCqnfQfus2hZ91j7VXrwOk7Ybm5g60elWJjw4vm2'
    #                '-_Msdh9ckUEAkJkDHydfdhv7RZlQRWEuvXYrHherYvlzo.'
    #     },
    #     {
    #         '_T_WM': 'dd39d61603eae48b01c3c9f455ef45b3',
    #         'SUHB': '0ebcg-n3xPFYmU',
    #         'SUB': '_2A25xyuwLDeRhGeRJ6lQT8ybIyz'
    #                '-IHXVTNPRDrDV6PUJbkdAKLUz4kW1NUnnd3S268vV0_rEOBYDwiV9UP_SPPach',
    #         'SSOLoginState': '1557044315',
    #         'SCF': 'AvK-wNPr_2LvgNlAX932BrW1JdPW2mXEtqLFjls4fb5yX'
    #                '-fCrDKQnd6zL6zlh5sWXqwQOMtAtBKsv2AJRHl8u_g.'
    #     },
    # ]
    # cookies = [
    #     {"ALF": "1592395259",
    #      "Apache": "7641355422360.468.1550545551314",
    #      "SCF": 'ArgY-i3N6StMP1trO7TWYCPUpY6WmzfHBE7pxahb4EMA8NbGrbHL'
    #             '-WD1rtMaTtl5PmeMTzT98iocaCwzKm4KlQ4.',
    #      "SINAGLOBAL":
    #          '7641355422360.468.1550545551314',
    #      "SSOLoginState": "1560859260",
    #      "SUB": "_2A25wDKIsDeRhGeNM41UR8yvOyDuIHXVTe5TkrDV8PUNbmtAKLXbTkW9NSfs"
    #             "-BKDQ1dSaebjA1745X5U32Ow22PhY",
    #      'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWN9_YYbKrAOU_0jaRCxHX25JpX5KMhUgL.Fo'
    #              '-E1hM7e0-Ee0M2dJLoIpRLxKqL1KMLB.2LxKqL1KMLB.2LxKqL1KMLB.27eh5t',
    #      'SUHB': '0HThJwW2ufBKi1',
    #      'ULV': '1550545551318:1:1:1:7641355422360.468.1550545551314:',
    #      'UOR': ',,www.hailiangxinxi.com',
    #      '_s_tentry': 'gl.ali213.net',
    #      'cross_origin_proto': 'SSL',
    #      'login_sid_t': '34b4689164b0254a9cc5dbe5c2cef7c4',
    #      'webim_unReadCount': '%7B%22time%22%3A1560924147959%2C%22dm_pub_total%22%3A0%2C'
    #                           '%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox'
    #                           '%22%3A0%7D',
    #      'wvr': '6'
    #      }
    # ]

    cookies = [
        {

            'SINAGLOBAL': '9041156132766.867.1543458613637',
            'login_sid_t': '28b7e901a822146ba646a4f01d51fe4c',
            'cross_origin_proto': 'SSL',
            '_ga': 'GA1.2.469243942.1564582470',
            '_s_tentry': 'login.sina.com.cn',
            '__gads': 'ID=dbe5305fe93ea2ba:T=1564582472:S=ALNI_MbYaw-slDdzze_NCw7cClL2AbKspA',
            'Apache': '9622518199179.783.1564582474813',
            'ULV': '1564582474823:8:2:1:9622518199179.783.1564582474813:1562834785705',
            's_cc': 'true',
            's_sq': '%5B%5BB%5D%5D',
            'UM_distinctid': '16cb07917746ff-0a0e8989d83508-37677c02-13c680-16cb0791775754',
            'wvr': '6',
            'UOR': ',,pypi.org',
            'SCF': 'Am7Jt7ySAY5qGVf-9s3G4Of_Q9InAuL_1ZZY7JWBEh1Ek9lVOFRP4PFu9Z2OcqiwCnlwtKzenhVqTQ6n4Af_9vQ.',
            'SSOLoginState': '1566931949',
            'SUHB': '0G0uuIftjyM0Va',
            'ALF': '1569558823',
            'SUB': '_2A25wYnR3DeRhGeVK41cR8CnKyzuIHXVTrRw_rDV8PUJbkNBeLWnzkW1NTCdnpoCY4SPuBYQrrPVRgFNepqORVwHh',
            'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJcHiLLQYmQJX._sM6GNLg5JpX5oz75NHD95Q0Shnfeh5NSo5NWs4Dqc_fi--Ni-iFiKnRi--Xi-iWiKy8i--fiKysi-8si--Xi-iFi-2fi--ciK.Xi-z4i--fiK.7iKy2i--Xi-iWiKnci--fiKysiKnRi--Ri-2ciKnpi--fiK.7iKy8i--ciKnEiK.Xi--Xi-zRiKn7i--fi-z4i-zX',
            'S_ACCOUNT-G0': '8bd737c12f321cf9d9f95301c2782451',
            '_T_WM': '8ddabf447041f61bd2b060f4ef93928d',
            'webim_unReadCount': '%7B%22time%22%3A1567024240889%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A2%7D',
            'WBStorage': 'f54cf4e4362237da|undefined'
        }
    ]

    def process_request(self, request, spider):
        cookie = random.choice(self.cookies)
        request.cookies = cookie
