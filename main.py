# coding=utf-8
import datetime
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from spider.spiders.toutiao_spider import XuanchuanbuSpider
from apscheduler.schedulers.blocking import BlockingScheduler
import multiprocessing


def job():
    # cmdline.execute("scrapy crawl toutiao --nolog".split())
    cmdline.execute("scrapy crawl toutiao".split())


sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=60 * 10, next_run_time=datetime.datetime.now())
def run():
    process = multiprocessing.Process(target=job)
    process.start()


if __name__ == '__main__':
    # sched.start()
    job()
