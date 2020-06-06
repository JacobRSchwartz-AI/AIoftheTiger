# Importing all necessary libraries
import cv2
import os

# Read the video from specified path
cam = cv2.VideoCapture("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\KetoPizza.MOV")

#folder for output
folder = 'data_1'

try:

    # creating a folder named folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0

while True:

    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        name = './' + folder + '/frame' + str(int(1+currentframe/3)) + '.jpg'

        #Record number of  frames per second
        fps = 30
        division_factor = fps / 10
        if currentframe % division_factor == 0:
            print('Creating...' + name)
            # writing the extracted images
            cv2.imwrite(name, frame)

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1

    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
