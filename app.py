from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import shutil
from models.hrviton import test_generator
from models.clothsegment import infer


from fileinput import filename
import shutil
import os, glob
from PIL import Image, ImageChops


app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "vatsal"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
def predict(filename):

    human_model = '00013_00.jpg'

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



    dir = 'models/hrviton/my_data/test/agnostic-v3.2'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/cloth'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/cloth-mask'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/image'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/image-densepose'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/image-parse-agnostic-v3.2'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/image-parse-v3'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/openpose_img'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'models/hrviton/my_data/test/openpose_json'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    #filename = '00008_00.jpg'
    #human_model = '00013_00.jpg'

    src = 'static/uploads/' + filename
    dst = 'models/hrviton/my_data/test/cloth/' + filename
    shutil.copyfile(src, dst)

    src = 'static/inputs_cloth_mask_modified/' + filename
    dst = 'models/hrviton/my_data/test/cloth-mask/' + filename
    shutil.copyfile(src, dst)

    src = 'models/hrviton/data/zalando-hd-resized/test/image/' + human_model
    dst = 'models/hrviton/my_data/test/image/' + human_model
    shutil.copyfile(src, dst)

    src = 'models/hrviton/data/zalando-hd-resized/test/image-densepose/' + human_model
    dst = 'models/hrviton/my_data/test/image-densepose/' + human_model
    shutil.copyfile(src, dst)

    src = 'models/hrviton/data/zalando-hd-resized/test/image-parse-agnostic-v3.2/' + human_model.replace("jpg", "png")
    dst = 'models/hrviton/my_data/test/image-parse-agnostic-v3.2/' + human_model.replace("jpg", "png")
    shutil.copyfile(src, dst)

    src = 'models/hrviton/data/zalando-hd-resized/test/image-parse-v3/' + human_model.replace("jpg", "png")
    dst = 'models/hrviton/my_data/test/image-parse-v3/' + human_model.replace("jpg", "png")
    shutil.copyfile(src, dst)    

    src = 'models/hrviton/data/zalando-hd-resized/test/openpose_img/' + (human_model[0:8]+"_rendered"+human_model[8:]).replace("jpg","png")
    dst = 'models/hrviton/my_data/test/openpose_img/' + (human_model[0:8]+"_rendered"+human_model[8:]).replace("jpg","png")
    shutil.copyfile(src, dst)

    src = 'models/hrviton/data/zalando-hd-resized/test/openpose_json/' + (human_model[0:8]+"_keypoints"+human_model[8:]).replace("jpg","json")
    dst = 'models/hrviton/my_data/test/openpose_json/' + (human_model[0:8]+"_keypoints"+human_model[8:]).replace("jpg","json")
    shutil.copyfile(src, dst)


    with open('models/hrviton/my_data/test_pairs.txt', 'w') as f:
        f.write(human_model+" "+filename)

    test_generator.main()
    #final output here
    #output/test/unpaired/generator/output



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():

    dir = 'static/uploads'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'static/inputs_cloth_mask'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'static/inputs_cloth_mask_modified'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)


    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        #flash('Image successfully uploaded and displayed below')
        predict(filename)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static' ,filename='inputs_cloth_mask_modified/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()