# Importing all necessary libraries
import os
import pandas as pd
import shutil

#Takes a list of lists and writes  it to a csv file.
def auto_write_to_file(filepath: str, dir):
    with open(filepath, "w") as file:
        for x in range(0, len(os.listdir(dir))):
            file.write("{}\n".format(0))



#Folder that contains Split out images
video = '2019 PGA Championship - Final Round'

filepath = video + " Data.csv"

data_file = video + ' Folder'

dir = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + data_file  # Folder with frames of video we're pulling from

auto_write_to_file(filepath, dir)

#Makes copy of folder
src = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + data_file
dst = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_" + data_file
print("Copying Data")
shutil.copytree(src, dst)


#Locates scores for
loc = ("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + filepath)

#Reads in the image score file to create a df of the binary digits.
df = pd.read_csv(loc, header=None, index_col=False)

#For each score, attach it to the end of the name of the frame its associated with.
for label in range(0, len(df)):
    if label % round(len(df)/100) == 0:
        print(str(int(label/round(len(df)/100))) + "% done")
    img_score = df.iloc[label, 0]
    os.rename("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_" + data_file + "\\frame" + str(label+1) + '.jpg',
              "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_" + data_file + "\\" + str(label+1) + "_frame_" + str(img_score) + '.jpg')






