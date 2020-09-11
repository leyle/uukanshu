#!/usr/bin/env python
#-*-coding:utf-8-*-
import sys
import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from uukanshu.spiders.uukanshu_spider import UUKanShuSpdier

def run(args):
    start_url = args.url
    filename = args.name
    total = args.total

    settings = get_project_settings()
    settings.set('START_URL', start_url)
    settings.set('FILENAME', filename)
    settings.set('TOTAL', total)

    crawler_process = CrawlerProcess(settings)
    crawler_process.crawl(UUKanShuSpdier)
    crawler_process.start()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', default=None, help=u"./start.py -u first chapter url")
    parser.add_argument('-n', '--name', default='novel.txt', help=u'./start.py -n path/to/novelname.txt')
    parser.add_argument('-t', '--total', default=sys.maxsize, help=u'set how many pages to crawl')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    if not args.url:
        print('Need start url, use -h to get help')
        exit(1)
    total = args.total
    try:
        total = int(total)
    except Exception as e:
        print(e)
        exit(1)
    else:
        args.total = total
    print(args)
    run(args)

