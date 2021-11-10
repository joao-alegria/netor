FROM mongo

COPY mongo.key /
RUN chmod 600 mongo.key
CMD [ "/usr/bin/mongod", "--auth", "--bind_ip_all", "--replSet", "rs0", "--keyFile", "mongo.key"]