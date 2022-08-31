from PIL import Image
from numpy import asarray
import os
import cv2
import numpy as np

def MSE(img1, img2):
  squared_diff = (img1 - img2) ** 2
  summed = np.sum(squared_diff)
  num_pix = img1.shape[0] * img1.shape[1] #img1 and 2 should have same shape
  err = summed / num_pix
  return err

def image_quality():
    warped_clothmask = os.listdir('output/test/test/unpaired/generator/warped_clothmask')
    output = os.listdir('output/test/test/unpaired/generator/output')
    for k in range(len(warped_clothmask)):
        img1 = Image.open('output/test/test/unpaired/generator/warped_clothmask/' + warped_clothmask[k])
        img2 = Image.open('output/test/test/unpaired/generator/output/' + output[k])
        numpydata1 = asarray(img1)
        arr1 = np.array(numpydata1)
        numpydata2 = asarray(img2)
        arr2 = np.array(numpydata2)
        #print(numpydata.shape)
        for i in range(1024):
            for j in range(768):
                if numpydata1[i][j][0]==0 and numpydata1[i][j][1]==0 and numpydata1[i][j][2]==0:
                    arr1[i][j][0] = 255
                    arr1[i][j][1] = 255
                    arr1[i][j][2] = 255
                elif numpydata1[i][j][0]==255 and numpydata1[i][j][1]==255 and numpydata1[i][j][2]==255:
                    arr1[i][j][0] = arr2[i][j][0]
                    arr1[i][j][1] = arr2[i][j][1]
                    arr1[i][j][2] = arr2[i][j][2]
        img = Image.fromarray(arr1)
        img.save('output/test/test/unpaired/generator/model_cloth_segment/' + warped_clothmask[k])

    names = os.listdir('output/test/test/unpaired/generator/cloth_segment')
    err = {}
    for i in range(len(os.listdir('output/test/test/unpaired/generator/cloth_segment'))):
        img1 = cv2.imread("output/test/test/unpaired/generator/cloth_segment/" + names[i])
        img2 = cv2.imread("output/test/test/unpaired/generator/model_cloth_segment/" + names[i])
        err[MSE(img1, img2)] = names[i]

    sorted_err = {}
    for i in sorted(err):
        sorted_err[i] = err[i]
        #print((i, err[i]))
    print(sorted_err)
    return sorted_err
