import logging
import re
from scraper.spiders.base_spider import BaseSpider
from scrapy.loader import ItemLoader
from scraper.items.ad import Ad


class AutopliusSpider(BaseSpider):
    name = 'mobile'
    urls = [
        ('Kawasaki ER6', 'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&lang=en&makeModelVariant1.makeId=13100&makeModelVariant1.modelDescription=ninja&makeModelVariant2.makeId=13100&makeModelVariant2.modelDescription=EX&makeModelVariant3.makeId=13100&makeModelVariant3.modelDescription=ER6f&maxCubicCapacity=700&maxPowerAsArray=55&maxPowerAsArray=KW&maxPrice=5500&minCubicCapacity=600&minFirstRegistrationDate=2006&pageNumber=1&scopeId=MB&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING'),
        ('Yamaha FZ6', 'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&lang=en&makeModelVariant1.makeId=26000&makeModelVariant1.modelDescription=FZ6+S&maxCubicCapacity=700&maxFirstRegistrationDate=2010-12-31&minCubicCapacity=600&minFirstRegistrationDate=2004-01-01&scopeId=MB&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING'),
        ('Yamaha XJ6', 'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=WINDSHIELD&isSearchRequest=true&lang=en&makeModelVariant1.makeId=26000&makeModelVariant1.modelDescription=XJ6&maxCubicCapacity=700&maxPowerAsArray=KW&minCubicCapacity=550&minFirstRegistrationDate=2009-01-01&minPowerAsArray=KW&scopeId=MB&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING'),
        ('BMW F800ST', 'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&lang=en&makeModelVariant1.makeId=3500&makeModelVariant1.modelDescription=F800ST&maxCubicCapacity=850&maxPowerAsArray=KW&minCubicCapacity=750&minFirstRegistrationDate=2006-01-01&minPowerAsArray=KW&scopeId=MB&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING'),
        ('Suzuki SV650', 'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=WINDSHIELD&isSearchRequest=true&lang=en&makeModelVariant1.makeId=23600&makeModelVariant1.modelDescription=SV&maxCubicCapacity=700&maxPowerAsArray=KW&minCubicCapacity=550&minFirstRegistrationDate=2003-01-01&minPowerAsArray=KW&scopeId=MB&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING'),
        ('Suzuki Bandit 650', 'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED&features=WINDSHIELD&isSearchRequest=true&lang=en&makeModelVariant1.makeId=23600&makeModelVariant1.modelDescription=gsf&makeModelVariant2.makeId=23600&makeModelVariant2.modelDescription=bandit&maxCubicCapacity=700&maxPowerAsArray=KW&minCubicCapacity=550&minFirstRegistrationDate=2005-01-01&minPowerAsArray=KW&scopeId=MB&sortOption.sortBy=searchNetGrossPrice&sortOption.sortOrder=ASCENDING'),
    ]

    def extract_items(self, response):
        return response.css('.cBox-body--resultitem > .result-item::attr(href)').extract()

    def next_page_url(self, response):
        return response.css('.next-resultitems-page::attr(data-href)').extract_first()

    def parse_item_page(self, response):
        container = response.css('.cBox')

        error = container.css('.vip-error__title .u-text-red::text').extract_first()
        if error is not None:
            self.log('Ad is no longer active. Reason: %s. %s' % error % response.url, logging.ERROR)
            return

        pictures = container.css('#rbt-image-gallery img::attr(src)').extract()
        pictures.extend(container.css('#rbt-image-gallery img::attr(data-lazy)').extract())

        il = ItemLoader(Ad())
        il.add_value(None, {
            'id': 'mobile-' + container.css('.parking-block::attr(data-park-ad-id)').re_first(r'[\d]+'),
            'link': re.findall(r'.+\?id=\d+', response.url),
            'model': response.meta['model'],
            'title': container.css('#rbt-ad-title::text').extract_first(),
            'price': container.css('.rbt-prime-price::text').re_first(r'[\d,]+'),
            'mileage': container.css('#rbt-mileage-v::text').re_first(r'[\d,]+(?=\skm)'),
            'cubic': container.css('#rbt-cubicCapacity-v::text').re_first(r'[\d]+(?=\sccm)'),
            'power': container.css('#rbt-power-v::text').re_first(r'[\d]+(?=\skW)'),
            'year': container.css('#rbt-firstRegistration-v::text').re_first(r'(?<=\/)[\d]+') or '2018',
            'color': container.css('#rbt-color-v::text').extract_first(),
            'description': container.css('.description').xpath('normalize-space()').extract_first(),
            'location': container.css('#rbt-db-address').re_first(r'\w{2}-\d{5}'),
            'pictures': pictures,
        })

        return il.load_item()
