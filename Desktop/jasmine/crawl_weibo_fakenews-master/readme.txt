使用的是Scrapy框架

解压后
requiremens.txt	里是用到的库

main.py	是主函数，其他部分修改好之后运行这个文件

spider/middlewares.py	是中间件，里面有登录用的Cookie，没发现被封的情况，基本不需要改，如果后续爬取出302可以改RandomCookieMiddleware里的cookies

spider/settings.py	是爬虫的设置，CONCURRENT_REQUESTS是一次请求的链接数量，最大好像是支持32吧；DOWNLOAD_DELAY是访问延迟，不被封设0就好

spider/spiders/jubao_spider.py	爬虫。	max_page_num设置最大页码数量。这个网页会更新数据导致页码数增加，为了避免重复数据，爬虫是从后往前爬的。但必然会漏掉一小部分的数据；
										file_dir设置文件存储的路径，策略是一页20条数据存成一个文本文件。