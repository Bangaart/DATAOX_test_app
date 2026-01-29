FROM python:3.13.2

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR  /app/Scrap_Autoria/Autoria


COPY . ./app

RUN pip install --no-cache-dir -r app/requirements.txt
RUN pip install webdriver-manager

EXPOSE 8000

CMD sh -c "scrapy crawl autoria && python /app/make_dump.py"
