import xlsxwriter
import time
import keyboard
import os


#When Program Starts
init_time = time.time()

#Live stream of 1s and 0s every
def record_data(dir,ideal_seconds,woods):
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


        print(error)
        if error >= ideal_seconds:
            data[0].append(woods)
            data[1].append(start_time)
            i += 1
            error -= ideal_seconds
            print("Positive correction error when i=" + str(i))

        elif error <= -1*ideal_seconds:
            time.sleep(abs(error))
            print("Negative correction error when i=" + str(i))

        i += 1
    return data


#Takes a list of lists and writes  it to a csv file.
def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0,len(data[0])):
            file.write("{},{}\n".format(data[0][x],data[1][x]))


#Start of execution, allows for 3 seconds from starting this program to starting a video to score.
print("On your marks")
time.sleep(1)
print("Get Ready")
time.sleep(1)
print("Get Set")
time.sleep(1)
print("Go!")

#Inital Variables
dir = r'C:\Users\manag\PycharmProjects\AIoftheTiger\data_1'
ideal_seconds = 0.1
woods = 0

tiger_tracker = record_data(dir, ideal_seconds, woods)

print("Done recording data, now writing to CSV")

#Output file
filepath = "image_score_testing2.csv"

write_to_file(filepath, tiger_tracker)

end_time = time.time()

print(end_time - init_time)
