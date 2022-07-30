FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

WORKDIR .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install psycopg2-binary

COPY . .

CMD scrapy crawl spider
