#FROM python:3.9.13-alpine3.15
#FROM python:3.10.4-alpine3.15
#better debian, because contains more packages that are necessary to pandas
FROM python:3.10.4-slim-bullseye
#FROM python:3.10.4-bullseye
#FROM ubuntu:22.04

WORKDIR /home/Reddit
COPY . /home/Reddit

RUN cp -R ML /home

#installations necessary to pandas
#RUN apt update && \
#    apt install -y gcc && \
#    apt install -y g++
RUN apt update && apt install -y unixodbc unixodbc-dev

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


#CMD ["python3", "reddit_post_manager.py"]
CMD [ "sleep", "3600d" ]