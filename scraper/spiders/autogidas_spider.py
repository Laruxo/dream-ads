import logging
import re
from scraper.spiders.base_spider import BaseSpider
from scraper.items.ad_loader import AdLoader


class AutogidasSpider(BaseSpider):
    name = 'autogidas'
    urls = [
        ('Kawasaki ER6', 'https://autogidas.lt/skelbimai/motociklai/?f_41=2009&f_1%5B1%5D=Kawasaki&f_model_14%5B1%5D=ER&f_133=600&f_134=750&s=509969086'),
        ('Honda VFR800', 'https://autogidas.lt/skelbimai/motociklai/?f_41=2006&f_1%5B1%5D=Honda&f_model_14%5B1%5D=VFR&f_133=750&f_134=900&s=509969086'),
        ('Yamaha FZ6', 'https://autogidas.lt/skelbimai/motociklai/?f_1%5B1%5D=Yamaha&f_model_14%5B1%5D=FZ&f_41=2007&f_42=2010&f_133=550&f_134=650&s=509969086'),
        ('Yamaha XJ6', 'https://autogidas.lt/skelbimai/motociklai/?f_1%5B1%5D=Yamaha&f_model_14%5B1%5D=XJ&f_41=2009&f_133=550&f_134=650&s=509969086'),
        ('BMW F800ST', 'https://autogidas.lt/skelbimai/motociklai/?f_1%5B1%5D=BMW&f_model_14%5B1%5D=F&f_41=2006&f_133=550&f_134=900&s=509985610'),
        ('Suzuki SV650', 'https://autogidas.lt/skelbimai/motociklai/?f_1%5B1%5D=Suzuki&f_model_14%5B1%5D=SV&f_41=2004&f_133=600&f_134=750&s=509969086'),
        ('Suzuki Bandit 650', 'https://autogidas.lt/skelbimai/motociklai/?f_1%5B1%5D=Suzuki&f_model_14%5B1%5D=GSF+%2F+Bandit&f_41=2005&f_133=600&f_134=750&s=509969086'),
        ('Suzuki GSX650F', 'https://autogidas.lt/skelbimai/motociklai/?f_41=2008&f_42=2013&f_1%5B1%5D=Suzuki&f_model_14%5B1%5D=GSX&f_1%5B2%5D=Suzuki&f_model_14%5B2%5D=GSX-F+%2F+Katana&f_133=600&f_134=750&s=509969086'),
    ]

    def extract_items(self, response):
        return response.css('.item-link::attr(href)').extract()

    def next_page_url(self, response):
        return response.css('.next-page-block a::attr(href)').extract_first()

    def parse_item_page(self, response):
        container = response.css('.content-panel')

        ad_id = container.css('.times .param:last-child > .right::text').extract_first()
        if ad_id is None:
            self.log('Ad is no longer active %s' % response.url, logging.ERROR)
            return

        typePrefix = re.escape(container.css('.left:contains("Tr. priemonės tipas") ~ .right::text').extract_first() or '')

        il = AdLoader()
        il.add_value(None, {
            'id': 'autogidas-' + ad_id,
            'link': response.url,
            'model': response.meta['model'],
            'title': container.css('h1.title::text').re_first(r'(?<=^%s).+' % typePrefix),
            'price': container.css('meta[itemprop="price"]::attr(content)').extract_first(),
            'mileage': container.css('.left:contains("Rida, km") ~ .right::text').re_first(r'[0-9]+'),
            'cubic': container.css('.left:contains("Darbinis tūris") ~ .right::text').re_first(r'[0-9]+'),
            'power': container.css('.left:contains("Galia, kW") ~ .right::text').re_first(r'[0-9]+'),
            'year': container.css('.left:contains("Metai") ~ .right::text').re_first(r'^[0-9]+'),
            'color': container.css('.left:contains("Spalva") ~ .right::text').extract_first(),
            'description': container.css('.comments').xpath('normalize-space()').extract_first(),
            'location': container.css('.seller-location').xpath('normalize-space()').re_first(r'^[^,]+'),
            'images': container.css('.photo > img:not([src="/static/images/vs_map.gif"])::attr(src)').extract(),
        })

        return il.load_item()
