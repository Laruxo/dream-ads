from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scraper.items.ad import Ad


class AdLoader(ItemLoader):
    default_item_class = Ad
    default_output_processor = TakeFirst()

    mileage_out = TakeFirst() or None
