FROM python:3.13.2

WORKDIR  /app


COPY . .

RUN pip install -r requriments.txt

COPY  Scrap_Autoria ./Autoria_app


EXPOSE 8000


CMD ["python", "manage.py",  "runserver", "0.0.0.0:8000"]