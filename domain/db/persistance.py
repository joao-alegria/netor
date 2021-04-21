import config
from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, create_engine, inspect
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

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
    domainStatus=Column(Integer)
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
        'polymorphic_identity':'OsmDomainLayer',
    }

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

def initDB():
  domain=session.query(Domain).filter(Domain.domainId=="ITAV").first()
  if domain==None:
    domain=Domain(domainId="ITAV",admin="ITAV",description="test domain",auth=False,interfaceType="HTTP",url="10.0.12.118",name="ITAV",owner="joao")

    domainLayer=OsmDomainLayer(domainLayerId="OSM",domainLayerType="OsmDomainLayer",username="admin", password="admin", project="admin", vimAccount="microstack")
    domainLayer.domains.append(domain)

    persist(domain)
    persist(domainLayer)