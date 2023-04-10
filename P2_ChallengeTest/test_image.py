#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:13:14 2023

@author: mehernagpal
"""

##### turn certificate verification off  #####
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

## import libraries
import tensorflow as tf
import matplotlib.pyplot as plt
import pathlib
import certifi

#https://stackoverflow.com/questions/72479044/cannot-import-name-load-img-from-keras-preprocessing-image
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import load_model




class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

def load_image(filename):
	img = load_img(filename, target_size=(32, 32))
	img = img_to_array(img)
	img = img.reshape(1, 32, 32, 3)
	img = img / 255.0
	return img

##################################################################
## This is the model that you built from your improvement using ##
##  the baseline file CNNbaseline.py                            ##
##################################################################
# load the trained CIFAR10 model
model = load_model('MN_CIFARmodel_baseline.h5')

##################################################################
# get the image from the internet
URL = "https://upload.wikimedia.org/wikipedia/commons/0/03/American_quarter_horse.jpg"
picture_path  = tf.keras.utils.get_file(origin=URL)
img = load_image(picture_path)
result = model.predict(img)

# show the picture
image = plt.imread(picture_path)
plt.imshow(image)
plt.show()
# show prediction result.
print('\nPrediction: This image most likely belongs to ' + class_names[int(result.argmax(axis=-1))])

##################################################################
# get the image from the internet
URL = "https://image.shutterstock.com/image-vector/airplane-600w-646772488.jpg"
picture_path  = tf.keras.utils.get_file(origin=URL)
img = load_image(picture_path)
result = model.predict(img)


# show the picture
image = plt.imread(picture_path)
plt.imshow(image)
plt.show()
# show prediction result.
print('\nPrediction: This image most likely belongs to ' + class_names[int(result.argmax(axis=-1))])

#################################################################################
## You can either write a for loop for all 5 pictures or just add 3 more below ##
#################################################################################

URL = "https://upload.wikimedia.org/wikipedia/commons/5/53/Weaver_bird.jpg"
picture_path  = tf.keras.utils.get_file(origin=URL)
img = load_image(picture_path)
result = model.predict(img)

# show the picture
image = plt.imread(picture_path)
plt.imshow(image)
plt.show()


