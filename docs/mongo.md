# Netor Documentation - MongoDB

Even though the `catalogue` directory, contains a `docker-compose.yaml` file and `Dockerfile` for the mongoDB database, using a master-slave topology, those are not currently being used, as there were some issues regarding the mongo image versions, since **MongoDB  versions 5+ is incompatible** with the current CPUs of the IT Virtual Machines.  Thus, the solution found, and currently being used, is using Mongo Sharded images provided by [Bitnami](https://github.com/bitnami/bitnami-docker-mongodb-sharded).

To avoid the errors mentioned before, make sure to use the following image to implement the Mongo Sharded architecture:

- `docker.io/bitnami/mongodb-sharded:4.2`

