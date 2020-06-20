import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import cv2
import os, os.path
import random
import ResizeImages
import numpy as np


# ResizeImages.resizeImage(256, 144, "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_TW Memorial Round 3 2018 Folder\\1_frame_1.jpg")

f = open("directory.txt", "r")
path = f.read()

folder_name = path + "\\Scored Data\\scored_TW Memorial Round 3 2018 Folder"
print(folder_name)
folder = os.listdir(folder_name)

print(len(folder))

total_images = len(folder)
num_train_images = round(0.8*total_images)
num_test_images = total_images - num_train_images

train_images = np.zeros((num_train_images,144,256,3))
train_labels = np.zeros(num_train_images)
test_images = np.zeros((num_test_images,144,256,3))
test_labels = np.zeros((num_test_images))

training_proportion = 0.8
test_frame = 0
train_frame = 0

for frame in range(0, len(folder)):
    frame_path = folder_name + "\\" + folder[frame]
    ResizeImages.resizeImage(256, 144, frame_path)
    image = cv2.imread(frame_path)
    if frame%5 != 4:
        if frame == len(folder)-1 and (len(folder)%5 == 3 or len(folder)%5 == 4):
            test_images[num_test_images-1]= image
            test_labels[num_test_images-1] = (int(folder[frame][-5]))
        else:
            train_images[train_frame] = image
            train_labels[train_frame] = (int(folder[frame][-5]))
            train_frame += 1
    else:
        test_images[test_frame] = image
        test_labels[test_frame] = (int(folder[frame][-5]))
        test_frame += 1

    if frame % round(len(folder) / 100) == 0:
        print(str(int(frame / round(len(folder) / 100))) + "% done adding to lists")



# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# print(len(train_images))
# print(len(train_images[0]))
# print(len(train_images[0][0]))
# print(len(train_images[0][0][0]))
# print(len(train_images[0][0][0][0]))


#print(len(train_images[0][0]))

# train_images = np.array(train_images)
# train_labels = np.array(train_labels)
# test_images =  np.array(test_images)
# test_labels = np.array(test_labels)


# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0

class_names = ['Not Tiger', 'Tiger']

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    # The CIFAR labels happen to be arrays, 
    # which is why you need the extra index
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(144, 256, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=10, 
                    validation_data=(test_images, test_labels))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)