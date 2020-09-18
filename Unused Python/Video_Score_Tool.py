import time
import keyboard
import os
import cv2
import pandas as pd
import shutil
import Functions


#When Program Starts
init_time = time.time()
path = os.getcwd() + "\\"

#Live stream of 1s and 0s every
def record_data(dir,video,woods):
    fps = video.get(cv2.CAP_PROP_FPS)
    print(fps)
    ideal_seconds = 1/(fps/3)
    seconds = ideal_seconds
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

        # If a change has occurred print the updated value of woods and reset equality
        if woods_prev != woods:
            print(woods)
            woods_prev = woods

        #On button  press change the stream of outgoing 0s to 1s and change 1s to 0s.
        elif keyboard.is_pressed("S"):
            woods = (woods+1) % 2

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
            seconds = seconds*0.998
            #print("Positive correction error when i=" + str(i))

        elif error <= -1*ideal_seconds:
            time.sleep(abs(error))
            #print("Negative correction error when i=" + str(i))
            seconds = seconds*1.002

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


video_files = [

                    "Brooks Koepkas highlights Round 1 3M",
                    "Brooks Koepka's highlights _ Round 2 _ TOUR Championship 2019-FwG4GzJjC8s",
                    "Bryson DeChambeau Rocket Mortgage Classic",
                    "Dustin Johnson WGCMexico",
                    "Jon Rahm shoots 7-under 65 _ Round 3 _ Farmers 2020-ASvCXGI4ark",
                    "Jordan Spieth's winning highlights from 2017 AT&T Pebble Beach Pro-Am-PTXpmjlI3yg",
                    "Justin Thomas' Winning Highlights From The 2020 Sentry Tournament of Champions-z_lzGbUKhmY",
                    "Patrick Reed wins the 2020 WGC-Mexico Championship _ Extended Highlights-vQwSVE7gjBM",
                    "Phil Mickelson shoots 5-under 67 _ Round 3 _ AT&T Pebble Beach 2020-rDk2vx45_CQ",
                    "Phil Mickelson shoots 7-under 63 _ Round 2 _ Travelers Championship 2020-KW4xetuxjqY",
                    "Rickie Fowlers BMW Championship",
                    "Rory McIlroy shoots 7-under 63 _ Round 2 _ Charles Schwab Challenge-MIe8lPGqxIU",
                    "Rory McIlroy's winning highlights from TOUR Championship 2019-jSS-_Iu0Qkw",

                      ]
for video in range(0,len(video_files)):
    woods = 1   # Initial value of first frame
    video_file = video_files[video] + ".mp4"

    #Inital Variables
    folder = video_file[:-4] + ' Folder'
    dir = path + folder  # Folder with frames of video we're pulling from
    video = cv2.VideoCapture(path + video_file) # From original video find fps

    automatic_manual = int(input("Enter 0 to automatically score with all 0s and 1 to manually score: "))
    #automatic_manual = 0

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
    src = path +  img_folder
    dst = path + "Scored Data\\scored_" + img_folder
    print("Copying Data")

    try:
        shutil.copytree(src, dst)
    except FileExistsError:
        print("Folder " + dst + " already exists")
        decision = int(input("Enter 0 to overwrite and 1 to keep additional scored copies: "))
        if decision == 0:
            shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print("Overwriting Data")
        else:
            dst += str(2)
            shutil.copytree(src, dst)
            print("Copying Data")



    #Locates scores for
    loc = (path + data_scores)

    #Reads in the image score file to create a df of the binary digits.
    df = pd.read_csv(loc, header=None, index_col=False)

    #For each score, attach it to the end of the name of the frame its associated with.
    for label in range(0, len(df)):
        if label % round(len(df)/100) == 0:
            print(str(int(label/round(len(df)/100))) + "% done")
        img_score = df.iloc[label, 0]
        os.rename(dst + "\\frame" + str(label+1) + '.jpg',
                dst + "\\" + str(label+1) + "_frame_" + str(img_score) + '.jpg')


    reaction_time_fixer(dst, 256, 144)

end_time = time.time()

print(end_time - init_time)
