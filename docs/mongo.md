# Netor Documentation - MongoDB

Even though the `catalogue/db` directory, contains a `docker-compose.yaml` file and `Dockerfile` for the mongoDB database, using a master-slave topology, those are not currently being used, as there were some issues:

-  MongoDB image versions:  since **MongoDB  versions 5+ is incompatible** with the current CPUs of the IT Virtual Machines, the containers deployed could not perform any operations regarding this database.
- Recently Created Volumes: When the volumes are created for the first time, the mongoDB initalization script was not being ran. Therefore,  it was needed to manually run the script, or redeploy all services through `docker-compose`, which is not pratical neither dinamic.



Thus, the solution found, and currently being used, is using **Mongo Sharded** images provided by [Bitnami](https://github.com/bitnami/bitnami-docker-mongodb-sharded). To avoid the image version error mentioned before, make sure to use the following image to implement the Mongo Sharded architecture:

- `docker.io/bitnami/mongodb-sharded:4.2`

