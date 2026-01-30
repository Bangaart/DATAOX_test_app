
import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class AutoriaSpider(scrapy.Spider):
    name = "autoria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/search/?search_type=2&page=0"]
    base_url = "https://auto.ria.com"
    max_pages = 4

    #define custom settings. Here we set up setting for JSON file for storage data as a backup copy.

    custom_settings = {
        "FEEDS": {
        "used_cars.json": {
        "format": "json",
        "encoding": "utf-8",
        "indent": 4,
        "override": True
    }
},
        "COOKIES_ENABLED": True,
        "CONCURRENT_REQUESTS": 1,
    }

    #Define webdriver from Selenium. Selenium will help us to retrieve phone number from pop up. Also, it would be done with playwright

    def __init__(self, *args, **kwargs):
        super(AutoriaSpider, self).__init__(*args, **kwargs)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)

        self.page_counter = 0

    def closed(self, reason):
        self.driver.close()

    #Here we define our page urls and cars urls(car profile). In this case parse method return responses which go to the
    # method belows (parse_car_items)
    def parse(self, response):
        self.page_counter += 1

        cars_links = response.xpath('//div[@id="items"]//a[contains(@class, "product-card")]/@href').getall()
        full_cars_urls = [self.base_url + item for item in cars_links]
        yield from response.follow_all(full_cars_urls, self.parse_car_item)

        #define next_link
        page_link = urlparse(response.url)
        queries = parse_qs(page_link.query)
        queries["page"] = [str((int(queries.get("page")[0]) + 1))]
        next_url = urlunparse(page_link._replace(query=urlencode(queries, doseq=True)))
        if (response.xpath('//button[@title="Next" and not(@disabled)]')) and self.page_counter < self.max_pages:
            yield response.follow(next_url, callback=self.parse)


    #The main logic. Here we parse the response which we get from Downloader. Use selenium to click on the phone link and invoke
    #popup where we can get the phone number. I don't use scrapy.Request because the POST method for pop up has huge and
    # hard to understanding payload

    def parse_car_item(self, response):
        self.driver.get(response.url)
        button = self.driver.find_element(By.XPATH, '//div[@id="sellerInfo"]//button[@data-action="showBottomPopUp"]')
        button.click()
        wait = WebDriverWait(self.driver, 5)
        wait.until(lambda d: d.find_element(By.XPATH,
                                            '//div[contains(@class, "popup-body")]//button[@data-action="call"]/span').text.strip() != "")

        sel = Selector(text=self.driver.page_source)
        phone_number = sel.xpath(
            '//div[contains(@class, "popup-body")]//button[@data-action="call"]/span/text()').get()
        item = response.xpath('//div[@id="main"]')

        #find appropriate values by xpath

        title = item.xpath('//div[@id="sideTitleTitle"]/span/text()').get()

        odometer = item.xpath('//div[@id="basicInfoTableMainInfo0"]/span/text()').get()
        username = item.xpath('//div[@id="sellerInfoUserName"]/span/text()').get()
        image_url = item.css(".photo-slider").xpath('//img/@src').re(r"^https:\/\/.+$")[0]
        images_count = item.xpath('//div[@id="photoSlider"]/span/span[last()]/text()').get()
        car_number = item.xpath('//div[@id="badges"]/div/span/text()').get(default="Number is not provided")
        car_vin = item.xpath('//div[@id="badgesVinGrid"]//span/text()').get()
        price_usd = item.xpath('//div[@id="sidePrice"]/strong/text()').get()

        #yield an item with dictionary filled with values we scrapped above
        cars = {
                "url": response.url,
                "title": title,
                "price_usd": price_usd,
                "odometer":  odometer,
                "username": username,
                "phone_number": phone_number,
                "image_url": image_url,
                "images_count": images_count,
                "car_number": car_number,
                "car_vin": car_vin,
            }
        yield cars
