from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import db.persistance as persistance

class VerticalServiceInstanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.VerticalServiceInstance
        include_relationships = True
        load_instance = True

class NetworkSliceSubnetInstanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.NetworkSliceSubnetInstance
        include_relationships = True
        load_instance = True

class NetworkSliceSubnetInstanceVnfPlacementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.NetworkSliceSubnetInstanceVnfPlacement
        include_relationships = True
        load_instance = True
        
class VerticalSubserviceInstanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.VerticalSubserviceInstance
        include_relationships = True
        load_instance = True

class VerticalSubserviceInstanceParametersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.VerticalSubserviceInstanceParameters
        include_relationships = True
        load_instance = True

class NetworkSliceInstanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.NetworkSliceInstance
        include_relationships = True
        load_instance = True

class NetworkSliceInstanceVnfPlacementSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = persistance.NetworkSliceInstanceVnfPlacement
        include_relationships = True
        load_instance = True