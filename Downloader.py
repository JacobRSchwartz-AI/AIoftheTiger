from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}

all_vids = ["https://www.youtube.com/watch?v=HK_Z2stfZ7s",
            "https://www.youtube.com/watch?v=k6Nm2ITIl4o",
            "https://www.youtube.com/watch?v=jqGg6VPBIS0",
            "https://www.youtube.com/watch?v=AszF5_Xflx0",
            "https://www.youtube.com/watch?v=7e1mkKymbzU"
            ]

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in range(0,len(all_vids)):
        ydl.download([all_vids[url]])
        print(str(int(url+1)) + " out of " + str(len(all_vids)) + " complete")