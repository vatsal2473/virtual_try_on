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
from image_quality_assessment import image_enchancer, image_quality
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
    full_length = ['02017_00.jpg', '00858_00.jpg', '02299_00.jpg', '08232_00.jpg',
       '06919_00.jpg', '02152_00.jpg', '02404_00.jpg', '03033_00.jpg',
       '01410_00.jpg', '01609_00.jpg', '00889_00.jpg', '11841_00.jpg',
       '12460_00.jpg', '00821_00.jpg', '04392_00.jpg', '01641_00.jpg',
       '01008_00.jpg', '02870_00.jpg', '02666_00.jpg', '01796_00.jpg',
       '11659_00.jpg', '00460_00.jpg', '09685_00.jpg', '00112_00.jpg',
       '08278_00.jpg', '03615_00.jpg', '07212_00.jpg', '00740_00.jpg',
       '11078_00.jpg', '01963_00.jpg', '11626_00.jpg', '00782_00.jpg',
       '02424_00.jpg', '07706_00.jpg', '00084_00.jpg', '08199_00.jpg']
    half_length = ['01630_00.jpg', '09199_00.jpg', '00286_00.jpg', '00891_00.jpg',
       '00345_00.jpg', '04313_00.jpg', '13331_00.jpg', '08186_00.jpg',
       '11401_00.jpg', '08322_00.jpg', '08376_00.jpg', '01713_00.jpg',
       '10294_00.jpg', '05898_00.jpg', '08183_00.jpg', '00190_00.jpg',
       '00055_00.jpg', '02887_00.jpg', '10709_00.jpg', '12345_00.jpg',
       '06161_00.jpg', '04130_00.jpg', '01051_00.jpg', '11528_00.jpg',
       '02759_00.jpg', '01944_00.jpg', '09541_00.jpg', '01229_00.jpg',
       '00852_00.jpg', '00579_00.jpg', '12030_00.jpg', '05235_00.jpg',
       '01449_00.jpg', '08538_00.jpg', '07036_00.jpg', '01198_00.jpg',
       '13770_00.jpg', '13642_00.jpg', '06360_00.jpg', '10687_00.jpg',
       '00499_00.jpg', '02244_00.jpg', '10680_00.jpg', '00440_00.jpg',
       '11707_00.jpg', '11836_00.jpg', '01565_00.jpg', '02457_00.jpg',
       '09867_00.jpg', '09097_00.jpg', '12534_00.jpg', '07703_00.jpg',
       '02941_00.jpg', '02180_00.jpg', '01000_00.jpg', '01463_00.jpg',
       '02534_00.jpg', '10448_00.jpg', '03250_00.jpg', '02765_00.jpg',
       '05588_00.jpg', '01382_00.jpg', '04818_00.jpg', '08429_00.jpg',
       '00121_00.jpg', '11330_00.jpg', '00802_00.jpg', '01035_00.jpg',
       '02530_00.jpg', '04743_00.jpg']
    middle_length = ['08673_00.jpg', '01320_00.jpg', '08989_00.jpg', '06647_00.jpg',
       '08981_00.jpg', '03884_00.jpg', '10706_00.jpg', '12451_00.jpg',
       '01470_00.jpg', '11028_00.jpg', '10090_00.jpg', '00592_00.jpg',
       '05400_00.jpg', '02824_00.jpg', '00865_00.jpg', '04041_00.jpg']
    sleeveless_length = ['02270_00.jpg', '06241_00.jpg', '03052_00.jpg', '02039_00.jpg',
       '08321_00.jpg', '03061_00.jpg', '02007_00.jpg', '09026_00.jpg',
       '04240_00.jpg', '10324_00.jpg', '10549_00.jpg', '04661_00.jpg',
       '02768_00.jpg', '06173_00.jpg', '10931_00.jpg', '00986_00.jpg',
       '09069_00.jpg', '02184_00.jpg', '12807_00.jpg', '03922_00.jpg',
       '04700_00.jpg', '08481_00.jpg', '03374_00.jpg', '10343_00.jpg',
       '02364_00.jpg']

#    human_model = []

    if category == 'full':
        human_model = full_length
    elif category == 'half':
        human_model = half_length
    elif category == 'middle':
        human_model = middle_length
    elif category == 'sleeveless':
        human_model = sleeveless_length


    
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
    

    clean_my_data()

    
    src = 'static/uploads/' + filename
    dst = 'models/hrviton/my_data/test/cloth/' + filename
    shutil.copyfile(src, dst)

    src = 'static/inputs_cloth_mask_modified/' + filename
    dst = 'models/hrviton/my_data/test/cloth-mask/' + filename
    shutil.copyfile(src, dst)

    

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

    test_generator.main()


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
    print("done1")
    img_dict = image_quality()
    image_enchancer()
    print("done2")

    img = list(img_dict.values())[0]
#    img = '00055_00_image.png'
    file_path = 'output/test/test/unpaired/generator/enhance_output/' + img

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
    app.run()
