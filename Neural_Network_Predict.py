import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks
import matplotlib.pyplot as plt
import cv2
import math
import os, os.path
import numpy as np
import keras
import shutil
import time
import copy
import threading
import concurrent.futures
from queue import Queue
from Functions import sorted_alphanumeric, resizeImage
from OCR import main_ocr, prepare_ocr



# Method to get our Neural Network to only run our OCR tool on images
# that we want to see
def image_analyzer(test_img_path, reconstructed_model, stop_token, creds, golfer_list, drive_service=None, doc_service=None, driver=None):
    # make a copy of the image of interest and resize it for
    # use in our Neural Network
    # print(test_img_path)
    shutil.copyfile(test_img_path, test_img_path[:-4] + "_OCR.jpg")
    resizeImage(256, 144, test_img_path)
    test_img = cv2.imread(test_img_path)
    resizeImage(630, 360, test_img_path[:-4] + "_OCR.jpg")
    

    # convert image to pixel values and standardize them
    test_img_array = np.zeros((1, 144, 256, 3), dtype='float64')
    test_img_array[0] = test_img / 255

    # make our prediction of what the image is
    prediction_array = reconstructed_model.predict(test_img_array)
    prediction_array = prediction_array[0]

    # grab what the Neural Network predicts the image is showing
    result = np.where(prediction_array == np.amax(prediction_array))
    score_prediction = result[0][0] + 1
    # end_time = time.time()
    found = False

    start_time = time.time()
    # if we want to see the image run our OCR tool
    if score_prediction == 5 and stop_token == True:
        driver.execute_script('document.getElementsByTagName("video")[0].pause()')
        stop_token = False
        print(score_prediction)
        found = main_ocr(test_img_path[:-4] + "_OCR.jpg", "googleDriveImage.jpg", golfer_list, creds, drive_service, doc_service)
        # print(test_img_path)
        # if tiger == True:
        #     os.rename(test_img_path[:-4] + "_NN.jpg", test_img_path[:-4] + "_OCR_TIGER.jpg")
    elif score_prediction != 5 and stop_token == False:
        stop_token = True
    

    return found, score_prediction, stop_token, start_time