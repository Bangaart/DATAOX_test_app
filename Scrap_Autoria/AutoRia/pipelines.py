# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


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


#Fill PostgresSQL database

class PostgresSQLPipeline:

    def open_spider(self):
        pass
