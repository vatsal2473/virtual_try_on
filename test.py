from fileinput import filename
import shutil
import os, glob

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

filename = '00008_00.jpg'
human_model = '00013_00.jpg'

src = 'static/uploads/' + filename
dst = 'models/hrviton/my_data/test/cloth/' + filename
shutil.copyfile(src, dst)

src = 'models/hrviton/data/zalando-hd-resized/test/cloth-mask/' + filename
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

# hinge cost function
def hinge_cost(y_true, y_pred):
    return np .mean(K.mean(K.square(y_pred - y_true), axis=-1))