#!/usr/bin/env python
#-*-coding:utf-8-*-
import os
import scrapy
from urllib.parse import urljoin
from uukanshu.items import UUKanShuItem

class UUKanShuSpdier(scrapy.Spider):
    name = "uukanshu"

    def start_requests(self):
        # get url from cli args
        url = self.settings.get('START_URL')
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = UUKanShuItem()
        cur_url = response.url
        item['url'] = cur_url

        title = response.xpath(u'//*[@id="timu"]/text()').extract()
        if title:
            title = [i.strip() for i in title]
            item['title'] = title[0]

        content = self._process_content(response)
        item['content'] = content

        next_page = response.xpath(u'//*[@id="next"]/@href').extract()
        if next_page:
            next_page = [i.strip() for i in next_page]
            # if next_page doesn't contain 'html', it is not a valid next page url
            if 'html' in next_page[0]:
                next_url = urljoin(cur_url, next_page[0])
                item['next_url'] = next_url
                total_page = self.settings.get('TOTAL')
                cur_page = response.meta.get('cur_page', 1)
                if cur_page < total_page:
                    req = scrapy.Request(url=next_url, callback=self.parse)
                    req.meta['cur_page'] = cur_page + 1
                    yield req
        yield item
        self._write_to_txt(item)

    def _process_content(self, response):
        contents = response.xpath(u'//*[@id="contentbox"]//p/text()').extract()
        if not contents:
            contents = response.xpath(u'//*[@id="contentbox"]//text()').extract()
        if not contents:
            print('No content data, maybe the xpath rule is out of date.')
            return ''
        else:
            content = ''
            for line in contents:
                line = self._clean_content(line)
                line = line.strip()
                if not line:
                    continue
                content += line + os.linesep
            return content

    def _clean_content(self, content:str):
        keys = [
            u'最新小说百度搜索',
            u'UＵ看书',
            u'UU看书',
            u'wｗw．uukaｎshu.com',
            u'www.uukanshｕ.com',
            u'www.uukanｓhu.ｃｏm',
            u'(adsbygoogle = window.adsbygoogle || []).push({});',
        ]
        for key in keys:
            content = content.replace(key, '')
        return content

    def _write_to_txt(self, item):
        filename = self.settings.get('FILENAME', 'novel.txt')
        with open(filename, 'a+') as f:
            f.write(item['title'] + os.linesep)
            f.write(item['url'] + os.linesep)
            f.write(item['content'])
