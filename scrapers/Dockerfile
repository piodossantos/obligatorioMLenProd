FROM python:3-slim-buster
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [ "scrapy", "crawl", "gallito" ]