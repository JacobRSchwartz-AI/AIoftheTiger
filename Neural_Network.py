import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks
import matplotlib.pyplot as plt
import cv2
import os, os.path
import random
import numpy as np
import keras
from Functions import resizeImage

f = open("directory.txt", "r")
path = f.read()

scored_data_name = path + "\\Test Data\\"
scored_data_folder = os.listdir(scored_data_name)

train_folders_list = []
test_folders_list = []

for folder in range(0,len(scored_data_folder)):
    if folder % 5 != 4:
        train_folders_list.append(path + "\\Test Data\\" + scored_data_folder[folder])
    else:
        test_folders_list.append(path + "\\Test Data\\" + scored_data_folder[folder])

num_train_images = 0
num_test_images = 0

for folder in range(0,len(train_folders_list)):
    if len(os.listdir(train_folders_list[folder])) >= 40000:
        num_train_images += 40000
    else:
        num_train_images += len(os.listdir(train_folders_list[folder]))

for folder in range(0,len(test_folders_list)):
    num_test_images += len(os.listdir(test_folders_list[folder]))

height_px = 144
width_px = 256

train_images = np.zeros((num_train_images,height_px,width_px,3), dtype='float64')
train_labels = np.zeros((num_train_images, 1), dtype='i4')
test_images = np.zeros((num_test_images,height_px,width_px,3), dtype='float64')
test_labels = np.zeros((num_test_images, 1), dtype='i4')

# training_proportion = 0.8
test_frame = 0
train_frame = 0
train_index = 0
test_index = 0

for folder in range(0,len(train_folders_list)):
    train_folder = os.listdir(train_folders_list[folder])
    print("Pulling images from: " + train_folders_list[folder] + " to add to training data")
    for frame in range(0, len(train_folder)):
        frame_path = train_folders_list[folder] + "\\" + train_folder[frame]
        resizeImage(width_px, height_px, frame_path)
        image = cv2.imread(frame_path)
        train_images[train_index] = image
        try:
            if int(train_folder[frame][-5]) != 1 and int(train_folder[frame][-5]) != 2 and int(train_folder[frame][-5]) != 3 and int(train_folder[frame][-5]) != 4 and int(train_folder[frame][-5]) != 5 and int(train_folder[frame][-5]) != 6:
                print(train_folder)
                print(train_folder[frame])
        except ValueError:
            print(train_folder[frame])
        train_labels[train_index][0] = int(train_folder[frame][-5]) - 1
        train_index += 1
        # if frame % round(len(train_folder) / 100) == 0:
        #     print(str(int(frame / round(len(train_folder) / 100))) + "% done adding to training array")
        if frame == 39999:
            break

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
        # if frame % round(len(test_folder) / 100) == 0:
        #     print(str(int(frame / round(len(test_folder) / 100))) + "% done adding to testing array")



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
class_names = ['Golfer-Half', 'Golfer-Full', 'Blue/Grey Background', 'Green/Yellow Background', 'Box top']

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

# model = models.Sequential()
# model.add(layers.Conv2D(32, (9, 9), activation='relu', input_shape=(height_px, width_px, 3), padding='same'))
# model.add(layers.Conv2D(32, (9, 9), activation='relu', padding='same'))
# model.add(layers.Conv2D(32, (9, 9), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
# model.add(layers.Conv2D(32, (7, 7), activation='relu', padding='same'))
# model.add(layers.Conv2D(32, (7, 7), activation='relu', padding='same'))
# model.add(layers.Conv2D(32, (5, 5), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
# model.add(layers.Conv2D(32, (5, 5), activation='relu', padding='same'))
# model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
# model.add(layers.Conv2D(32, (2, 2), activation='relu', padding='same'))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Flatten())
# model.add(layers.Dense(32, activation='relu'))
# model.add(layers.Dense(8))
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(height_px, width_px, 3), padding='same'))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.Dropout(0.5, noise_shape=None, seed=None))
model.add(layers.Flatten())
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(5))
model.summary()

# opt = tf.keras.optimizers.SGD(learning_rate=0.05, momentum=0.9)

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

checkpoint = tf.keras.callbacks.ModelCheckpoint('REre-test-model-{epoch:03d}.h5', verbose=1, monitor='val_accuracy',save_best_only=True, mode='auto')

model.fit(train_images, train_labels, batch_size=32, epochs=36, validation_data=(test_images, test_labels), callbacks=[checkpoint])

model.save("my_model")

# plt.plot(history.history['accuracy'], label='accuracy')
# plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.ylim([0.5, 1])
# plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)