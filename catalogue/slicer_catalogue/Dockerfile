FROM python:3.9-slim

COPY api /api
COPY rabbitmq /rabbitmq
COPY static /static

COPY requirements.txt /
COPY main.py /

RUN apt update
RUN apt install -y build-essential

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python3 main.py