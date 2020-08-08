import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks
import matplotlib.pyplot as plt
import cv2
import os, os.path
import numpy as np
import keras
import shutil
import time
from Functions import sorted_alphanumeric, resizeImage
from OCR import main_ocr, prepare_ocr

f = open("directory.txt", "r")
path = f.read()
my_model = path + "test-model-017.h5"

# test_img_path = path + "Test Data\\\\" + "scored_TW BMW Round 1 2018 Folder\\\\" + "117_frame_2.jpg" 

test_folder_path = path + "2008_U.S._Open_Final_Round_Full_Telecast-Vvi_LtvptKs Folder\\\\" 
test_folder = os.listdir(test_folder_path)
test_folder = sorted_alphanumeric(test_folder)

reconstructed_model = tf.keras.models.load_model(my_model)

creds, drive_service, doc_service = prepare_ocr()

# wrong_counter = 0
image = 0
start_time = 0
end_time = 0

while image < len(test_folder):
    start_time = time.time()
    if image % 4 == 0:
        print(image)
    test_img_path = test_folder_path + "\\" + test_folder[image]
    shutil.copyfile(test_img_path, test_img_path[:-4] + "ocr.jpg")
    
    #NN Stuff Beginning
    resizeImage(256,144,test_img_path)
    test_img = cv2.imread(test_img_path)
    test_img_array = np.zeros((1,144,256,3), dtype='float64')
    test_img_array[0] = test_img / 255

    prediction_array = reconstructed_model.predict(test_img_array)
    prediction_array = prediction_array[0]

    result = np.where(prediction_array == np.amax(prediction_array))
    score_prediction = result[0][0] + 1
    #End NN Stuff

    #Start OCR tool
    tiger = main_ocr(test_img_path[:-4] + "ocr.jpg", test_folder[image], creds, drive_service, doc_service)
    #End of OCR tool

    #Wait for both to complete
    if tiger == True and score_prediction == 2:
        os.rename(test_img_path[:-4] + "ocr.jpg", test_img_path[:-4] + "ocr_C.jpg")

    end_time = time.time()
    image += round((end_time-start_time)*10)

    # if str(score_prediction) != test_folder[image][-5]:
    #     print(test_folder[image])
    #     print(prediction_array)
    #     print(score_prediction)
    #     print('\n')
    #     wrong_counter += 1

# print(str(1-(wrong_counter/len(test_folder))))