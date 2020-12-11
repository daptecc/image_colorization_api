from PIL import Image
import torch
from image_colorization_api.image_colorization.utils import PIL_image_to_model_input, lab_to_rgb
from image_colorization_api import app

def make_prediction(datastream):
    '''
    reads image data stream
    resizes image to model input size (256)
    converts to L*a*b* color space
    gets L features
    feeds L input features to colorization model to predict ab features
    reconstructs Lab image from L and ab features
    converts to RGB color space
    returns colorized image
    '''
    
    img = Image.open(datastream)
    data = PIL_image_to_model_input(img)
    
    app.model.net_G.eval()
    with torch.no_grad():
        app.model.setup_input(data)
        app.model.forward()
    
    ab = app.model.fake_color.detach()
    img = lab_to_rgb(data['L'], ab.cpu())
    img = img.squeeze(0)
    return img