# -*- coding: utf-8 -*-
import scrapy
from ..items import Content


class Spider01Spider(scrapy.Spider):
    name = 'spider01'
    allowed_domains = ['archive.org']

    def start_requests(self):
        search_words = [
            # ('story', 'English'),
            # ('récit', 'French'),
            # ('storia', 'Italian'),
            # ('история', 'Russian'),
            # ('historia', 'Spanish'),
            ('Geschichte', 'German'),
            ('कहानी', 'Hindi'),
            ('قصة', 'Arabic')
            # ('物語', 'Japanese'),
            # ('داستان', 'Persian')
            # ('故事', 'Chinese')
        ]
        base_url = 'https://archive.org/search.php?query={0}&and[]=languageSorter%3A%22{1}%22&and[]=mediatype%3A%22texts%22&and[]=loans__status__status%3A%22-1%22'
        for search in search_words:
            url = base_url.format(search[0], search[1])
            yield scrapy.Request(url, callback=self.parse, meta={'search': search})

    def parse(self, response):
        search = response.meta['search']
        number_of_titles = response.css('.results_count::text').get()
        if number_of_titles is not None:
            number_of_titles = number_of_titles.strip()
            number_of_titles = number_of_titles.replace(',', '')
            number_of_titles = int(number_of_titles)
            number_of_titles /= 50
            number_of_titles = int(number_of_titles)
        else:
            number_of_titles = 100
        for i in range(number_of_titles):
            url = 'https://archive.org/search.php?query={0}&and%5B%5D=languageSorter%3A%22{1}%22&and%5B%5D=mediatype%3A%22texts%22&and%5B%5D=loans__status__status%3A%22-1%22&page={2}'.format(search[0], search[1], i)
            yield scrapy.Request(url, callback=self.parse_titles, meta={'search_key': search[0], 'lang': search[1]})

    def parse_titles(self, response):
        lang = response.meta['lang']
        search_key = response.meta['search_key']
        data = response.css('.item-ia')
        for d in data:
            content = Content()
            content['title'] = d.css('.ttl::text').get()
            content['publisher'] = d.css('.item-parent-ttl::text').get()
            content['writer'] = d.css('.byv::text').get()
            content['lang'] = lang
            content['search'] = search_key
            content['url'] = response.urljoin(d.xpath('.//a[@title]').xpath('@href').get())
            request = scrapy.Request(content.get('url'), callback=self.parse_content, meta={'content': content})
            yield request

    def parse_content(self, response):
        content = response.meta['content']
        download_urls = response.css('.download-pill').xpath('@href')
        txt_url = None
        for i in download_urls:
            if i.get().endswith('.txt'):
                txt_url = response.urljoin(i.get())

        details = response.css('.metadata-definition')

        # lang = None
        # for i in details:
        #     if i.xpath('.//dt/text()').get() == 'Language':
        #         lang = i.xpath('.//a/text()').get()

        publication_date = None
        for i in details:
            if i.xpath('.//dt/text()').get() == 'Publication date':
                publication_date = i.xpath('.//span/text()').get()

        added_date = None
        for i in details:
            if i.xpath('.//dt/text()').get() == 'Addeddate':
                added_date = i.xpath('.//dd/text()').get()

        topics = None
        for i in details:
            if i.xpath('.//dt/text()').get() == 'Topics':
                topics = i
        if topics:
            topics = topics.xpath('.//a/text()').getall()

        # content['lang'] = lang
        content['publication_date'] = publication_date
        content['added_date'] = added_date
        content['topics'] = topics

        request = scrapy.Request(txt_url, callback=self.parse_get_content, meta={'content': content})
        yield request

    def parse_get_content(self, response):
        content = response.meta['content']
        data = response.xpath('//pre/text()').get()
        content['content'] = data
        yield content
