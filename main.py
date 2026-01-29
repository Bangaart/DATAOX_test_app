from sqlalchemy import create_engine, select, exc
from sqlalchemy.orm import sessionmaker
from Scrap_Autoria.AutoRia.models import UsedCar

CONNECT_TO_POSTGRES_URL = f"postgresql+psycopg2://admin:1234@localhost:5432/cars"

engine = create_engine(
            CONNECT_TO_POSTGRES_URL
        )

Session = sessionmaker(engine)

with Session() as session:
            for i in range(6):
                try:
                    car = UsedCar(url="333" + str(i), title="title", price_usd=33 + i,
                                  odometer=55 + i, username="username",
                                  phone_number=33333333 + i, image_url="hello",
                                  images_count=33 + i, car_number="33rr33",
                                  car_vin=444 + i)
                    session.add(car)
                    session.commit()
                except exc.IntegrityError:
                    session.rollback()
                ("It is duplicate skip")
