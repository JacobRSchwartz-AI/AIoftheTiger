import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks
import matplotlib.pyplot as plt
import cv2
import os, os.path
import random
import numpy as np
import keras
import random
from Functions import resizeImage

os.chdir(r"C:\Users\manag\Documents\GitHub\AIoftheTiger")
f = open("directory.txt", "r")
path = f.read()

#Parent folder that contains subfolders with image data
scored_data_name = path + "\\Test Data\\"
scored_data_folder = os.listdir(scored_data_name)

#List of folders to add to our training set and a list of folders for our testing/validation set
train_folders_list = []
test_folders_list = []

rand_num = random.randint(0,4)

#Loops through all possible subfolders, puts every 5th one into our testing set
for folder in range(0,len(scored_data_folder)):
    if folder % 5 != rand_num:
        train_folders_list.append(path + "\\Test Data\\" + scored_data_folder[folder])
    else:
        test_folders_list.append(path + "\\Test Data\\" + scored_data_folder[folder])

#Counts the nummber of training and testing images per folder
num_train_images = 0
num_test_images = 0

#Caps the amount of images from 1 folder at 40,000
for folder in range(0,len(train_folders_list)):
    if len(os.listdir(train_folders_list[folder])) >= 40000:
        num_train_images += 40000
    else:
        num_train_images += len(os.listdir(train_folders_list[folder]))

for folder in range(0,len(test_folders_list)):
    if len(os.listdir(test_folders_list[folder])) >= 40000:
        num_test_images += 40000
    else:
        num_test_images += len(os.listdir(test_folders_list[folder]))

#Input size for our image into the neural network, Ultra HD 4k shit
height_px = 144
width_px = 256

#Creates numpy arrays initally with all 0s that have the proper dimensions.
#The final 3 is for the number of color channels R G B
train_images = np.zeros((num_train_images,height_px,width_px,3), dtype='float64')
#Labels that are the true value the NN is trying to predict
train_labels = np.zeros((num_train_images, 1), dtype='i4')
test_images = np.zeros((num_test_images,height_px,width_px,3), dtype='float64')
test_labels = np.zeros((num_test_images, 1), dtype='i4')

#Loop counters that continue across subfolders
train_index = 0
test_index = 0

#Loops through all of our training folders and adds the RGB values and labels to the proper arrays
for folder in range(0,len(train_folders_list)):
    train_folder = os.listdir(train_folders_list[folder])
    print("Pulling images from: " + train_folders_list[folder] + " to add to training data")
	#For every frame in each subfolder
    for frame in range(0, len(train_folder)):
        frame_path = train_folders_list[folder] + "\\" + train_folder[frame]
		#Resize image to the size that the NN will accept
        resizeImage(width_px, height_px, frame_path)
		#Adds the RGB values of the image to the numpy array
        image = cv2.imread(frame_path)
        train_images[train_index] = image
		#Debugging that helps us look for data that might lead to nan loss
        try:
            if int(train_folder[frame][-5]) != 1 and int(train_folder[frame][-5]) != 2 and int(train_folder[frame][-5]) != 3 and int(train_folder[frame][-5]) != 4 and int(train_folder[frame][-5]) != 5:
                print(train_folder)
                print(train_folder[frame])
        except ValueError:
            print(train_folder[frame])
		#Adds the label to its array
        train_labels[train_index][0] = int(train_folder[frame][-5]) - 1
        train_index += 1
		#Limit of 40000 images per folder
        if frame == 39999:
            break

#Very similar logic as above, but adds it to the testing array to calculate validation accurracy 
for folder in range(0,len(test_folders_list)):
    test_folder = os.listdir(test_folders_list[folder])
    print("Pulling images from: " + test_folders_list[folder] + " to add to testing data")
    for frame in range(0, len(test_folder)):
        frame_path = test_folders_list[folder] + "\\" + test_folder[frame]
        resizeImage(width_px, height_px, frame_path)
        image = cv2.imread(frame_path)
        test_images[test_index] = image
        test_labels[test_index][0] = int(test_folder[frame][-5]) - 1
        test_index += 1



# Normalize pixel values to be between 0 and 1, creates class names
train_images, test_images = train_images / 255.0, test_images / 255.0
class_names = ['Golfer-Half', 'Golfer-Full', 'Blue/Grey Background', 'Green/Yellow Background', 'Box top']

#Shows the first 25 images in our dataset with the class names
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
# plt.show()

num_filters = 32
filter_size = (3,3)
max_pool = (2,2)
conv_dropout = 0.1
dense_dropout = 0.5

#Creates a model using tensorflow and keras
model = models.Sequential()
#Convolutional layers are used for edge detection
model.add(layers.Conv2D(num_filters, filter_size, activation='relu', input_shape=(height_px, width_px, 3), padding='same'))


for x in range(0,4):
    for y in range(0,4):
        if y%2 == 0:
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
checkpoint = tf.keras.callbacks.ModelCheckpoint('6_RE-test-model-{epoch:03d}.h5', verbose=1, monitor='val_accuracy',save_best_only=True, mode='auto')

#Trains the model
model.fit(train_images, train_labels, batch_size=32, epochs=54, validation_data=(test_images, test_labels), callbacks=[checkpoint])

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)