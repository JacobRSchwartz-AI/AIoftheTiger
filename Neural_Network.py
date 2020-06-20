import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import cv2
import os, os.path
import random

# test_pic = cv2.imread("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_TW Zozo Rounds 1-4 2019 Folder\\12_frame_1.jpg")
#print(len(test_pic[0][0]))

folder_name = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_TW Memorial Round 3 2018 Folder"
folder = os.listdir(folder_name)

print(len(folder))

train_images = []
train_lables = []
test_images = []
test_lables = []

for frame in range(0,len(folder)):
    random_value = random.random()    
    if random_value < 0.8:
        image = cv2.imread(folder_name + "\\" + folder[frame])
        train_images.append(image)
        train_lables.append(int(folder[frame][-5]))
    else:
        image = cv2.imread(folder_name + "\\" + folder[frame])
        test_images.append(image)
        test_lables.append(int(folder[frame][-5]))

    if frame % round(len(folder) / 100) == 0:
        print(str(int(frame / round(len(folder) / 100))) + "% done adding to lists")
        



# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

#print(len(train_images[0][0]))

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
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
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