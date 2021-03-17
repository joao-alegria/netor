from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import db.persistance as persistance

class DomainSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.Domain
        include_relationships = True
        load_instance = True

class DomainLayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.DomainLayer
        include_relationships = True
        load_instance = True

class OsmDomainLayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.OsmDomainLayer
        include_relationships = True
        load_instance = True