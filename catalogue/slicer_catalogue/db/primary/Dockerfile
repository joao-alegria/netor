FROM mongo:4.4

COPY mongo.key /
RUN chmod 600 mongo.key

COPY replica.js /
COPY setup.sh /docker-entrypoint-initdb.d/

#CMD [ "/usr/bin/mongod", "--auth", "--bind_ip_all", "--replSet", "rs0", "--keyFile", "mongo.key"]

#using only one replica for now, change later for master-slave arch
CMD [ "/usr/bin/mongod", "--auth", "--bind_ip_all", "--keyFile", "mongo.key"]

