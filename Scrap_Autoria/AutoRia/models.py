from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, BigInteger


class Base(DeclarativeBase):
    pass


class UsedCar(Base):
    __tablename__ = "used_cars"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    price_usd = Column(BigInteger)
    odometer = Column(BigInteger, default=0)
    username = Column(String)
    phone_number = Column(BigInteger)
    image_url = Column(String, default="Not found")
    images_count = Column(Integer)
    car_number = Column(String, default="Not found")
    car_vin = Column(String, unique=True)
    datetime_found = Column(DateTime, default=datetime.now())
