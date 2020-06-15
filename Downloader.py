from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}

all_vids = ["https://www.youtube.com/watch?v=d6zm0pFnFgk",
            "https://www.youtube.com/watch?v=uWngIqTI1aA"
            ]

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in range(0,len(all_vids)):
        ydl.download([all_vids[url]])
        print(str(int(url+1)) + " out of " + str(len(all_vids)) + " complete")