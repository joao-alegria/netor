#!/bin/bash
#until mongo < /replica.js
#do
#  echo "..."
#  sleep 1
#done


until mongo --eval "admin = db.getSiblingDB(\"admin\"); admin.createUser({user: \"$MONGO_INITDB_ROOT_USERNAME\", pwd: \"$MONGO_INITDB_ROOT_PASSWORD\", roles: [ { role: \"userAdminAnyDatabase\", db: \"admin\" }]})"
do
    echo "..."
    sleep 1
done

until mongo --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --eval "db=db.getSiblingDB('$CATALOGUES_DATABASE'); db.createUser({user: \"$CATALOGUES_USERNAME\",pwd: \"$CATALOGUES_PASSWORD\" ,roles: [ { role: \"dbOwner\" , db: \"$CATALOGUES_DATABASE\" } ]})"
do
  echo "..."
  sleep 1
dones