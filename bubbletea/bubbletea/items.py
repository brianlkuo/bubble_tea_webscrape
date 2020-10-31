# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BubbleteaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    business_name = scrapy.Field()
    rating = scrapy.Field()
    review_num = scrapy.Field()
    food_tags = scrapy.Field()
    address = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip5 = scrapy.Field()
    first_review_date = scrapy.Field()
    last_review_date = scrapy.Field()
