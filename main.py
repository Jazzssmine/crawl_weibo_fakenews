# coding=utf-8
from scrapy import cmdline
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def job():
    cmdline.execute("scrapy crawl toutiao".split())


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(job, trigger='interval', seconds=60 * 30,
                  next_run_time=datetime.datetime.now())
