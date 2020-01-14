# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Content(scrapy.Item):
    url = scrapy.Field()
    lang = scrapy.Field()
    content = scrapy.Field()
    publisher = scrapy.Field()
    writer = scrapy.Field()
    title = scrapy.Field()
    search = scrapy.Field()
    publication_date = scrapy.Field()
    added_date = scrapy.Field()
    topics = scrapy.Field()