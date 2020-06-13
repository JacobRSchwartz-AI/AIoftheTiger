from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}

all_vids = ["https://www.youtube.com/watch?v=Pxee-0nxuls",
            "https://www.youtube.com/watch?v=cBn7V2tU5QA",
            "https://www.youtube.com/watch?v=XbRitWGzL40",
            "https://www.youtube.com/watch?v=er5hfQgSQrc",
            "https://www.youtube.com/watch?v=zNLac85aj1A"
            ]

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in range(0,len(all_vids)):
        ydl.download([all_vids[url]])
        print(str(int(url+1)) + " out of " + str(len(all_vids)) + " complete")