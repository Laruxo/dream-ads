import logging
from scraper.spiders.base_spider import BaseSpider
from scraper.items.ad_loader import AdLoader


class AutopliusSpider(BaseSpider):
    name = 'autoplius'
    urls = [
        ('Kawasaki ER6', 'https://autoplius.lt/skelbimai/motociklai-moto-apranga/motociklai?category_id=3&engine_capacity_from=600&engine_capacity_to=700&make_date_from=2009&make_id%5B1590%5D=2049_18710_25823&make_id_list=1590&slist=421324377'),
        ('Yamaha FZ6', 'https://autoplius.lt/skelbimai/motociklai-moto-apranga/motociklai?category_id=3&engine_capacity_from=500&engine_capacity_to=750&make_date_from=2007&make_date_to=2010&make_id%5B1621%5D=2294&make_id_list=1621&slist=453446453'),
        ('Yamaha XJ6', 'https://autoplius.lt/skelbimai/motociklai-moto-apranga/motociklai?category_id=3&engine_capacity_from=500&engine_capacity_to=750&make_date_from=2009&make_id%5B1621%5D=2291&make_id_list=1621&slist=421324377'),
        ('BMW F800ST', 'https://autoplius.lt/skelbimai/motociklai-moto-apranga/motociklai?category_id=3&engine_capacity_from=750&engine_capacity_to=900&make_date_from=2006&make_id%5B1563%5D=25947_25959&make_id_list=1563&slist=421324377'),
    ]

    def extract_items(self, response):
        return response.css('.announcement-item::attr(href)').extract()

    def next_page_url(self, response):
        return response.css('.pagination a.next::attr(href)').extract_first()

    def parse_item_page(self, response):
        container = response.css('.content-container')

        error = container.css('.error .msg-subject::text').extract_first()
        if error is not None:
            self.log('Ad is no longer active. Reason: %s. %s' % (error, response.url), logging.ERROR)
            return

        sold = container.css('.is-sold-badge::text').extract_first()
        if sold is not None:
            self.log('Ad is no longer active. Reason: %s. %s' % (sold, response.url), logging.ERROR)
            return

        il = AdLoader()
        il.add_value(None, {
            'id': 'autoplius-' + container.css('.announcement-id > strong::text').re_first(r'[^ID: ].+'),
            'link': response.url,
            'model': response.meta['model'],
            'title': container.css('h1::text').re_first(r'^[^,]+'),
            'price': container.css('.view-price::text').re_first(r'[\d ]+'),
            'mileage': container.css('tr:contains("Rida") strong::text').re_first(r'[\d ]+'),
            'cubic': container.css('tr:contains("Variklis") strong::text').re_first(r'^[\d]+'),
            'power': container.css('tr:contains("Variklis") strong::text').re_first(r'[\d]+(?=kW)'),
            'year': container.css('tr:contains("Pagaminimo data") strong::text').re_first(r'^[\d]+'),
            'color': container.css('tr:contains("Spalva") strong::text').extract_first(),
            'description': container.css('.announcement-description').xpath('normalize-space()').extract_first(),
            'location': container.css('.owner-location').xpath('normalize-space()').re_first(r'^[^,]+'),
            'images': container.css('.announcement-media-gallery > .thumbnail::attr(style)').re(r'https:\/\/.+\.jpg'),
        })

        return il.load_item()
