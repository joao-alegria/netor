from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, create_engine, inspect
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import config

class DB:

    def __init__(self, Base):
        super().__init__()
        self.Base=Base

    def persist(self,entity):
        self.session.add(entity)
        self.session.commit()

    def delete(self,entity):
        self.session.delete(entity)
        self.session.commit()

    def createDB(self):
        if config.ENVIRONMENT=="testing":
            self.engine = create_engine('sqlite:///:memory:')
        else:
            self.engine = create_engine('postgresql://'+str(config.POSTGRES_USER)+':'+str(config.POSTGRES_PASS)+'@'+str(config.POSTGRES_IP)+':'+str(config.POSTGRES_PORT)+'/'+str(config.POSTGRES_DB))
        try:
          self.Base.metadata.create_all(self.engine)
        except Exception as e:
          if "does not exist" in str(e):
            tmpengine=create_engine('postgresql://'+str(config.POSTGRES_USER)+':'+str(config.POSTGRES_PASS)+'@'+str(config.POSTGRES_IP)+':'+str(config.POSTGRES_PORT)+'/postgres')
            conn = tmpengine.connect()
            conn.execute("commit")
            conn.execute("create database \""+str(config.POSTGRES_DB)+"\"")
            conn.close()
            Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session=Session()


    def removeDB(self):
        self.Base.metadata.drop_all(self.engine)
        self.session.close()



Base = declarative_base()
DB=DB(Base)

# nestedVsiTable = Table('nestedVsi', Base.metadata,
#     Column('nestedVsi', Integer, ForeignKey('verticalServiceInstance.vsiId'), primary_key=True),
#     Column('parentVsi', Integer, ForeignKey('verticalServiceInstance.vsiId'))
# )

class VerticalServiceInstance(Base):
  __tablename__ = 'verticalServiceInstance'
  vsiId = Column(String, primary_key=True)
  description=Column(String)
  domainId=Column(String)
  statusMessage=Column(String)
  altitude=Column(Float)
  latitude=Column(Float)
  longitude=Column(Float)
  radioRange=Column(Float)
  mappedInstanceId=Column(String)
  name=Column(String)
  networkSliceId=Column(String)
  ranEndPointId=Column(String)
  status=Column(String)
  tenantId=Column(String)
  vsdId=Column(String)
  nestedParentId = Column(String, ForeignKey('verticalServiceInstance.vsiId'))
  nestedVsi=relationship("VerticalServiceInstance", remote_side=[vsiId])
    # parentVsi = relationship(
    #       "VerticalService",
    #       secondary=nestedVsiTable,
    #       back_populates="nestedVsi")
  nssis=relationship("NetworkSliceSubnetInstance", back_populates="vertical_service_instance")
  vssis=relationship("VerticalSubserviceInstance", back_populates="vertical_service_instance")
  domainPlacements=relationship("DomainPlacements", back_populates="vertical_service_instance")
  additionalConf=relationship("ComponentConfigs", back_populates="vertical_service_instance")

class ComponentConfigs(Base):
  __tablename__ = 'componentConfigs'
  domainPlacementId = Column(Integer, primary_key=True)
  vertical_service_instance_id = Column(String, ForeignKey('verticalServiceInstance.vsiId'))
  vertical_service_instance = relationship("VerticalServiceInstance", back_populates="additionalConf")
  componentName=Column(String)
  conf=Column(String)

class DomainPlacements(Base):
  __tablename__ = 'domainPlacement'
  domainPlacementId = Column(Integer, primary_key=True)
  vertical_service_instance_id = Column(String, ForeignKey('verticalServiceInstance.vsiId'))
  vertical_service_instance = relationship("VerticalServiceInstance", back_populates="domainPlacements")
  componentName=Column(String)
  domainId=Column(String)

class NetworkSliceSubnetInstance(Base):
  __tablename__ = 'networkSliceSubnetInstance'
  nssiId = Column(Integer, primary_key=True)
  domain_id=Column(String)
  ns_deployment_flavor_id=Column(String)
  ns_instantiation_level_id=Column(String)
  nsst_id=Column(String)
  status=Column(Integer)
  vertical_service_instance_id = Column(String, ForeignKey('verticalServiceInstance.vsiId'))
  vertical_service_instance = relationship("VerticalServiceInstance", back_populates="nssis") 
  vnfs = relationship("NetworkSliceSubnetInstanceVnfPlacement", back_populates="network_slice_subnet_instance")
  network_slice_instance_id = Column(Integer, ForeignKey('networkSliceInstance.nsiId'))
  network_slice_instance = relationship("NetworkSliceInstance", back_populates="subnets")

class NetworkSliceSubnetInstanceVnfPlacement(Base):
  __tablename__ = 'networkSliceSubnetInstanceVnfPlacement'
  network_slice_subnet_instance_id = Column(Integer, ForeignKey('networkSliceSubnetInstance.nssiId'), primary_key=True)
  network_slice_subnet_instance = relationship("NetworkSliceSubnetInstance", back_populates="vnfs")
  vnf_placement_key=Column(Integer, primary_key=True)
  vnf_placement=Column(Integer)

class VerticalSubserviceInstance(Base):
  __tablename__ = 'verticalSubserviceInstance'
  vssiId = Column(Integer, primary_key=True)
  blueprint_id=Column(String)
  descriptor_id=Column(String)
  domain_id=Column(String)
  instance_id=Column(String)
  vertical_service_status=Column(Integer)
  vertical_service_instance_id = Column(String, ForeignKey('verticalServiceInstance.vsiId'))
  vertical_service_instance = relationship("VerticalServiceInstance", back_populates="vssis")
  parameters=relationship("VerticalSubserviceInstanceParameters", back_populates="vertical_subservice_instance")

class VerticalSubserviceInstanceParameters(Base):
  __tablename__ = 'verticalSubserviceInstanceParameters'
  vertical_subservice_instance_id = Column(Integer, ForeignKey('verticalSubserviceInstance.vssiId'), primary_key=True)
  vertical_subservice_instance = relationship("VerticalSubserviceInstance", back_populates="parameters")
  parameters_key=Column(Integer, primary_key=True)
  parameters=Column(String)

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
  status = Column(String)
  errorMessage = Column(String)
  nfvNsUrl = Column(String)
  subnets=relationship("NetworkSliceSubnetInstance", back_populates="network_slice_instance")
  vnfs = relationship("NetworkSliceInstanceVnfPlacement", back_populates="network_slice_instance")

class NetworkSliceInstanceVnfPlacement(Base):
  __tablename__ = 'netwokSliceInstanceVnfPlacement'
  network_slice_instance_id = Column(Integer, ForeignKey('networkSliceInstance.nsiId'), primary_key=True)
  network_slice_instance = relationship("NetworkSliceInstance", back_populates="vnfs")
  vnf_placement_key=Column(Integer, primary_key=True)
  vnf_placement=Column(Integer)
