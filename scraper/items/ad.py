from scrapy.item import Item, Field
from scrapy.loader.processors import Compose, MapCompose, TakeFirst
import json


def to_int(value):
    return int(value.replace(' ', '').replace(',', '') or '0') or None


def enlarge_images(image):
    return image\
        .replace('autogidas.lt/4_15_', 'autogidas.lt/4_26_')\
        .replace('autoplius-img.dgn.lt/ann_4_', 'autoplius-img.dgn.lt/ann_25_')


def json_encode(value):
    return json.dumps(value, ensure_ascii=False)


class Ad(Item):
    id = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    link = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    model = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    title = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    mileage = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    cubic = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    power = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    year = Field(input_processor=MapCompose(to_int), output_processor=TakeFirst())
    color = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    description = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    location = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    images = Field(input_processor=MapCompose(enlarge_images), output_processor=Compose(json_encode))
    created_at = Field()
    active = Field()
    ignored = Field()
