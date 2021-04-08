FROM ubuntu:18.04
COPY . .
RUN apt-get update
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
RUN chmod +x installDrivers.sh
RUN ./installDrivers.sh
CMD python3 main.py