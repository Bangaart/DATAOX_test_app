from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime


class Base(DeclarativeBase):
    __tablename__ = "used_cars"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    price_usd = Column(Integer)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(Integer)
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String, unique=True)
    datetime_found = Column(DateTime, default=datetime.now())
