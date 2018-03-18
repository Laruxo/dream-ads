from scrapy.item import Item, Field
from scrapy.loader.processors import Identity, MapCompose, TakeFirst


def to_int(value):
    return int(value.replace(' ', '').replace(',', '') or '0') or None


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
    pictures = Field(input_processor=Identity(), output_processor=Identity())
    date = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
    active = Field(input_processor=TakeFirst(), output_processor=TakeFirst())
