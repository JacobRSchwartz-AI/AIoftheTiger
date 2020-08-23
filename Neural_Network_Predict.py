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
from Screenshot_Tool import screenshot_from_url


# Method to get our Neural Network to only run our OCR tool on images
# that we want to see
def image_analyzer(test_img_path, reconstructed_model, stop_token, creds, golfer_list, drive_service=None, doc_service=None, driver=None):
    # make a copy of the image of interest and resize it for
    # use in our Neural Network
    # print(test_img_path)
    shutil.copyfile(test_img_path, test_img_path[:-4] + "_NN.jpg")
    resizeImage(256, 144, test_img_path)
    test_img = cv2.imread(test_img_path)

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
        found = main_ocr(test_img_path[:-4] + "_NN.jpg", "googleDriveImage.jpg", golfer_list, creds, drive_service, doc_service)
        # print(test_img_path)
        # if tiger == True:
        #     os.rename(test_img_path[:-4] + "_NN.jpg", test_img_path[:-4] + "_OCR_TIGER.jpg")
    elif score_prediction != 5 and stop_token == False:
        stop_token = True
    

    return found, score_prediction, stop_token, start_time


if __name__ == "__main__":

    # change the directory to match the correct directory that we will be
    # working out of in our terminal
    os.chdir("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger")
    f = open("directory.txt", "r")
    path = f.read()

    # creates a copy of our testing data set so that we don't have to
    # redownload a copy
    if os.path.exists(path + "Live Test Subset"):
        shutil.rmtree(path + "Live Test Subset")
    shutil.copytree(path + "Live Test Subset - Copy", path + "Live Test Subset")

    # test_img_path = path + "Test Data\\\\" + "scored_TW BMW Round 1 2018 Folder\\\\" + "117_frame_2.jpg"

    # defines the model we use for our Neural Network
    my_model = path + "RE-test-model-030.h5"
    reconstructed_model = tf.keras.models.load_model(my_model)

    # gets all our tools to run the OCR
    creds, drive_service, doc_service = prepare_ocr()

    # defines which folder we want to run the image analyzer on
    test_folder_path = path + "Test Data\\\\REscored_Phil Mickelson shoots 5-under 67 _ Round 3 _ AT&T Pebble Beach 2020-rDk2vx45_CQ Folder\\\\"
    test_folder = os.listdir(test_folder_path)
    test_folder = sorted_alphanumeric(test_folder)

    # # Runs the image analyzer on all images in the folder
    # for image in range(0, len(test_folder)):
    #     test_img_path = test_folder_path + test_folder[image]
    #     # result = image_analyzer(test_img_path, reconstructed_model, creds, drive_service=None, doc_service=None)
    #     if test_folder[image][-5] == "N":
    #         os.remove(test_img_path)

    wrong_counter = 0
    image = 0
    start_time = 0
    end_time = 0

    while image < len(test_folder):
        start_time = time.time()
        test_img_path = test_folder_path + "\\" + test_folder[image]
        try:
            result = image_analyzer(test_img_path, reconstructed_model, creds, drive_service, doc_service)
        except Exception as e:
            print(str(e))
        end_time = time.time()
        print(result)
        image += math.ceil(10*(end_time - start_time))
        if result[0] == True:
            test_img_path = test_folder_path + "\\" + test_folder[image]
            os.rename(test_img_path[:-4] + ".jpg", test_img_path[:-4] + "_NN_TIGER.jpg")
            image += 1

    for image in range(0,len(test_folder)):
        test_img_path = test_folder_path + "\\" + test_folder[image]
        test_folder[image] = test_img_path

    test_folder_model = []

    for image in range(0,len(test_folder)):
        test_folder_model.append([])
        test_folder_model[image].append(test_folder[image])
        test_folder_model[image].append(reconstructed_model)
        test_folder_model[image].append(creds)
        # test_folder_model[image].append(drive_service)
        # test_folder_model[image].append(doc_service)

    # print(test_folder_model)

    start_time = time.time()

    while len(test_folder_model) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for result in executor.map(lambda p: image_analyzer(*p), test_folder_model):
                    test_folder_model.pop(0)
                    # print(test_folder_model[0])
        except Exception as e:
            print(str(e))
            print(len(test_folder_model))
        # print("Chris Webber don't call timeout!")

    # for image in range(0,len(test_folder)):
    #     image_analyzer(test_folder[image])

    end_time = time.time()
    image += round((end_time-start_time)*10)

    print(end_time-start_time)

    if str(score_prediction) != test_folder[image][-5]:
        print(test_folder[image])
        print(prediction_array)
        print(score_prediction)
        print('\n')
        wrong_counter += 1

    print(str(1-(wrong_counter/len(test_folder))))