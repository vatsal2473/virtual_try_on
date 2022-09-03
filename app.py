from email.mime import base
import io
from unicodedata import category
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import urllib.request
import os
import base64
from werkzeug.utils import secure_filename
import shutil
from models.hrviton import test_generator
from models.clothsegment import infer
from fileinput import filename
import shutil
import os, glob
from PIL import Image
import cv2
import json
from json import JSONEncoder
import numpy
from image_quality_assessment import image_quality
from clean_directories import clean_my_data, clean_static, clean_output


app = Flask(__name__)
#CORS(app, support_credentials=True)
    
UPLOAD_FOLDER = 'static/uploads/'
 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
 
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
def predict(filename, category):

    #human_model = ['00094_00.jpg', '00135_00.jpg', '00260_00.jpg', '00484_00.jpg', '00494_00.jpg', '00684_00.jpg', '00814_00.jpg', '01985_00.jpg']
    full_length = os.listdir('Length/full')
    half_length = os.listdir('Length/half')
    middle_length = os.listdir('Length/middle')
    sleeveless_length = os.listdir('Length/sleveless')

    human_model = []

    if category == 'full':
        human_model = full_length
    elif category == 'half':
        human_model = half_length
    elif category == 'middle':
        human_model = middle_length
    elif category == 'sleeveless':
        human_model = sleeveless_length


    '''
    print(human_model)
    print(filename)
    infer.main()
    
    images_list = os.listdir('static/inputs_cloth_mask')
    for image in images_list:
        image_path = 'static/inputs_cloth_mask/' + image
        image_save_path = 'static/inputs_cloth_mask_modified/' + image.split('.')[0] + '.jpg'
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size
        print(width, height)
        for i in range(0, width):  					  
            for j in range(0, height):  				  
                data = img.getpixel((i, j))  				  
                if (data[0] >= 64):
                    img.putpixel((i, j), (255, 255, 255))
        img = img.convert('L')
        img.save(image_save_path)  	
    '''

    clean_my_data()

    '''
    src = 'static/uploads/' + filename
    dst = 'models/hrviton/my_data/test/cloth/' + filename
    shutil.copyfile(src, dst)

    src = 'static/inputs_cloth_mask_modified/' + filename
    dst = 'models/hrviton/my_data/test/cloth-mask/' + filename
    shutil.copyfile(src, dst)

    '''

    for i in range(len(human_model)):
        src = 'models/hrviton/data/zalando-hd-resized/test/image/' + human_model[i]
        dst = 'models/hrviton/my_data/test/image/' + human_model[i]
        shutil.copyfile(src, dst)

        src = 'models/hrviton/data/zalando-hd-resized/test/image-densepose/' + human_model[i]
        dst = 'models/hrviton/my_data/test/image-densepose/' + human_model[i]
        shutil.copyfile(src, dst)

        src = 'models/hrviton/data/zalando-hd-resized/test/image-parse-agnostic-v3.2/' + human_model[i].replace("jpg", "png")
        dst = 'models/hrviton/my_data/test/image-parse-agnostic-v3.2/' + human_model[i].replace("jpg", "png")
        shutil.copyfile(src, dst)

        src = 'models/hrviton/data/zalando-hd-resized/test/image-parse-v3/' + human_model[i].replace("jpg", "png")
        dst = 'models/hrviton/my_data/test/image-parse-v3/' + human_model[i].replace("jpg", "png")
        shutil.copyfile(src, dst)    

        src = 'models/hrviton/data/zalando-hd-resized/test/openpose_img/' + (human_model[i][0:8]+"_rendered"+human_model[i][8:]).replace("jpg","png")
        dst = 'models/hrviton/my_data/test/openpose_img/' + (human_model[i][0:8]+"_rendered"+human_model[i][8:]).replace("jpg","png")
        shutil.copyfile(src, dst)

        src = 'models/hrviton/data/zalando-hd-resized/test/openpose_json/' + (human_model[i][0:8]+"_keypoints"+human_model[i][8:]).replace("jpg","json")
        dst = 'models/hrviton/my_data/test/openpose_json/' + (human_model[i][0:8]+"_keypoints"+human_model[i][8:]).replace("jpg","json")
        shutil.copyfile(src, dst)

    
    with open('models/hrviton/my_data/test_pairs.txt', 'w') as f:
        for i in range(len(human_model)):
            f.write(human_model[i]+" "+filename)
            f.write("\n")

    #test_generator.main()


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


@app.route("/")
def template_test():
    return render_template('index.html')


@app.route('/file-upload', methods=['POST'])
#@cross_origin(supports_credentials=True)
def upload_image():

    clean_static()
    clean_output()
    
    category  = request.form.get('human_model', type=str, default='')
    cloth_file=request.form.get('file',type = str, default='')

    new_string = cloth_file.split(',')[1]

    my_str_as_bytes = str.encode(new_string)
    with open("static/uploads/image.jpg", "wb") as fh:
        fh.write(base64.decodebytes(my_str_as_bytes))

    for i in os.listdir('static/uploads/'):
        print(i)
        im = cv2.imread('static/uploads/'+i)
        print(im.shape)
        im = cv2.resize(im,(768,1024))
        print(im.shape)
        cv2.imwrite('static/uploads/'+i.split('.')[0]+'.jpg',im)

    predict('image.jpg', category)

    #need best output value of img
    img_dict = image_quality()

    img = list(img_dict.values())[0]
    file_path = 'output/test/test/unpaired/generator/output/' + img
    encoded_img = get_response_image(file_path)

    response = jsonify({'output': encoded_img})
    return (response)

    '''
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 401
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    else:
        resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = 201
        return resp
    '''


 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
