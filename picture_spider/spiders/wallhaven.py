# -*- coding: utf-8 -*-
import scrapy
import re
from picture_spider.items import PictureSpiderItem


class PixabaySpider(scrapy.Spider):
    name = 'wallhaven'
    size = '21x9'

    def start_requests(self):
        url = 'https://wallhaven.cc/search?categories=100&purity=100&ratios={}&sorting=relevance&order=desc'.format(self.size)
        yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        context = response.css('h1::text').extract_first()
        print(context)
        counts = re.findall('(.*?) Wallpapers found', context)
        if counts:
            counts = int(re.sub(',', '', counts[0]))
            pages = counts // 24 + 1
        else:
            print(counts)
            print('获取图片数量出错，抓取终止')
            pages = 0
        for page in range(1,pages+1):
            url = 'https://wallhaven.cc/search?categories=100&purity=100&ratios={}&sorting=relevance&order=desc&page={}'.format(self.size, page)
            yield scrapy.Request(url,callback=self.parse_page)

    def parse_page(self, response):
        urls = response.css('.thumb-listing-page ul li a.preview::attr(href)').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = PictureSpiderItem()
        item['img_urls'] = response.css('img#wallpaper::attr(src)').extract()
        yield item
