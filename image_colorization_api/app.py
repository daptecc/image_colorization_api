from flask import Flask

from image_colorization_api import api
from image_colorization_api.extensions import apispec

import sys
import os

from image_colorization_api.image_colorization import main_model
import pickle

model = None
def create_app(testing=False, cli=False):
    """Application factory, used to create application"""
    app = Flask("image_colorization_api")
    app.config.from_object("image_colorization_api.config")
    load_model()
    
    if testing is True:
        app.config["TESTING"] = True

    configure_apispec(app)
    register_blueprints(app)

    return app

def load_model():
    global model
    app_path = f'{sys.path[-1]}/image_colorization_api'
    submodule_path = f'{app_path}/image_colorization'
    sys.path.append(app_path)
    sys.path.append(submodule_path)
    sys.modules['main_model'] = main_model
    SERIALIZED_MODEL_PATH = f'{submodule_path}/weights/colorization_model.pkl'
    model = pickle.load(open(SERIALIZED_MODEL_PATH, 'rb'))
    
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
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(api.views.simple_page)
    