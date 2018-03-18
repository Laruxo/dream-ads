import scrapy
import logging


class BaseSpider(scrapy.Spider):
    dont_cache_lists = False
    dont_cache_items = False

    urls = []

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url[1],
                callback=self.parse,
                meta={'dont_cache': self.dont_cache_lists, 'model': url[0]}
            )

    def closed(self, reason):
        self.log('Spider closed. %s' % reason, logging.ERROR)

    def extract_items(self, response):
        raise NotImplementedError('extract_items is not defined'.format(self.__class__.__name__))

    def next_page_url(self, response):
        raise NotImplementedError('next_page_url is not defined'.format(self.__class__.__name__))

    def parse(self, response):
        items = self.extract_items(response)
        if items is None:
            self.log('No items available. %s' % response.status, logging.ERROR)
            return

        for item_link in items:
            yield response.follow(
                url=item_link,
                callback=self.parse_item_page,
                meta={'dont_cache': self.dont_cache_items, 'model': response.meta['model']}
            )

        next_page = self.next_page_url(response)
        if next_page is not None:
            yield response.follow(
                url=next_page,
                callback=self.parse,
                meta={'dont_cache': self.dont_cache_lists, 'model': response.meta['model']}
            )

    def parse_item_page(self, response):
        raise NotImplementedError('parse_item_page is not defined'.format(self.__class__.__name__))
