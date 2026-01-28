from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from Scrap_Autoria.AutoRia.models import UsedCar

CONNECT_TO_POSTGRES_URL = f"postgresql+psycopg2://admin:1234@localhost:5432/cars"

engine = create_engine(
            CONNECT_TO_POSTGRES_URL
        )

Session = sessionmaker(engine)

with Session() as session:
    statment = select(UsedCar).where(UsedCar.id == 1)
    cars = session.execute(statment).fetchall()
    print(cars)