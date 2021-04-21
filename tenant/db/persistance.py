from sqlalchemy import Table, Column, Integer, Float, String, Boolean, ForeignKey, create_engine, inspect, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
from datetime import timedelta, datetime
from hashlib import blake2b
import config
from flask_login import UserMixin
import logging

Base = declarative_base()

class Group(Base):
    __tablename__ = 'Group'
    name = Column(String, primary_key=True)
    tenants=relationship("Tenant", back_populates="group")

class Sla(Base):
    __tablename__ = 'Sla'
    id = Column(Integer, primary_key=True)
    enabled=Column(Boolean)
    tenantUsername=Column(String, ForeignKey('Tenant.username'),nullable=False)
    tenant=relationship("Tenant", back_populates="slas")
    constraints= relationship("SlaConstraint", back_populates="sla")

class SlaConstraint(Base):
    __tablename__ = 'SlaConstraint'
    id = Column(Integer, primary_key=True)
    storage = Column(Integer)
    memory = Column(Integer)
    vcpu = Column(Integer)
    scope = Column(Integer)
    location = Column(String)
    slaId = Column(Integer, ForeignKey('Sla.id'),nullable=False)
    sla = relationship("Sla", back_populates="constraints")

class VSD(Base):
    __tablename__ = 'VSD'
    id = Column(Integer, primary_key=True)
    tenantUsername=Column(String, ForeignKey('Tenant.username'), primary_key=True)
    tenant=relationship("Tenant", back_populates="vsds")

class VSI(Base):
    __tablename__ = 'VSI'
    id = Column(Integer, primary_key=True)
    tenantUsername=Column(String, ForeignKey('Tenant.username'), primary_key=True)
    tenant=relationship("Tenant", back_populates="vsis")

class Tenant(Base, UserMixin):
    __tablename__ = 'Tenant'
    username = Column(String, primary_key=True)
    password = Column(String)
    role = Column(String)
    storage = Column(Integer)
    memory = Column(Integer)
    vcpu = Column(Integer)
    groupName = Column(String, ForeignKey('Group.name'))
    group = relationship("Group", back_populates="tenants")
    vsds=relationship("VSD", back_populates="tenant")
    vsis=relationship("VSI", back_populates="tenant")
    slas=relationship("Sla", back_populates="tenant")

    def get_id(self):
        return self.username

    def check_password(self, password):
        hashedPass=blake2b(password.encode("utf-8")).hexdigest()
        return hashedPass==self.password

    # def getTenant(self):
    #     return {"username":self.username}

    # def __str__(self):
    #     return json.dumps({"username":self.username})


class OauthClient(Base):
    # id = db.Column(db.Integer, primary_key=True)
    # human readable name
    __tablename__ = 'OauthClient'
    name = Column(String)
    client_id = Column(String, primary_key=True)
    client_secret = Column(String, unique=True, index=True,
                              nullable=False)
    client_type = Column(String, default='public')
    _redirect_uris = Column(Text)
    default_scope = Column(Text, default='email address')

    @property
    def user(self):
        return session.query(Tenant).first()

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split(" ")
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scope:
            return self.default_scope.split(" ")
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials',
                'refresh_token']


class OauthGrant(Base):
    __tablename__ = 'Grant'
    id = Column(Integer, primary_key=True)
    user_id = Column(
        String, ForeignKey('Tenant.username', ondelete='CASCADE')
    )
    user = relationship('Tenant')

    client_id = Column(
        String, ForeignKey('OauthClient.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    client = relationship('OauthClient')
    code = Column(String, index=True, nullable=False)

    redirect_uri = Column(String)
    scope = Column(Text)
    expires = Column(DateTime)

    def delete(self):
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return None


class OauthToken(Base):
    __tablename__ = 'Token'
    id = Column(Integer, primary_key=True)
    client_id = Column(
        String, ForeignKey('OauthClient.client_id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id = Column(
        String, ForeignKey('Tenant.username', ondelete='CASCADE')
    )
    user = relationship('Tenant')
    client = relationship('OauthClient')
    token_type = Column(String(40))
    access_token = Column(String(255))
    refresh_token = Column(String(255))
    expires = Column(DateTime)
    scope = Column(Text)

    def __init__(self, **kwargs):
        expires_in = kwargs.pop('expires_in', None)
        if expires_in is not None:
            self.expires = datetime.utcnow() + timedelta(seconds=expires_in)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def delete(self):
        session.delete(self)
        session.commit()
        return self

    @property
    def scopes(self):
        if self.scope:
            return self.scope.split()
        return []



def persist(entity):
  session.add(entity)
  session.commit()

def delete(entity):
  session.delete(entity)
  session.commit()


def initDB():
    portal = OauthClient(
        name='portal', client_id='portal',
        client_secret='portal', client_type='confidential',
        _redirect_uris=('http://127.0.0.1/authorized'),
    )
    
    adminPassword=blake2b('admin'.encode("utf-8")).hexdigest()
    userPassword=blake2b('user'.encode("utf-8")).hexdigest()
    adminGroup=Group(name="admin")
    userGroup=Group(name="user")
    admin = Tenant(username='admin', role='ADMIN', storage=100, memory=100, vcpu=100, group=adminGroup, password=adminPassword)
    user = Tenant(username='user', role='TENANT', storage=100, memory=100, vcpu=100, group=userGroup, password=userPassword)

    try:
        session.add(adminGroup)
        session.add(userGroup)
        session.add(portal)
        session.add(admin)
        session.add(user)
        session.commit()
        logging.info("Successfully initiated database")
    except Exception as e:
        session.rollback()
        logging.info("Error while initializing database: "+str(e))

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
initDB()