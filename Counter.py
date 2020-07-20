import os

f = open("directory.txt", "r")
path = f.read()


scored_data_name = path + "\\Test Data\\"
scored_data_folder = os.listdir(scored_data_name)

for folder in range(0, len(scored_data_folder)):
    files = os.listdir(path + "\\Test Data\\" + scored_data_folder[folder])
    one_counter = 0
    for image in range(0, len(files)):
        if files[image][-5] == "1":
            one_counter += 1
    print("Num of ones: " + str(one_counter))
    print(str(len(files) - one_counter))
