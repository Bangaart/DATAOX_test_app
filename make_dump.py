import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from Scrap_Autoria.AutoRia.models import UsedCar
import os
from dotenv import load_dotenv

from pathlib import Path

load_dotenv()
USER = os.environ['POSTGRES_USER']
PASSWORD = os.environ['POSTGRES_PASSWORD']
HOST = os.environ['POSTGRES_HOST']
PORT = os.environ['POSTGRES_PORT']
DATABASE = os.environ['POSTGRES_DB']


def connect_db():
    connect_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(connect_url)
    session = sessionmaker(engine)
    return session


def dump_data(session=connect_db()):
    cars_dump = []
    with session() as session:
        statement = select(UsedCar)
        cars = session.scalars(statement).all()
        for car in cars:
            cars_dump.append({
                "id": car.id,
                "url": car.url,
                "title": car.title,
                "price_usd": car.price_usd,
                "odometer": car.odometer,
                "username": car.username,
                "phone_number": car.phone_number,
                "image_url": car.image_url,
                "images_count": car.images_count,
                "car_number": car.car_number,
                "car_vin": car.car_vin,
                "datetime_found": car.datetime_found.isoformat(),
            })

    dumps_dir = Path("dumps")
    dumps_dir.mkdir(exist_ok=True, parents=True)

    filename = "used_cars"
    i = 0

    while (dumps_dir / f"{filename}{i}.json").exists():
        i += 1

    file_path = dumps_dir / f"{filename}{i}.json"

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(cars_dump, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    dump_data(session=connect_db())