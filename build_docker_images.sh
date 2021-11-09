#!/bin/bash

# Author : Rafael Direito (rdireito@av.it.pt)
# Copyright (c) Instituto de Telecomunicações  - Aveiro
# Date: November 9th, 2021

while test $# -gt 0
do
    case "$1" in
        all) 
            echo "Building all images..."
            docker build ./catalogue/slicer-catalogue/db/primary -t netor/mongo1 --no-cache	
            docker build ./catalogue/slicer-catalogue/db/secondary1 -t netor/mongo2 --no-cache	
            docker build ./catalogue/slicer-catalogue/db/secondary2 -t netor/mongo3 --no-cache	
            docker build ./coordinator -t netor/coordinator --no-cache		
            docker build ./manager -t netor/manager --no-cache	
            docker build ./placement -t netor/placement --no-cache	
            docker build ./tenant -t netor/tenant --no-cache	
            docker build ./catalogue/slicer-catalogue -t netor/catalogue --no-cache	
            docker build ./catalogue/portal -t netor/portal --no-cache	
            docker build ./domain -t netor/domain --no-cache \
                --build-arg PYTHON3_OSM_IM_URL='https://artifactory-osm.etsi.org/artifactory/osm-IM/v11.0/2/pool/IM/python3-osm-im_9.0.0.post19+g1ab5b68-1_all.deb' \
                --build-arg PYTHON3_OSMCLIENT_URL='https://artifactory-osm.etsi.org/artifactory/osm-osmclient/v10.0/14/pool/osmclient/python3-osmclient_10.0.3+gc0a69f8-1_all.deb'
            ;;
        mongo1) echo "Building the mongo1's image..."
            docker build ./catalogue/slicer-catalogue/db/primary -t netor/mongo1 --no-cache	
            ;;
        mongo2) echo "Building the mongo2's image..."
            docker build ./catalogue/slicer-catalogue/db/secondary1 -t netor/mongo2 --no-cache	
            ;;
        mongo3) echo "Building the mongo3's image..."
            docker build ./catalogue/slicer-catalogue/db/secondary2 -t netor/mongo3 --no-cache	
            ;;
        coordinator) echo "Building the coordinator's image..."
            docker build ./coordinator -t netor/coordinator --no-cache	
            ;;
        domain) echo "Building the domain's image..."
            docker build ./domain -t netor/domain --no-cache \
                --build-arg PYTHON3_OSM_IM_URL='https://artifactory-osm.etsi.org/artifactory/osm-IM/v11.0/2/pool/IM/python3-osm-im_9.0.0.post19+g1ab5b68-1_all.deb' \
                --build-arg PYTHON3_OSMCLIENT_URL='https://artifactory-osm.etsi.org/artifactory/osm-osmclient/v10.0/14/pool/osmclient/python3-osmclient_10.0.3+gc0a69f8-1_all.deb'
            ;;
        manager) echo "Building the manager's image..."
            docker build ./manager -t netor/manager --no-cache	
            ;;
        placement) echo "Building the placement's image..."
            docker build ./placement -t netor/placement --no-cache	
            ;;
        tenant) echo "Building the tenant's image..."
            docker build ./tenant -t netor/tenant --no-cache	
            ;;
        catalogue) echo "Building the placement's image..."
            docker build ./catalogue/slicer-catalogue -t netor/catalogue --no-cache	
            ;;
        portal) echo "Building the portal's image..."
            docker build ./catalogue/portal -t netor/portal --no-cache	
            ;; 
    esac
    shift
done

exit 0
