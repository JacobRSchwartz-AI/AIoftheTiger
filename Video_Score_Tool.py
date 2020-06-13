import xlsxwriter
import time
import keyboard
import os
import cv2
import pandas as pd
import shutil


#When Program Starts
init_time = time.time()

#Live stream of 1s and 0s every
def record_data(dir,video,woods):

    fps = video.get(cv2.CAP_PROP_FPS)
    ideal_seconds = 1/(fps/3)
    seconds = ideal_seconds - 0.00088
    list = os.listdir(dir)      # dir is your directory path
    total_frames = len(list)    # list of video frames
    data = [[],[]]              # Data structure is a nested list AKA list of lists
    print(woods)                # Prints the initial value of woods, won't change until "S" is pressed
    woods_prev = woods          # Essentially copies woods, will be used to see if a change has occurred.

    error = 0
    i = 0


    while i < total_frames:


        start_time = time.time()

        #appends woods and start_time to  the beginning of the list.
        data[0].append(woods)
        data[1].append(start_time)

        if i > 0:
            error += (data[1][i] - data[1][i-1] - ideal_seconds)


        #If a change has occurred print the updated value of woods and reset equality
        if woods_prev != woods:
            print(woods)
            woods_prev = woods

        #On button  press change the stream of outgoing 0s to 1s and change 1s to 0s.
        elif keyboard.is_pressed("S"):
            woods = (woods+1)%2

        #Loop designed to slow the program down to 10 iterations per second.
        while True:
            current_time = time.time()
            if start_time + seconds <= current_time:
                break

        #print(error)
        if error >= ideal_seconds:
            data[0].append(woods)
            data[1].append(start_time)
            i += 1
            error -= ideal_seconds
            #print("Positive correction error when i=" + str(i))

        elif error <= -1*ideal_seconds:
            time.sleep(abs(error))
            #print("Negative correction error when i=" + str(i))

        i += 1
    return data


#Takes a list of lists and writes  it to a csv file.
def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0,len(data[0])):
            file.write("{},{}\n".format(data[0][x],data[1][x]))

def auto_write_to_file(filepath: str, dir):
    with open(filepath, "w") as file:
        for x in range(0, len(os.listdir(dir))):
            if x % round(len(os.listdir(dir)) / 100) == 0:
                print(str(int(x / round(len(os.listdir(dir)) / 100))) + "% done with writing to CSV file")
            file.write("{}\n".format(0))


woods = 0   # Initial value of first frame
video_file = "Tony Finau's Third Round in Three Minutes" + ".mp4"

#Inital Variables
folder = video_file[:-4] + ' Folder'
dir = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + folder  # Folder with frames of video we're pulling from
video = cv2.VideoCapture("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + video_file) # From original video find fps

automatic_manual = int(input("Enter 0 to automatically score with all 0s and 1 to manually score: "))

#Output file of scores
data_scores = video_file[:-4] + " Data.csv"

if automatic_manual == 1:
    # Start of execution, allows for 3 seconds from starting this program to starting a video to score.
    print("On your marks")
    time.sleep(1)
    print("Get Ready")
    time.sleep(1)
    print("Get Set")
    time.sleep(1)
    print("Go!")
    tiger_tracker = record_data(dir, video, woods)

    print("Done recording data, now writing to CSV")
    write_to_file(data_scores, tiger_tracker)
else:
    print("Now auto-scoring")
    auto_write_to_file(data_scores, dir)



#Folder that contains Split out images
img_folder = video_file[:-4] + ' Folder'

#Makes copy of folder
src = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" +  img_folder
dst = "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_" + img_folder
print("Copying Data")
shutil.copytree(src, dst)


#Locates scores for
loc = ("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\" + data_scores)

#Reads in the image score file to create a df of the binary digits.
df = pd.read_csv(loc, header=None, index_col=False)

#For each score, attach it to the end of the name of the frame its associated with.
for label in range(0, len(df)):
    if label % round(len(df)/100) == 0:
        print(str(int(label/round(len(df)/100))) + "% done")
    img_score = df.iloc[label, 0]
    os.rename("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_" + img_folder + "\\frame" + str(label+1) + '.jpg',
              "C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\Scored Data\\scored_" + img_folder + "\\" + str(label+1) + "_frame_" + str(img_score) + '.jpg')




end_time = time.time()

print(end_time - init_time)
