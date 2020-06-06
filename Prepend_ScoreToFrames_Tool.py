# Importing all necessary libraries
import os
import pandas as pd
import shutil

#Folder that contains Split out images
data_file = 'data_1'

#Makes copy of folder
src = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" +  data_file
dst = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\scored_" + data_file
shutil.copytree(src, dst)


#Locates scores for
loc = ("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\image_score_" + data_file + ".csv")

#Reads in the image score file to create a df of the binary digits.
df = pd.read_csv(loc, header=None, index_col=False)

#For each score, attach it to the end of the name of the frame its associated with.
for label in range(0, len(df)):
    img_score = df.iloc[label, 0]
    os.rename(r'C:\Users\manag\PycharmProjects\AIoftheTiger\scored_data_1\frame' + str(label+1) + '.jpg',
              "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\scored_data_1\\" + str(label+1) + '_frame_' + str(img_score) + '.jpg')






