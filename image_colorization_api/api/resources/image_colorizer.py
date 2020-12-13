from flask_restful import Resource
from flask import jsonify, request, send_file
import numpy as np
from PIL import Image
import io
from image_colorization_api.predict import make_prediction

class ImageColorizerResource(Resource):
    """
    
    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  status: str
        404:
          description: failed
    post:
      tags:
        - api
      requestBody:
        content:
          multipart/form-data
      responses:
        200:
          content:
            image/PNG
        404:
          error message
    """
    def get(self):
        return jsonify({"status": "ok"})
    
    def post(self):
        '''
        '''
        
        data = request.files['file']
        img = Image.open(data.stream)
        w,h = img.size
    
        img_color = make_prediction(data.stream)
        img_color = Image.fromarray((img_color * 255).astype(np.uint8))
        img_color = img_color.resize((600, int(600 * h / w)))
        file_obj = io.BytesIO()
        img_color.save(file_obj, 'png')
        file_obj.seek(0)
        return send_file(file_obj,  mimetype='image/PNG')
