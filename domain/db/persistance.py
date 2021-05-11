import config
from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, create_engine, inspect
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

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

  def initDB(self):
    domain=self.session.query(Domain).filter(Domain.domainId=="ITAV").first()
    if domain==None:
      domain=Domain(domainId="ITAV",admin="ITAV",description="test domain",auth=False,interfaceType="HTTP",url="10.0.12.118",name="ITAV",owner="joao")

      domainLayer=OsmDomainLayer(domainLayerId="OSM",domainLayerType="OSM_NSP",username="admin", password="admin", project="admin", vimAccount="microstack")
      domainLayer.domains.append(domain)

      self.persist(domain)
      self.persist(domainLayer)

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
        self.Base.metadata.create_all(self.engine)
    Session = sessionmaker(bind=self.engine)
    self.session=Session()


  def removeDB(self):
      self.Base.metadata.drop_all(self.engine)
      self.session.close()

Base = declarative_base()
DB=DB(Base)

associationTable=Table('DomainOwnedLayers', Base.metadata, Column('domainId', String, ForeignKey('Domain.domainId')),Column('domainLayerId', String, ForeignKey('DomainLayer.domainLayerId')))

class Domain(Base):
    __tablename__ = 'Domain'
    domainId = Column(String, primary_key=True)

    admin=Column(String)
    description=Column(String)
    auth=Column(Boolean)
    interfaceType=Column(String)
    port=Column(Integer)
    url=Column(String)
    status=Column(String)
    name=Column(String)
    owner=Column(String)
    ownedLayers=relationship("DomainLayer", secondary=associationTable, back_populates="domains")

# class DomainAgreement(Base):
#     __tablename__ = 'domainAgreement'
#     agreementId = Column(Integer, primary_key=True)

class DomainLayer(Base):
    __tablename__ = 'DomainLayer'
    domainLayerId = Column(String, primary_key=True)
    domainLayerType=Column(String)
    domains=relationship("Domain", secondary=associationTable, back_populates="ownedLayers")
    __mapper_args__ = {
        'polymorphic_identity':'DomainLayer',
        'polymorphic_on':domainLayerType
    }

class OsmDomainLayer(DomainLayer):
    __tablename__ = 'OsmDomainLayer'
    domainLayerId = Column(String, ForeignKey('DomainLayer.domainLayerId'), primary_key=True)
    username=Column(String)
    password=Column(String)
    project=Column(String)
    vimAccount=Column(String)
    ranEnabled=Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity':'OSM_NSP',
    }