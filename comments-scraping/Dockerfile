FROM amd64/python:3.9-slim

RUN apt-get update -y

COPY . /app

WORKDIR /app

RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT ["python3", "-u", "comments_scraper.py"]