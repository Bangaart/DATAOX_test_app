import scrapy


class AutoriaSpider(scrapy.Spider):
    name = "autoria_used"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/used"]

    def parse(self, response):
        pass
