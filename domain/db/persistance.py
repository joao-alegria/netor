from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, create_engine, inspect
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

associationTable=Table('domainOwnedLayers', Base.metadata, Column('domainId', String, ForeignKey('domain.domainId')),Column('domainLayerId', String, ForeignKey('domainLayer.domainLayerId')))

class Domain(Base):
    __tablename__ = 'domain'
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
    __tablename__ = 'domainLayer'
    domainLayerId = Column(String, primary_key=True)
    domainLayerType=Column(String)
    domains=relationship("Domain", secondary=associationTable, back_populates="ownedLayers")
    __mapper_args__ = {
        'polymorphic_identity':'domainLayer',
        'polymorphic_on':domainLayerType
    }

class OsmDomainLayer(DomainLayer):
    __tablename__ = 'osmDomainLayer'
    domainLayerId = Column(String, ForeignKey('domainLayer.domainLayerId'), primary_key=True)
    username=Column(String)
    password=Column(String)
    project=Column(String)
    vimAccount=Column(Integer)
    ranEnabled=Column(Boolean)
    __mapper_args__ = {
        'polymorphic_identity':'osmDomainLayer',
    }

engine = create_engine('postgresql://postgres:postgres@localhost/vsDomain', echo=True)
if not database_exists(engine.url):
  create_database(engine.url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()

def persist(entity):
  session.add(entity)
  session.commit()

def delete(entity):
  session.delete(entity)
  session.commit()