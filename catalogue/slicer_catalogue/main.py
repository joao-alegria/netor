import os
import importlib, inspect
import api.models
from flask import Flask
from api.views.vs_blueprint import app as vs_blueprint_api
from api.views.vs_descriptor import app as vs_descriptor_api
from api.settings import ProdConfig
from mongoengine import Document, DynamicDocument
from flask_mongoengine import MongoEngine
from rabbitmq.messaging import MessageReceiver
from api.auth import loginManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
   

APPLICATION_NAME = os.environ.get('APPLICATION_NAME', 'catalogues')

class ReverseProxied(object):
    def __init__(self, app, script_name):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.script_name
        return self.app(environ, start_response)






def init_flask():
    app = Flask(APPLICATION_NAME)
    
    app.wsgi_app = ReverseProxied(app.wsgi_app, script_name='/catalogue')
    SWAGGER_URL = '/apidocs'
    # API_URL = 'templates/swagger.json'
    API_URL = '/catalogue/static/documentation.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Catalogue API"
        }
    )
    CORS(app)

    # Configurations settings
    app.config.from_object(ProdConfig)

    # Register flask's blueprints
    app.register_blueprint(vs_blueprint_api)
    app.register_blueprint(vs_descriptor_api)

    #Register SwaggerUI Blueprint
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    

    #  Connect database
    db = MongoEngine()
    db.init_app(app)

    @app.before_first_request
    def before_first_request():
        # Create all collection before because of the multi document transcations
        database = db.get_db()
        for model in dir(api.models)[7:]:
            for name, cls in inspect.getmembers(importlib.import_module(f"api.models.{model}"), inspect.isclass):
                if 'api.models' in cls.__module__ and issubclass(cls, (Document, DynamicDocument)):
                    collection_name = cls.get_collection().name
                    if collection_name not in database.list_collection_names(filter={"name": collection_name}):
                        database.create_collection(collection_name)

    # Authentication
    loginManager.init_app(app)

    app.run(host="0.0.0.0", port=ProdConfig.PORT)


def init_rabbit():
    message_receiver = MessageReceiver()
    message_receiver.start()


if __name__ == '__main__':
    init_rabbit()
    init_flask()
