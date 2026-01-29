
import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class AutoriaSpider(scrapy.Spider):
    name = "autoria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]

    #define custom settings. Here we set up setting for json file for storage data as a backup copy.
    #Cookies = False,to not provide cookie and try to escape
    #site defense against bots (it doesn't work in my case)

    custom_settings = {
        "FEEDS": {
        "used_cars.json": {
        "format": "json",
        "encoding": "utf-8",
        "indent": 4,
        "override": True
    }
},
        "COOKIES_ENABLED": True
    }

    #Define webdriver from Selenium. Selenium will help us to retrieve phone number from pop up. Also it would be done with playwright

    def __init__(self, *args, **kwargs):
        super(AutoriaSpider, self).__init__(*args, **kwargs)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)

    def closed(self, reason):
        self.driver.close()


    #Here we define our page urls and cars urls(car profile). In this case parse method return responses which go to the
    # method belows (parse_car_items)
    #I manually restricted only to 2 pages for demo purpose and also i have problem with site bots defense.
    #To avoid it we can use for example proxies and other techniques but i have no enough experience but the main problem is time resource

    def parse(self, response):
        cars_links = response.xpath('//div[@class="content"]//a/@href').re(r"^https:\/\/.+$")
        yield from response.follow_all(cars_links, self.parse_car_item)

#here you can change numbers of pages to scrap
        for i in range(2):
            next_url = response.xpath('//link[@rel="prefetch"]/@href').get()
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
        image_url = item.css(".photo-slider").xpath('//img/@src').re("^https:\/\/.+$")[0]
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