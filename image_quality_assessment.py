from fileinput import filename
from time import time
from tkinter import W
from PIL import Image
from numpy import asarray
import os
import cv2
import numpy as np
from wand.image import Image as WandImage

def MSE(img1, img2):
  squared_diff = (img1 - img2) ** 2
  summed = np.sum(squared_diff)
  num_pix = img1.shape[0] * img1.shape[1] #img1 and 2 should have same shape
  err = summed / num_pix
  return err

def image_quality():
    for i in os.listdir('output/test/test/unpaired/generator/warped_clothmask/'):
        im = cv2.imread('output/test/test/unpaired/generator/warped_clothmask/'+i)
        im = cv2.resize(im,(270, 360))
        cv2.imwrite('output/test/test/unpaired/generator/warped_clothmask_resized/'+i.split('.')[0]+'.png',im)
    '''
    # sharpen image
    for i in os.listdir('output/test/test/unpaired/generator/output/'):
        with WandImage(filename="output/test/test/unpaired/generator/output/"+i) as img:
            img.sharpen(8,4)
            img.save(filename="output/test/test/unpaired/generator/output_sharpened/"+i)
    '''

    for i in os.listdir('output/test/test/unpaired/generator/output/'):
        im = cv2.imread('output/test/test/unpaired/generator/output/'+i)
        im = cv2.resize(im, (270, 360))
        cv2.imwrite('output/test/test/unpaired/generator/output_resized/'+i.split('.')[0]+'.png',im)

    for i in os.listdir('output/test/test/unpaired/generator/cloth_segment/'):
        im = cv2.imread('output/test/test/unpaired/generator/cloth_segment/'+i)
        im = cv2.resize(im, (270, 360))
        cv2.imwrite('output/test/test/unpaired/generator/cloth_segment_resized/'+i.split('.')[0]+'.png',im)

    warped_clothmask = os.listdir('output/test/test/unpaired/generator/warped_clothmask_resized')
    output = os.listdir('output/test/test/unpaired/generator/output_resized')
    for k in range(len(warped_clothmask)):
        img1 = Image.open('output/test/test/unpaired/generator/warped_clothmask_resized/' + warped_clothmask[k])
        img2 = Image.open('output/test/test/unpaired/generator/output_resized/' + output[k])
        numpydata1 = asarray(img1)
        arr1 = np.array(numpydata1)
        numpydata2 = asarray(img2)
        arr2 = np.array(numpydata2)
        #print(numpydata.shape)
        for i in range(360):
            for j in range(270):
                if numpydata1[i][j][0]==255 and numpydata1[i][j][1]==255 and numpydata1[i][j][2]==255:
                    arr1[i][j][0] = arr2[i][j][0]
                    arr1[i][j][1] = arr2[i][j][1]
                    arr1[i][j][2] = arr2[i][j][2]
                else:
                    arr1[i][j][0] = 255
                    arr1[i][j][1] = 255
                    arr1[i][j][2] = 255
        img = Image.fromarray(arr1)
        img.save('output/test/test/unpaired/generator/model_cloth_segment_resized/' + warped_clothmask[k])

    names = os.listdir('output/test/test/unpaired/generator/cloth_segment')
    err = {}
    for i in range(len(os.listdir('output/test/test/unpaired/generator/cloth_segment_resized'))):
        img1 = cv2.imread("output/test/test/unpaired/generator/cloth_segment_resized/" + names[i])
        img2 = cv2.imread("output/test/test/unpaired/generator/model_cloth_segment_resized/" + names[i])
        err[MSE(img1, img2)] = names[i]
    '''
    blur = {}
    for i in range(len(os.listdir('output/test/test/unpaired/generator/model_cloth_segment_resized'))):
        img = cv2.imread("output/test/test/unpaired/generator/model_cloth_segment_resized/" + names[i])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        value = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur[value] = names[i]
    '''
    sorted_err = {}
    for i in sorted(err):
        sorted_err[i] = err[i]
    print(sorted_err)
    '''
    sorted_blur = {}
    for i in sorted(blur):
        sorted_blur[i] = blur[i]
    print(sorted_blur)
    '''
    return sorted_err

#image_quality()