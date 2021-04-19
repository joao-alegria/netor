from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, create_engine, inspect
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import config

Base = declarative_base()

# nestedVsiTable = Table('nestedVsi', Base.metadata,
#     Column('nestedVsi', Integer, ForeignKey('verticalServiceInstance.vsiId'), primary_key=True),
#     Column('parentVsi', Integer, ForeignKey('verticalServiceInstance.vsiId'))
# )

class VerticalServiceInstance(Base):
  __tablename__ = 'verticalServiceInstance'
  vsiId = Column(Integer, primary_key=True)

  description=Column(String)
  domainId=Column(String)
  additionalConf=Column(String)
  statusMessage=Column(String)
  altitude=Column(Float)
  latitude=Column(Float)
  longitude=Column(Float)
  radioRange=Column(Float)
  mappedInstanceId=Column(String)
  name=Column(String)
  networkSliceId=Column(String)
  ranEndPointId=Column(String)
  status=Column(Integer)
  tenantId=Column(String)
  vsdId=Column(String)
  nestedParentId = Column(Integer, ForeignKey('verticalServiceInstance.vsiId'))
  nestedVsi=relationship("VerticalServiceInstance", remote_side=[vsiId])
    # parentVsi = relationship(
    #       "VerticalService",
    #       secondary=nestedVsiTable,
    #       back_populates="nestedVsi")
  nssis=relationship("NetworkSliceSubnetInstance", back_populates="vertical_service_instance")
  vssis=relationship("VerticalSubserviceInstance", back_populates="vertical_service_instance")

  # def loadJson(self,data):
  #   if "description" in data:
  #     self.description=data["description"]
  #   if "domainId" in data:
  #     self.domainIddomainId=data["domainId"]
  #   if "errorMessage" in data:
  #     self.errorMessage=data["errorMessage"]
  #   if "locationConstrains" in data:
  #     if "alt" in data["locationConstrains"]:
  #       self.altitude=data["locationConstrains"]["alt"]
  #     if "lat" in data["locationConstrains"]:
  #       self.latitude=data["locationConstrains"]["lat"]
  #     if "long" in data["locationConstrains"]:
  #       self.longitude=data["locationConstrains"]["long"]
  #     if "range" in data["locationConstrains"]:
  #       self.radioRange=data["locationConstrains"]["range"]
  #   if "mappedInstanceId" in data:
  #     self.mappedInstanceId=data["mappedInstanceId"]
  #   if "name" in data:
  #     self.name=data["name"]
  #   if "networkSliceId" in data:
  #     self.networkSliceId=data["networkSliceId"]
  #   if "ranEndPointId" in data:
  #     self.ranEndPointId=data["ranEndPointId"]
  #   if "status" in data:
  #     self.status=data["status"]
  #   if "tenantId" in data:
  #     self.tenantId=data["tenantId"]
  #   if "vsdId" in data:
  #     self.vsdId=data["vsdId"]

  # def dumpJson(self):
  #   return {"vsiId":self.vsiId,"description":self.description,"domainId":self.domainId,"errorMessage":self.errorMessage,"altitude":self.altitude,"latitude":self.latitude,"longitude":self.longitude,"radioRange":self.radioRange,"mappedInstanceId":self.mappedInstanceId,"name":self.name,"networkSliceId":self.networkSliceId,"ranEndPointId":self.ranEndPointId,"status":self.status,"tenantId":self.tenantId,"vsdId":self.vsdId,"nestedParentId":self.nestedParentId}

  # def __str__(self):
  #   return json.dumps({"vsiId":self.vsiId,"description":self.description,"domainId":self.domainId,"errorMessage":self.errorMessage,"altitude":self.altitude,"latitude":self.latitude,"longitude":self.longitude,"radioRange":self.radioRange,"mappedInstanceId":self.mappedInstanceId,"name":self.name,"networkSliceId":self.networkSliceId,"ranEndPointId":self.ranEndPointId,"status":self.status,"tenantId":self.tenantId,"vsdId":self.vsdId,"nestedParentId":self.nestedParentId})

class NetworkSliceSubnetInstance(Base):
  __tablename__ = 'networkSliceSubnetInstance'
  nssiId = Column(Integer, primary_key=True)
  domain_id=Column(String)
  ns_deployment_flavor_id=Column(String)
  ns_instantiation_level_id=Column(String)
  nsst_id=Column(String)
  status=Column(Integer)
  vertical_service_instance_id = Column(Integer, ForeignKey('verticalServiceInstance.vsiId'))
  vertical_service_instance = relationship("VerticalServiceInstance", back_populates="nssis") 
  vnfs = relationship("NetworkSliceSubnetInstanceVnfPlacement", back_populates="network_slice_subnet_instance")
  network_slice_instance_id = Column(Integer, ForeignKey('networkSliceInstance.nsiId'))
  network_slice_instance = relationship("NetworkSliceInstance", back_populates="subnets")

  # def loadJson(self,data):
  #   if "domain_id" in data:
  #     self.domain_id = data["domain_id"]
  #   if "ns_deployment_flavor_id" in data:
  #     self.ns_deployment_flavor_id = data["ns_deployment_flavor_id"]
  #   if "ns_instantiation_level_id" in data:
  #     self.ns_instantiation_level_id = data["ns_instantiation_level_id"]
  #   if "nsst_id" in data:
  #     self.nsst_id = data["nsst_id"]
  #   if "status" in data:
  #     self.status = data["status"]

  # def dumpJson(self):
  #   return {"nssiId":self.nssiId,"domain_id":self.domain_id,"ns_deployment_flavor_id":self.ns_deployment_flavor_id,"ns_instantiation_level_id":self.ns_instantiation_level_id,"nsst_id":self.nsst_id,"status":self.status,"vertical_service_instance_id":self.vertical_service_instance_id,"network_slice_instance_id":self.network_slice_instance_id}

  # def __str__(self):
  #   return json.dumps({"domain_id":self.domain_id,"ns_deployment_flavor_id":self.ns_deployment_flavor_id,"ns_instantiation_level_id":self.ns_instantiation_level_id,"nsst_id":self.nsst_id,"status":self.status,"vertical_service_instance_id":self.vertical_service_instance_id,"network_slice_instance_id":self.network_slice_instance_id})

class NetworkSliceSubnetInstanceVnfPlacement(Base):
  __tablename__ = 'networkSliceSubnetInstanceVnfPlacement'
  network_slice_subnet_instance_id = Column(Integer, ForeignKey('networkSliceSubnetInstance.nssiId'), primary_key=True)
  network_slice_subnet_instance = relationship("NetworkSliceSubnetInstance", back_populates="vnfs")
  vnf_placement_key=Column(Integer, primary_key=True)
  vnf_placement=Column(Integer)

  # def loadJson(self,data):
  #   return

  # def dumpJson(self):
  #   return {"network_slice_subnet_instance_id":self.network_slice_subnet_instance_id,"vnf_placement_key":self.vnf_placement_key,"vnf_placement":self.vnf_placement}

  # def __str__(self):
  #   return json.dumps({"network_slice_subnet_instance_id":self.network_slice_subnet_instance_id,"vnf_placement_key":self.vnf_placement_key,"vnf_placement":self.vnf_placement})

class VerticalSubserviceInstance(Base):
  __tablename__ = 'verticalSubserviceInstance'
  vssiId = Column(Integer, primary_key=True)
  blueprint_id=Column(String)
  descriptor_id=Column(String)
  domain_id=Column(String)
  instance_id=Column(String)
  vertical_service_status=Column(Integer)
  vertical_service_instance_id = Column(Integer, ForeignKey('verticalServiceInstance.vsiId'))
  vertical_service_instance = relationship("VerticalServiceInstance", back_populates="vssis")
  parameters=relationship("VerticalSubserviceInstanceParameters", back_populates="vertical_subservice_instance")

  # def loadJson(self,data):
  #   return

  # def dumpJson(self):
  #   return {"vssiId":self.vssiId,"blueprint_id":self.blueprint_id,"descriptor_id":self.descriptor_id,"domain_id":self.domain_id,"instance_id":self.instance_id,"vertical_service_status":self.vertical_service_status,"vertical_service_instance_id":self.vertical_service_instance_id}

  # def __str__(self):
  #   return json.dumps({"vssiId":self.vssiId,"blueprint_id":self.blueprint_id,"descriptor_id":self.descriptor_id,"domain_id":self.domain_id,"instance_id":self.instance_id,"vertical_service_status":self.vertical_service_status,"vertical_service_instance_id":self.vertical_service_instance_id})

class VerticalSubserviceInstanceParameters(Base):
  __tablename__ = 'verticalSubserviceInstanceParameters'
  vertical_subservice_instance_id = Column(Integer, ForeignKey('verticalSubserviceInstance.vssiId'), primary_key=True)
  vertical_subservice_instance = relationship("VerticalSubserviceInstance", back_populates="parameters")
  parameters_key=Column(Integer, primary_key=True)
  parameters=Column(String)

  # def loadJson(self,data):
  #   return

  # def dumpJson(self):
  #   return {"vertical_subservice_instance_id":self.vertical_subservice_instance_id,"parameters_key":self.parameters_key,"parameters":self.parameters}

  # def __str__(self):
  #   return json.dumps({"vertical_subservice_instance_id":self.vertical_subservice_instance_id,"parameters_key":self.parameters_key,"parameters":self.parameters})

class NetworkSliceInstance(Base):
  __tablename__ = 'networkSliceInstance'
  nsiId = Column(Integer, primary_key=True)
  name = Column(String)
  description = Column(String)
  nstId = Column(String)
  nsdId = Column(String)
  nsdVersion = Column(String)
  dfId = Column(String)
  instantiationLevelId = Column(String)
  oldInstantiationLevelId = Column(String)
  nfvNsId = Column(String)
  soManaged = Column(Boolean)
  tenantId = Column(String)
  status = Column(Integer)
  errorMessage = Column(String)
  nfvNsUrl = Column(String)
  subnets=relationship("NetworkSliceSubnetInstance", back_populates="network_slice_instance")
  vnfs = relationship("NetworkSliceInstanceVnfPlacement", back_populates="network_slice_instance")

  # def loadJson(self,data):
  #   pass

  # def dumpJson(self):
  #   return {"nsiId":self.nsiId,"name":self.name,"description":self.description,"nstId":self.nstId,"nsdId":self.nsdId,"nsdVersion":self.nsdVersion,"dfId":self.dfId,"instantiationLevelId":self.instantiationLevelId,"oldInstantiationLevelId":self.oldInstantiationLevelId,"nfvNsId":self.nfvNsId,"soManaged":self.soManaged,"tenantId":self.tenantId,"status":self.status,"errorMessage":self.errorMessage,"nfvNsUrl":self.nfvNsUrl}

  # def __str__(self):
  #   return json.dumps({"nsiId":self.nsiId,"name":self.name,"description":self.description,"nstId":self.nstId,"nsdId":self.nsdId,"nsdVersion":self.nsdVersion,"dfId":self.dfId,"instantiationLevelId":self.instantiationLevelId,"oldInstantiationLevelId":self.oldInstantiationLevelId,"nfvNsId":self.nfvNsId,"soManaged":self.soManaged,"tenantId":self.tenantId,"status":self.status,"errorMessage":self.errorMessage,"nfvNsUrl":self.nfvNsUrl})

class NetworkSliceInstanceVnfPlacement(Base):
  __tablename__ = 'netwokSliceInstanceVnfPlacement'
  network_slice_instance_id = Column(Integer, ForeignKey('networkSliceInstance.nsiId'), primary_key=True)
  network_slice_instance = relationship("NetworkSliceInstance", back_populates="vnfs")
  vnf_placement_key=Column(Integer, primary_key=True)
  vnf_placement=Column(Integer)

  # def loadJson(self,data):
  #   pass

  # def dumpJson(self):
  #   return {"network_slice_instance_id":self.network_slice_instance_id,"vnf_placement_key":self.vnf_placement_key,"vnf_placement":self.vnf_placement}

  # def __str__(self):
  #   return json.dumps({"network_slice_instance_id":self.network_slice_instance_id,"vnf_placement_key":self.vnf_placement_key,"vnf_placement":self.vnf_placement})



engine = create_engine('postgresql://'+str(config.POSTGRES_USER)+':'+str(config.POSTGRES_PASS)+'@'+str(config.POSTGRES_IP)+':'+str(config.POSTGRES_PORT)+'/'+str(config.POSTGRES_DB))
try:
  Base.metadata.create_all(engine)
except Exception as e:
  if "does not exist" in str(e):
    tmpengine=create_engine('postgresql://'+str(config.POSTGRES_USER)+':'+str(config.POSTGRES_PASS)+'@'+str(config.POSTGRES_IP)+':'+str(config.POSTGRES_PORT)+'/postgres')
    conn = tmpengine.connect()
    conn.execute("commit")
    conn.execute("create database \""+str(config.POSTGRES_DB)+"\"")
    conn.close()
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session=Session()
def persist(entity):
  session.add(entity)
  session.commit()

def delete(entity):
  session.delete(entity)
  session.commit()