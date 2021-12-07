import scrapy


class productItem(scrapy.Item):
    files = scrapy.Field()
    file_urls = scrapy.Field()
