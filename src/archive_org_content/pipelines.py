# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class CheckContent(object):
    def process_item(self, item, spider):
        keys = ['title', 'writer', 'publisher', 'publication_date', 'added_date']
        for key in keys:
            if item.get(key):
                item[key] = item[key].strip()
        return item