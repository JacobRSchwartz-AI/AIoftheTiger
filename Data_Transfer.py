import os
import shutil

f = open("directory.txt", "r")
path = f.read()

test_data_path = path + "Test Data"
test_data_folder = os.listdir(test_data_path)

# print(test_data_folder)

for folder in test_data_folder:
    print(folder)
    image_folder = os.listdir(test_data_path + "\\\\" + folder)
    for image in image_folder:
        os.rename(test_data_path + "\\\\" + folder + "\\\\" + image, test_data_path + "\\\\" + folder + "\\\\" + folder + "_" + image)
        shutil.move(test_data_path + "\\\\" + folder + "\\\\" + folder + "_" + image, path + "Data\\\\Scored Data\\\\" + image[-5])