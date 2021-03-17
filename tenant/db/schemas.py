from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import db.persistance as persistance


class TenantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.Tenant
        include_relationships = True
        load_instance = True


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.Group
        include_fk = True
        load_instance = True

class SlaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.Sla
        include_fk = True
        load_instance = True

class SlaConstraintSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.SlaConstraint
        include_fk = True
        load_instance = True

class VSDSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.VSD
        include_fk = True
        load_instance = True

class VSISchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.VSI
        include_fk = True
        load_instance = True