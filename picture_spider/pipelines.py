# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class PictureSpiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        """ 这里做了一个查重判断，如果跟数据库重复则不进行下载"""
        for img_url in item['img_urls']:
            yield scrapy.Request(img_url,meta={'item':item,'dont_proxy':True})

    def item_completed(self, results, item, info):
        """ 如果下载的文件为空，则 img_paths 为空，就会删除掉item，也就不会保存至数据库"""
        img_paths = [x['path'] for ok, x in results if ok]
        if not img_paths:
            print(results)
            raise DropItem('Item contains no images')
        return item
