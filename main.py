# coding=utf-8
import datetime
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess

from apscheduler.schedulers.blocking import BlockingScheduler
import multiprocessing


def job():
    cmdline.execute("scrapy crawl jubao".split())
    cmdline.excute("scrapy crawl jubao".split())

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=60 * 10, next_run_time=datetime.datetime.now())
def run():
    process = multiprocessing.Process(target=job)
    process.start()


if __name__ == '__main__':
    # sched.start()
    job()