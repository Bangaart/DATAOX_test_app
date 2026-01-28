import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class AutoriaSpider(scrapy.Spider):
    name = "autoria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]
    custom_settings = {
        "FEEDS": {
        "used_cars.json": {
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
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        driver.get(response.url)
        button = driver.find_element(By.XPATH,'//div[@id="sellerInfo"]//button[@data-action="showBottomPopUp"]')
        button.click()
        wait = WebDriverWait(driver, 10)
        wait.until(lambda d: d.find_element(By.XPATH, '//div[contains(@class, "popup-body")]//button[@data-action="call"]/span').text.strip() != "")
        html = driver.page_source
        response = HtmlResponse(driver.current_url, body=html, encoding='utf-8')
        phone_number = response.xpath('//div[contains(@class, "popup-body")]//button[@data-action="call"]/span/text()').get()
        driver.close()
        item = response.xpath('//div[@id="main"]')
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