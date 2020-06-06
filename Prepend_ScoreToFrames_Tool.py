# Importing all necessary libraries
import xlrd
import os
import pandas as pd
import csv

#folder for output
folder = 'scored_data_1'

try:

    # creating a folder named scored_data_1
    if not os.path.exists(folder):
        os.makedirs(folder)

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0

# get number of columns of data points (number of frames)
loc = ("C:\\Users\\HP\\PycharmProjects\\AIOfTheTiger\\image_score_data_1.csv")

# open excel sheet
# get number of rows in file
with open(loc) as fImageScore:
    rowCount = sum(1 for line in fImageScore)

    # csvreader = csv.reader(fImageScore)
    # for row in csvreader:
    #     print(row[0])
    #     print("7")
    #
    # print(csvreader.line_num)
    # next(csvreader)

    for i in range(rowCount):
        score = i
        name = './' + folder + '/' + str(score) + 'frame' + str(int(i)) + '.jpg'
        print('Creating...' + name)


#fileObject = csv.reader(loc)
#rowCount = sum (1 for row in fileObject)
#numCols = df.axes[1]
print(rowCount)
# wb = xlrd.open_workbook(loc)
# sheet = wb.sheet_by_index(0)
#
# # Extracting number of columns from index 0 specified above
# numFrames = sheet.ncols
#
# # loop through and add the values from the excel sheet to the name of the file
#
# for i in range(numFrames):
#     score = sheet.cell_value(0, i)
#     name = './' + folder + '/' + score + 'frame' + str(int(i)) + '.jpg'
#     print('Creating...' + name)
    # write the extracted images
    #cv2.imwrite(name, frame)



# while (True):
#
#     # reading from frame
#     ret, frame = cam.read()
#
#     if ret:
#         # if video is still left continue creating images
#         name = './' + folder + '/' + 'frame' + str(int(1+currentframe/3)) + '.jpg'
#
#
#         if currentframe%3 == 0:
#             print('Creating...' + name)
#             # writing the extracted images
#             cv2.imwrite(name, frame)
#
#
#         # increasing counter so that it will
#         # show how many frames are created
#         currentframe += 1
#
#     else:
#         break
#
# # Release all space and windows once done
# cam.release()
# cv2.destroyAllWindows()
