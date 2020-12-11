from flask import Flask

#from image_colorization_api import auth, api
from image_colorization_api import api
#from image_colorization_api.extensions import db, jwt, migrate, apispec
from image_colorization_api.extensions import apispec

import sys
import os

from image_colorization_api.image_colorization import main_model
import pickle

submodule_path = f'{os.path.dirname(__file__)}/image_colorization'
sys.path.append(submodule_path)
sys.modules['main_model'] = main_model
SERIALIZED_MODEL_PATH = f'{submodule_path}/weights/colorization_model.pkl'
global model
model = pickle.load(open(SERIALIZED_MODEL_PATH, 'rb'))
print(model)

def create_app(testing=False, cli=False):
    """Application factory, used to create application"""
    app = Flask("image_colorization_api")
    app.config.from_object("image_colorization_api.config")
    
    if testing is True:
        app.config["TESTING"] = True

    #configure_extensions(app, cli)
    #configure_apispec(app)
    register_blueprints(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application"""
    #app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
