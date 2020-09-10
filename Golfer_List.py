import requests
import pandas as pd
import os

# os.chdir(r"C:\Users\manag\Documents\GitHub\AIoftheTiger")
f = open("directory.txt", "r")
path = f.read()
filepath = path + r'default_golfer_list.txt'


def get_active_golfer_list(filepath):
    active_golfers = []
    url = 'https://www.pgatour.com/stats/stat.186.html'
    try:
        html = requests.get(url).content
        df_list = pd.read_html(html)
        df = df_list[-1]

        # loop through and grab the active golfer list from url above
        for i in range(0, len(df['PLAYER NAME'])):
            player_name = df['PLAYER NAME'][i]
            start = df['PLAYER NAME'][i].find(' ')
            surname = player_name[start + 1:]
            active_golfers.append(surname.upper())
        # Easter Egg : )
        active_golfers.append("KN SEN")
        # Leader of tournament
        active_golfers.append("LEADER")

    except:
        # make a list from default golfer list
        with open(filepath, "r") as file:
            active_golfers = file.readlines()

    return active_golfers

get_active_golfer_list(filepath)