FROM ubuntu:18.04

COPY . .

RUN apt-get update
RUN apt-get -y install \
    python3.8 \
    python3-pip=9.0.* \
    libpq-dev=10.* \
    libcurl4-openssl-dev=7.58.* \
    libssl-dev=1.1.* \
    curl=7.58.*

ARG PYTHON3_OSMCLIENT_URL
ARG PYTHON3_OSM_IM_URL

RUN curl $PYTHON3_OSMCLIENT_URL -o osmclient.deb
RUN dpkg -i ./osmclient.deb

RUN curl $PYTHON3_OSM_IM_URL -o osm_im.deb
RUN dpkg -i ./osm_im.deb


RUN pip3 install -r requirements.txt

RUN chmod +x installDrivers.sh
RUN ./installDrivers.sh

CMD python3 main.py