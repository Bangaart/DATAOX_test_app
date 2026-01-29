# AutoRia Scraper Project

This project scrapes used car 
listings from AutoRia and stores them in a 
PostgreSQL database. After scraping, generates dump from database.
For this app were used Scrapy framework and Selenium.
Scrapy was chosen because it is already async from the box. Selemium used only
for scrap phone number, to interact with button



---
## What was implemented 

1. Scrap all fields from requirements
2. Saved them inside Postgres
3. Dump data once after scrap script is finished
4. Make dump after scrap 
5. Env Variables inside .env
6. Launch app via docker compose and dockerfile
7. Reduce duplicates 

## What wasn't implemented 
1. Daily scrap script run (schedule scrap)
2. Daily dump (schedule dump)

## Project Structure
```
│
├── make_dump.py # Script to dump database contents from PostgreSQL
├── requirements.txt # Python dependencies
├── Dockerfile # Dockerfile for scraper container
├── docker-compose.yml # Docker Compose for app and DB
├── .env # Environment variables for DB connection
│
├── Scrap_Autoria/ # Scrapy project folder
│ ├── scrapy.cfg # Scrapy config file
│ └── AutoRia/ # Main Python package
│ ├── init.py
│ ├── items.py # Define Scrapy items
│ ├── pipelines.py # Item pipelines - pipelines use for fill database and valided data(created 3 pipelines)
│ ├── settings.py # Scrapy settings
│ ├── models.py # SQLAlchemy models
│ └── spiders/ # Folder for spiders
│ ├── init.py
│ └── autoria.py # Main spider
│
└── dumps/ # Folder where JSON dumps will be stored
```

## How to launch apps 
1. Download this project in the folder on your compute
2. open docker inside this folder and run ```docker copmose up --build```
3. After this it starts to scrap it can take a lot of time so i am finding way to limit the number of pages, now i suggest to comment the code that yields next pages (it commented by default).
4. After this script finish, dump script activates and dumps all data from BD to folder dumps




## What files and where we expect from the app
1. folder dumps will create inside the root folder of the project.
It contains JSON files with data. This files can't be overrided and all next dumps will create separately.
2. Inside project folder Autoria after script finish we can find also JSON file (used_cars) it is a backup 
on case when postgres will not work
3. Also, we have scrapy_pipeline.log file for debugging 

## Additional info 
Of course this project can be upgraded with some middlewares to pass site 
bot defense such as proxies, fingerprints, changes browsers also use playwright instead of selemium and so on
I have no much time and experience to do it well.
