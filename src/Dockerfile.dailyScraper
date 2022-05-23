#FROM python:3.9.13-alpine3.15
FROM python:3.10.4-alpine3.15
#FROM python:3.10.4-bullseye
#FROM ubuntu:22.04
#FROM python:3.10.4-slim-bullseye

WORKDIR /home/Scraper
COPY . /home/Scraper

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#CMD ["python3", "scraper.py"]
CMD [ "sleep", "3600d" ]