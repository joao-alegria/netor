# NetOr - Network Orchestrator
a distributed and scalable 5G OSS/BSS system

![](https://img.shields.io/badge/Academical%20Project-Yes-success)
![](https://img.shields.io/badge/Tests-passing-success)
![](https://img.shields.io/badge/Maintained-Yes-success)
![](https://img.shields.io/badge/Made%20With-Python-red)
![](https://img.shields.io/badge/Using%20On-Flask-red)

![](https://img.shields.io/pypi/pyversions/3)
![](https://img.shields.io/badge/Deployment-Docker-blue)

<img src="portal/src/assets/netorLogo.png" width="300px">

## Description

Current 5G vertical service orchestration solutions suffer from limitations that, if solved, would significantly increase the platforms’ quality. NetOr is a new 5G vertical service orchestration platform that solves the encountered problems and supports more intricate use cases. This new system will inherit many of the abstractions and functionalities already used, but will improve maintainability, flexibility, and scalability.

One of the main use cases supported is the ability of deploying an End-to-End Network Slice spanning across multiple domains, possible by deploying its composing Network Slice Subnets in distinct administrative domains. 

## Architecture

![](docs/netor_docs/img/architecture.png)

NetOr is based on an micro-architeture and event-driven architecture. Every module is independent and all of them communicate through the Event Bus (RabbitMQ). All components were developed using Python, all REST APIs were implemented with Flask and the entire system can be deployed and managed through Docker.

## Testing

The NetOr platform was tested via:
- Unit Tests
- Integration Tests
- Performance Tests

Finally, the main use cases were tested several times to assert if NetOr generated good results in terms of E2E delay. These tested showed that, compared to State-of-the-Art solutions, it generated considerable lower delays. 

## Authors

The author of this repository is [João Alegria](https://github.com/joao-alegria) and is being modified and improved by [Rafael Direito](https://github.com/rafael-direito), [Daniel Gomes](https://github.com/DanielGomes14), and [Pedro Bastos](https://github.com/bastos-01). This project originated as the main innovation of João Alegria's Master Thesis(classified with 19/20) with the title "Inter-domain orchestration for verticals in 5G network services" during the Masters Degree in Informatics Engineering of the University of Aveiro.

For further information, please read our [docs](https://github.com/joao-alegria/netor/tree/main/docs) or contact us.
