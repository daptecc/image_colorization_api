from flask import Blueprint, current_app, jsonify, request, render_template
from flask_restful import Api
from marshmallow import ValidationError
from image_colorization_api.extensions import apispec
from image_colorization_api.api.resources import ImageColorizerResource
from image_colorization_api.predict import make_prediction
from PIL import Image
import io
import base64
import numpy as np

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)
api.add_resource(ImageColorizerResource, "/image_colorizer", endpoint="color_image")

simple_page = Blueprint('simple_page', __name__, template_folder='templates')

@simple_page.route('/')
def index_view():
    return render_template('index.html')

@simple_page.route('/colorize', methods=['POST'])
def colorize():
    data = request.files['file']
    
    img = Image.open(data.stream)
    w,h = img.size
    img = img.resize((600, int(600 * h / w)))
    img = pil_to_base64(img)
    
    img_color = make_prediction(data.stream)
    img_color = Image.fromarray((img_color * 255).astype(np.uint8))
    img_color = img_color.resize((600, int(600 * h / w)))
    img_color = pil_to_base64(img_color)
    
    return render_template('result.html',
                           data_orig=img,
                           data_color=img_color,
                           mimetype='image/png')

def pil_to_base64(pil_img):
	file_obj = io.BytesIO()
	pil_img.save(file_obj, 'png')
	file_obj.seek(0)
	base64_img = "data:image/png;base64,"+base64.b64encode(file_obj.getvalue()).decode('ascii')
	return base64_img
                     
# @blueprint.before_app_first_request
# def register_views():
#     apispec.spec.path(view=ImageColorizerResource, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
