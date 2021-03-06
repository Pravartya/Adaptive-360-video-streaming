# -*- coding: utf-8 -*-
"""DNN Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lPHk8wbBb-DHerMp0crD4iYMl7s5QYh3
"""

!git clone https://github.com/Pravartya/MTP-2.git

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math, os, keras, copy, glob, random, cv2, PIL, shutil, numpy as np
import cv2
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/content/MTP-2/gpac_segment'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

!apt install ffmpeg

def imshow(imag):
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(imag[:, :, :]/255, interpolation='nearest')
    plt.show()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# from __future__ import print_function, division
# import os, cv2, glob, copy, shutil, numpy as np
# from tqdm import tqdm_notebook
# 
# ## Target frames: 
# if os.path.exists("frames"):
#     shutil.rmtree("frames")  
# os.makedirs("frames")
# if os.path.exists("data"):
#     shutil.rmtree("data")  
# os.makedirs("data")
# # os.system('ffmpeg -i /kaggle/input/360-video/input.mp4 -vf fps=30 -s 4096x2048 frames/frame%000d.png')
# os.system('ffmpeg -i /content/MTP-2/input.mp4 -vf fps=30 -s 3840x2048 frames/frame%000d.png')
# 
# frames = os.listdir('frames')
# i = 1
# for frm in tqdm_notebook(frames):
#     frame = "frames/" + frm
#     frame = cv2.imread(frame)
#     b,g,r = cv2.split(frame)
#     frame = cv2.merge([r,g,b])
#     j = 1
#     tiles = []
#     
#     stepr = frame.shape[0] / 200
#     stepc = frame.shape[1] / 200
#     
#     rl = [stepr*x for x in range(200) ] 
#     cl = [stepc*x for x in range(200) ] 
# 
#     
#     
#     for r in range(0, frame.shape[0], 200):
#         for c in range(0, frame.shape[1], 200):
#             tile = frame[r:r+200, c:c+200]
#             tiles.append(tile)
#             j += 1
#     
# #     for r in rl:
# #         for c in cl:
# #             r = int(r)
# #             c = int(c)
# #             tile = frame[r:r+200, c:c+200]
# #             tiles.append(tile)
# #             j += 1
#         
#     
#     name = frm[:-4]
#     np.save('data/' + name + '.npy', np.array(tiles))
#     i += 1

## Input frames: 
if os.path.exists("framesDS"):
    shutil.rmtree("framesDS")  
os.makedirs("framesDS")
if os.path.exists("dataDS"):
    shutil.rmtree("dataDS")  
os.makedirs("dataDS")
os.system('ffmpeg -i /content/MTP-2/input.mp4 -vf fps=30 -s 960x512 framesDS/frame%000d.png')
frames = os.listdir('framesDS')
i = 1
for frm in tqdm_notebook(frames):
    frame = "framesDS/" + frm
    frame = cv2.imread(frame)
    b,g,r = cv2.split(frame)
    frame = cv2.merge([r,g,b])
    j = 1
    tiles = []
    
    rl = [4*x for x in range(50) ] 
    cl = [4*x for x in range(50) ] 

    
    for r in range(0, frame.shape[0], 50):
        for c in range(0, frame.shape[1], 50):
            tile = frame[r:r+50, c:c+50]
            tiles.append(tile)
            j += 1

#     for r in rl:
#         for c in cl:
#             tile = frame[r:r+50, c:c+50]
#             tiles.append(tile)
#             j += 1


    name = frm[:-4]
    np.save('dataDS/' + name + '.npy', np.array(tiles))
    i += 1

def prep(inp, target):
    tar =[]
    inpt = []

    for i in range(0, len(target)):
        if target[i].shape[0] == 200 and target[i].shape[1] == 200 and target[i].shape[2] == 3:
            tar.append([target[i].astype(object)])
            inpt.append([inp[i].astype(object)])

    tar = np.concatenate(tar, axis=0)
    inpt = np.concatenate(inpt, axis=0)
    
    
    tar = np.asarray(tar).astype('float32')
    inpt = np.asarray(inpt).astype('float32')
    
    return inpt, tar

def prep2(reconst, x=1):
    for i in range(len(reconst)):
        for j in range(len(reconst[i])):
            for k in range(len(reconst[i][j])):
                for l in range(len(reconst[i][j][k])):
                    if x==0:
                        continue
                    elif(x==1):
                        reconst[i][j][k][l] = np.int((0.5 * reconst[i][j][k][l] + 0.5)*255)
                    else :
                        reconst[i][j][k][l] = int(reconst[i][j][k][l]*255)
                    
    return reconst

def getData():
    total_frames = 30  #(30x2)
    total_tiles  = 200 #(20x10)
    frames = random.sample(range(1, total_frames+1), 12)
    input_data = []
    target_data = []
    for frame_id in frames:
        frame   = 'data/frame'+str(frame_id)+'.npy'
        frame   = np.load(frame,allow_pickle = True)
        DSframe = 'dataDS/frame'+str(frame_id)+'.npy'
        DSframe = np.load(DSframe,allow_pickle = True)
        tiles = random.sample(range(total_tiles), 5)
        for tile_id in tiles:
            tile = resize(DSframe[tile_id], (200, 200), cv2.INTER_CUBIC)
            input_data.append(tile)
            target_data.append(frame[tile_id])
    input_data  = np.float32(np.array(input_data))/255
#     target_data = (np.float32(np.array(target_data))- 127.5) / 127.5
    for i in range(len(target_data)):
        target_data[i] = (np.float32(np.array(target_data[i]))- 127.5) / 127.5
        
    input_data, target_data = prep(input_data, target_data)
    
    yield input_data, target_data

def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    return 20 * math.log10(255.0 / math.sqrt(mse))

import math, os, keras, copy, glob, random, cv2, PIL, shutil, numpy as np
from cv2 import imread, resize, imwrite
from keras.layers import *
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Model
from keras.optimizers import *
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as keras
from keras import applications
import tensorflow
Adam = tensorflow.keras.optimizers.Adam(learning_rate=0.01)

inp, target = next(getData())

inp

weights = 'weights/'
if os.path.exists(weights):
    shutil.rmtree(weights)
os.makedirs(weights)

img_size = (200, 200, 3)
inputs = Input(img_size)

layer1    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(inputs)))
layer2    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(layer1)))
residual1 = add([layer2, layer1])
layer3    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual1)))
residual2 = add([residual1, layer3])
layer4    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual2)))
residual3 = add([residual2, layer4])
layer5    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual3)))
residual4 = add([residual3, layer5])
layer6    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual4)))
residual5 = add([residual4, layer6])
layer7    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual5)))
residual6 = add([residual5, layer7])
layer8    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(36, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual6)))
residual7 = add([residual6, layer8])
layer9    = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(24, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(residual7)))
layer10   = BatchNormalization(momentum=0.8)(ReLU()(Conv2D(24, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(layer9)))
reconst   = BatchNormalization(momentum=0.8)(ReLU()(Conv2D( 3, 3, padding = 'same', kernel_initializer = 'random_normal', bias_initializer = 'zeros')(layer10)))

model = Model(inputs = inputs, outputs = reconst)
print(model.summary())
model.compile(loss=['mse'], optimizer=Adam)

for epoch in range(100):
    inp, target = next(getData())
    
    Loss = model.train_on_batch(inp, target)
    print ("Iter: ", epoch, " Loss: ", Loss)
    if epoch % 50 == 0:
        model.save_weights('weights/weights_'+str(epoch)+'.h5')

inp, target = next(getData())
reconst     = model.predict(inp)

inp

model.load_weights('/content/weights_950.h5')
reconst = model.predict(inp)

reconst

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # reconst = int((0.5 * reconst + 0.5)*255)
# reconst = prep2(reconst, 1)
# # target  = int((0.5 * target  + 0.5)*255)
# target = prep2(target, 1)
# # inp     = int(inp*255)
# inp = prep2(inp, 2)

reconst

img1 = np.hstack((target[0], target[1]))
img2 = np.hstack((reconst[0], reconst[1]))
img3 = np.hstack((inp[0], inp[1]))
img1.shape, img2.shape, img3.shape

imshow(img3)

imshow(img2)

imshow(img1)

x = psnr(img3,img1)
print(x)

import os, math, cv2, numpy as np
"""
ffmpeg -f rawvideo -vcodec rawvideo -s 4000x2000 -r 29.97 -pix_fmt yuv420p -i NYC360_1sec.yuv -s 4000x2000 -c:v libx265 -preset slow -qp 40 -r 30 NYC360_2_5M.mp4
"""
if os.path.exists("dir1"):
    shutil.rmtree("dir1")  
os.makedirs("dir1")
if os.path.exists("dir2"):
    shutil.rmtree("dir2")  
os.makedirs("dir2")
os.system('ffmpeg -i NYC360_1sec.mp4 -vf fps=30 -s 4000x2000 dir1/frame%000d.png')
os.system('ffmpeg -i NYC360_2_5M.mp4 -vf fps=30 -s 4000x2000 dir2/frame%000d.png')

def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    return 20 * math.log10(255.0 / math.sqrt(mse))

frames = range(1, 31)
d = []
for frame_id in frames:
    frame1 = 'dir1/frame'+str(frame_id)+'.png'
    frame1 = cv2.imread(frame1)
    frame2 = 'dir2/frame'+str(frame_id)+'.png'
    frame2 = cv2.imread(frame2)
    p = psnr(frame1, frame2)
    d.append(p)
    print(p)
print("Avg: ")
print(np.mean(np.array(d)))