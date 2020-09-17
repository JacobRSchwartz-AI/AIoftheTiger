import os
import shutil
import tensorflow as tf
import numpy as np
import cv2

f = open("directory.txt", "r")
path = f.read()

scored_data_path = path + "Data\\\\Scored Data"
scored_data_folder = os.listdir(scored_data_path)

# defines the model we use for our Neural Network
my_model = path + "6_RE-test-model-029.h5"
reconstructed_model = tf.keras.models.load_model(my_model)

for folder in scored_data_folder:
    images_correct = 0
    image_folder = os.listdir(scored_data_path + "\\\\" + folder)
    for image in image_folder:
        test_img = cv2.imread(scored_data_path + "\\\\" + folder + "\\\\" + image)
        # convert image to pixel values and standardize them
        test_img_array = np.zeros((1, 144, 256, 3), dtype='float64')
        test_img_array[0] = test_img / 255

        # make our prediction of what the image is
        prediction_array = reconstructed_model.predict(test_img_array)
        prediction_array = prediction_array[0]

        # grab what the Neural Network predicts the image is showing
        result = np.where(prediction_array == np.amax(prediction_array))
        score_prediction = result[0][0] + 1
        if str(score_prediction) == image[-5]:
            images_correct += 1
    percent_correct = 100 * images_correct / len(image_folder)
    print(str(percent_correct) + "% correct for " + str(folder) + " class")