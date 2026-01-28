import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By


class PhoneButton(scrapy.Spider):
    name = "phone"
    custom_settings = {
    "FEEDS": {
        "phone.json": {
            "format": "json",
            "encoding": "utf-8",
            "indent": 4,
            "override": True
        }
    }

    }
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()
        self.start_urls = [url]


    async def start(self):
         for url in self.start_urls:
            self.driver.get(url)
            button = self.driver.find_element(By.XPATH, '//div[@id="sellerInfo"]//button[@data-action="showBottomPopUp"]')
            button.click()
            html = self.driver.page_source
            response = HtmlResponse(self.driver.current_url, body=html, encoding='utf-8')
            yield response

    def parse(self, response):
        phone_number = response.xpath('//button[@data-action="call"]/text()').get()
        yield {"phone_number": phone_number}


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

        # next_url = response.xpath('//link[@rel="prefetch"]/@href').get()
        # yield response.follow(next_url, callback=self.parse)

    def parse_car_item(self, response):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)

        item=  response.xpath('//div[@id="main"]')
        driver.get(response.url)
        button = driver.find_element(By.XPATH,'//div[@id="sellerInfo"]//button[@data-action="showBottomPopUp"]')
        button.click()
        html = driver.page_source
        response = HtmlResponse(driver.current_url, body=html, encoding='utf-8')
        phone_number = response.xpath('//div[@id="autoPhoneTitle"]').getall()
        with open('after_click.html', 'a', encoding='utf-8') as f:
            f.write(driver.page_source)
        yield {
                "url": response.url,
                "title": item.xpath('//div[@id="sideTitleTitle"]/span/text()').get(),
                "price_usd": item.xpath('//div[@id="sidePrice"]/strong/text()').get(),
                "odometer":  item.xpath('//div[@id="basicInfoTableMainInfo0"]/span/text()').get(),
                "username": item.xpath('//div[@id="sellerInfoUserName"]/span/text()').get(),
                "phone_number": phone_number,
                "image_url": item.css(".photo-slider").xpath('//img/@src').re("^https:\/\/.+$")[0] ,
                "images_count": item.xpath('//div[@id="photoSlider"]/span/span[last()]/text()').get(),
                "car_number": item.xpath('//div[@id="badges"]/div/span/text()').get(default="Number is not provided"),
                "car_vin": item.xpath('//div[@id="badgesVinGrid"]//span/text()').get(),
            }