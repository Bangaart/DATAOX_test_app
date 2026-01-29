# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv

from .models import UsedCar, Base

#load env variables
load_dotenv()

class AutoriaPipeline:
    def process_item(self, item, spider):
        return item

#As all items go though pipline after be scrapped i create custom pipelines for validation, transform data and fill database

class DuplicatesPipeline:
    def __init__(self):
        self.vin_codes_seen = set()

#Validation on duplicates using vin_code field

    def process_item(self, item):
        adapter = ItemAdapter(item)
        if adapter["car_vin"] in self.vin_codes_seen:
            raise DropItem(f"Duplicate item found{adapter['car_vin']}")
        else:
            self.vin_codes_seen.add(adapter["car_vin"])
            return item

#Transform string fields to in etc.

class FormatDataPipeline:

    def process_item(self, item):
        adapter = ItemAdapter(item)
        adapter["images_count"] = int(adapter["images_count"])
        adapter["phone_number"] = int( "3" + "".join([item for item in adapter["phone_number"] if item.isdigit()]))
        adapter["odometer"] = int(str("".join([item for item in adapter["odometer"] if item.isdigit()])))*1000
        adapter["price_usd"] = int(str("".join([item for item in adapter["price_usd"] if item.isdigit()])))
        return item


#Connetc and fill PostgresSQL database

class PostgresSQLPipeline:

    def __init__(self):
        self.CONNECT_TO_POSTGRES_URL = (f"postgresql+psycopg2://"
                                        f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                                        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")

        self.engine = create_engine(
            self.CONNECT_TO_POSTGRES_URL
        )

        self.Session = sessionmaker(self.engine)


    def open_spider(self, spider):
        Base.metadata.create_all(self.engine)
        spider.logger.info('Created database tables')

    def process_item(self, item):
        adapter = ItemAdapter(item)
        with self.Session() as session:
            with session.begin_nested():
                try:
                    car = UsedCar(url=adapter["url"], title=adapter["title"], price_usd=adapter["price_usd"],
                                  odometer=adapter["odometer"], username=adapter["username"],
                                  phone_number=adapter["phone_number"], image_url=adapter["image_url"],
                                  images_count=adapter["images_count"], car_number=adapter["car_number"],
                                  car_vin=adapter["car_vin"])
                    session.add(car)
                    session.commit()
                except exc.IntegrityError:
                    session.rollback()
                    print("Skipped this row already exist in database")

        return item