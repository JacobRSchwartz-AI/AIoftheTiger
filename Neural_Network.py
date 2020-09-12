import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks
import matplotlib.pyplot as plt
import cv2
import os, os.path
import random
import numpy as np
import keras
import random


os.chdir(r"C:\Users\manag\Documents\GitHub\AIoftheTiger")
f = open("directory.txt", "r")
path = f.read()

#Parent folder that contains subfolders with image data
scored_data_name = path + "\\Data\\Scored Data"
scored_data_folder = os.listdir(scored_data_name)

#List of folders to add to our training set and a list of folders for our testing/validation set
train_image_list = []
test_image_list = []
random_number = 0

for folder in scored_data_folder:
    image_folder = os.listdir(scored_data_name + "\\\\" + folder)
    for image in image_folder:
        random_number = random.random()
        if random_number < 0.8:
            train_image_list.append(scored_data_name + "\\\\" + folder + "\\\\" + image)
        else:
            test_image_list.append(scored_data_name + "\\\\" + folder + "\\\\" + image)

#Input size for our image into the neural network, Ultra HD 4k shit
height_px = 144
width_px = 256

#Creates numpy arrays initally with all 0s that have the proper dimensions.
#The final 3 is for the number of color channels R G B
train_images = np.zeros((len(train_image_list),height_px,width_px,3), dtype='float64')
#Labels that are the true value the NN is trying to predict
train_labels = np.zeros((len(train_image_list), 1), dtype='i4')
test_images = np.zeros((len(test_image_list),height_px,width_px,3), dtype='float64')
test_labels = np.zeros((len(test_image_list), 1), dtype='i4')

train_index = 0
print("Adding " + str(len(train_image_list)) + " images to training set")
for image_path in train_image_list:
    if train_index % round(len(train_image_list)/100) == 0:
        print(str(round(100*train_index/len(train_image_list))) + " percent finished adding training data")
    
    image = cv2.imread(image_path)
    train_images[train_index] = image
    try:
        if int(image_path[-5]) != 1 and int(image_path[-5]) != 2 and int(image_path[-5]) != 3 and int(image_path[-5]) != 4 and int(image_path[-5]) != 5:
            print(image_path)
    except ValueError:
        print(image_path)
    train_labels[train_index][0] = int(image_path[-5]) - 1
    train_index += 1

print("Adding " + str(len(test_image_list)) + " images to testing set")
test_index = 0
for image_path in test_image_list:
    if test_index % round(len(test_image_list)/100) == 0:
        print(str(round(100*test_index/len(test_image_list))) + " percent finished adding testing data")
    
    image = cv2.imread(image_path)
    test_images[test_index] = image
    try:
        if int(image_path[-5]) != 1 and int(image_path[-5]) != 2 and int(image_path[-5]) != 3 and int(image_path[-5]) != 4 and int(image_path[-5]) != 5:
            print(image_path)
    except ValueError:
        print(image_path)
    test_labels[test_index][0] = int(image_path[-5]) - 1
    test_index += 1


# Normalize pixel values to be between 0 and 1, creates class names
train_images, test_images = train_images / 255.0, test_images / 255.0
class_names = os.listdir(scored_data_name)
# Shows the first 25 images in our dataset with the class names
# plt.figure(figsize=(10,10))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     # plt.imshow(cv2.cvtColor(train_images[i], cv2.COLOR_BGR2RGB))
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
#     # The CIFAR labels happen to be arrays, 
#     # which is why you need the extra index
#     # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#     plt.xlabel(class_names[train_labels[i][0]])
plt.show()

num_filters = 32
filter_size = (3,3)
max_pool = (2,2)
conv_dropout = 0.05
dense_dropout = 0.5

#Creates a model using tensorflow and keras
model = models.Sequential()
#Convolutional layers are used for edge detection
model.add(layers.Conv2D(num_filters, filter_size, activation='relu', input_shape=(height_px, width_px, 3), padding='same'))

#Convultional, dropout, and maxpool layers
for x in range(0,4):
    for y in range(0,4):
        model.add(layers.Dropout(conv_dropout, noise_shape=None, seed=None))
        model.add(layers.Conv2D(num_filters, filter_size, activation='relu', padding='same'))
    if x != 3:
        model.add(layers.MaxPooling2D(max_pool))

#Flatten converts it to a 1D array
model.add(layers.Flatten())
#16 node fully connected layer to the second to last layer
model.add(layers.Dense(num_filters, activation='relu'))
model.add(layers.Dropout(dense_dropout, noise_shape=None, seed=None))
#Output layer that has the same number of nodes as we have classes
model.add(layers.Dense(len(class_names)))
#Gives information about the model printed on the screen
model.summary()

#Compiles the model with the chosen optimizer, loss function, and metric
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#Checkpoint to save the best model so far
checkpoint = tf.keras.callbacks.ModelCheckpoint('7_RE-test-model-{epoch:03d}.h5', verbose=1, monitor='val_accuracy',save_best_only=True, mode='auto')

#Trains the model
model.fit(train_images, train_labels, batch_size=32, epochs=54, validation_data=(test_images, test_labels), callbacks=[checkpoint])
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)