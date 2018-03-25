import logging
from scraper.spiders.base_spider import BaseSpider
from scraper.items.ad_loader import AdLoader


class AutobilisSpider(BaseSpider):
    name = 'autobilis'
    urls = [
        ('Kawasaki ER6', 'http://www.autobilis.lt/skelbimai/motociklai?category_id=14&order_by=price-asc&make_id%5B%5D=7774&model_id%5B%5D=7782&year_from=2009&moto_engine_capacity_cubic_from=600&moto_engine_capacity_cubic_to=700'),
        ('Yamaha FZ6', 'http://www.autobilis.lt/skelbimai/motociklai?category_id=14&order_by=price-asc&make_id%5B%5D=8300&model_id%5B%5D=8312&model_id%5B%5D=8313&year_from=2007&moto_engine_capacity_cubic_from=530&moto_engine_capacity_cubic_to=650&city=&year_to=2010'),
        ('Yamaha XJ6', 'http://www.autobilis.lt/skelbimai/motociklai?category_id=14&order_by=price-asc&year_from=2009&moto_engine_capacity_cubic_from=530&moto_engine_capacity_cubic_to=650&city=&year_to=&make_id%5B%5D=8300&model_id%5B%5D=8357'),
        ('BMW F800ST', 'http://www.autobilis.lt/skelbimai/motociklai?category_id=14&order_by=price-asc&year_from=2006&moto_engine_capacity_cubic_from=750&moto_engine_capacity_cubic_to=1000&city=&year_to=&make_id%5B%5D=7360&model_id%5B%5D=7363'),
    ]

    def extract_items(self, response):
        return response.css('.search-rezult-content > a::attr(href)').extract()

    def next_page_url(self, response):
        return response.css('.rezult-search-pagination .cd-pagination li:last-child > a::attr(href)').extract_first()

    def parse_item_page(self, response):
        container = response.css('.main-content')

        error = container.css('.alert-inactive::text').extract_first()
        if error is not None:
            self.log('Ad is no longer active. Reason: %s. %s' % error % response.url, logging.ERROR)
            return

        il = AdLoader()
        il.add_value(None, {
            'id': 'autobilis-' + container.css('.advert-id::text').re_first(r'[\d]+'),
            'link': response.url,
            'model': response.meta['model'],
            'title': container.css('h1::text').extract_first(),
            'price': container.css('.advert-price-wrapper .price strong::text').re_first(r'[\d ]+'),
            'mileage': container.css('.car-info-r:contains("Rida, km") .car-info-c > p::text').extract_first(),
            'cubic': container.css('.car-info-r:contains("Darbinis tūris") .car-info-c > p::text').extract_first(),
            'power': container.css('.car-info-r:contains("Galia") .car-info-c > p::text').re_first(r'[\d]+(?= kW)'),
            'year': container.css('.car-info-r:contains("Metai") .car-info-c > p::text').extract_first(),
            'color': container.css('.car-info-r:contains("Spalva") .car-info-c > p::text').extract_first(),
            'description': container.css('.advert-price-MainInfo-text > span').xpath('normalize-space()').extract_first(),
            'location': container.css('.car-info-r:contains("Miestas") .car-info-c > p::text').extract_first(),
            'images': container.css('.single-item img::attr(src)').extract(),  # TODO also parse data-lazy
        })

        return il.load_item()
