# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionAnswerItem(scrapy.Item):
    data_rows = scrapy.Field()