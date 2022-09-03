import os, glob


def clean_static():
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



def clean_output():
    dir = 'output/test/test/unpaired/generator/cloth_segment'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/cloth_segment_resized'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/model_cloth_segment_resized'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/output'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/output_resized'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/output_sharpened'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/warped_clothmask'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)

    dir = 'output/test/test/unpaired/generator/warped_clothmask_resized'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        os.remove(f)


def clean_my_data():
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