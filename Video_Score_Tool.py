import xlsxwriter
import time
import keyboard

init_time = time.time()

filepath = "image_score.csv"

def record_data():
    seconds = 0.0993
    woods = 0
    total_frames = 180
    data = [[],[]]
    print(woods)
    woods_prev = woods
    for i in range(0, total_frames):
        start_time = time.time()
        data[0].append(woods)
        data[1].append(start_time)
        if woods_prev != woods:
            print(woods)
            woods_prev = woods
        elif keyboard.is_pressed("S"):
            woods = (woods+1)%2
        while True:
            current_time = time.time()
            if start_time + seconds <= current_time:
                break
    return data



def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        file.write("{},{}\n".format("Tiger", init_time))
        for x in range(0,len(data[0])):
            file.write("{},{}\n".format(data[0][x],data[1][x]))


print("On your marks")
time.sleep(1)
print("Get Ready")
time.sleep(1)
print("Get Set")
time.sleep(1)
print("Go!")

tiger_tracker = record_data()
write_to_file(filepath, tiger_tracker)

end_time = time.time()

print(end_time - init_time)
