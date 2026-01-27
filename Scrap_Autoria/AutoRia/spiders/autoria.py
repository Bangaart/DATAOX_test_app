import scrapy


class AutoriaSpider(scrapy.Spider):
    name = "autoria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]
    custom_settings = {
        "FEEDS": {
        "cars.json": {
        "format": "json",
        "encoding": "utf-8",
        "indent": 4,
        "override": True
    }
},
        "COOKIES_ENABLED": False
    }


    def parse(self, response):
        cars_links = response.xpath('//div[@class="content"]//a/@href').re(r"^https:\/\/.+$")
        yield from response.follow_all(cars_links, callback=self.parse_car_item)

        next_url = response.xpath('//link[@rel="prefetch"]/@href').get()
        yield response.follow(next_url, callback=self.parse)

    def parse_car_item(self, response):
        for item  in response.xpath('//div[@id="main"]'):
            yield {
                "url": response.url,
                "title": item.xpath('//div[@id="sideTitleTitle"]/span/text()').get(),
                "price_usd": item.xpath('//div[@id="sidePrice"]/strong/text()').get(),
                "odometer":  item.xpath('//div[@id="basicInfoTableMainInfo0"]/span/text()').get(),
                "username": item.xpath('//div[@id="sellerInfoUserName"]/span/text()').get(),
                "phone_number": item.xpath('//div[@id="sellerInfoPhoneNumber"]/text()').get(default="Not found"),
                "image_url": item.css(".photo-slider").xpath('//img/@src').re("^https:\/\/.+$")[0] ,
                "images_count": item.xpath('//div[@id="photoSlider"]/span/span[last()]/text()').get(),
                "car_number": item.xpath('//div[@id="badges"]/div/span/text()').get(default="Number is not provided"),
                "car_vin": item.xpath('//div[@id="badgesVinGrid"]//span/text()').get(),
            }