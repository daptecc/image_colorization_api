from flask_restful import Resource
from flask import jsonify, request
from PIL import Image
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
            application/json
              msg: str
              img: numpy array
        404:
          error message
    """
    def get(self):
        return jsonify({"status": "ok"})
    
    def post(self):
        '''
        '''
        
        data = request.files['file']
        img = make_prediction(data.stream)
        
        return jsonify({'msg': 'success', 'img': img.shape})
