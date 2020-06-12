# Importing all necessary libraries
import cv2
import os


def video_splitter(cam, folder):
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

            if currentframe % 3 == 0:
                if currentframe % 300 == 0:
                    os.system('cls')
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


unsplit_video_files = [

                        "Tony Finau Highlights _ Round 2 _ 2018 WGC",
                        "Tony Finau shoots 9-under 62 _ Round 3 _ Waste Management 2020",
                        "Tony Finau shoots 10-under 62 _ Round 2 _ The American Express 2020",
                        "Tony Finau's Highlights _ Round 3 _ Hero World Challenge 2018",
                        "Tony Finau's Third Round in Three Minutes"

                      ]


for video in range(0,len(unsplit_video_files)):
    # Read the video from specified path
    cam = cv2.VideoCapture("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + unsplit_video_files[video] + ".mp4")

    #folder for output
    folder = unsplit_video_files[video] + ' Folder'

    video_splitter(cam, folder)