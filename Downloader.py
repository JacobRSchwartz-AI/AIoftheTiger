from __future__ import unicode_literals
import youtube_dl

ydl_opts = {}

all_vids = ["https://www.youtube.com/watch?v=oqYbG8Zhoag&t=18731s",
            "https://www.youtube.com/watch?v=Vvi_LtvptKs",
            "https://www.youtube.com/watch?v=7XlL3xAP9cg",
            "https://www.youtube.com/watch?v=Qd434rS7GtM",
            "https://www.youtube.com/watch?v=jpYg-BK3nMc",
            "https://www.youtube.com/watch?v=4P5_Ld07sMA",
            "https://www.youtube.com/watch?v=7YpVwFmHOgM",
            "https://www.youtube.com/watch?v=d6zm0pFnFgk",
            "https://www.youtube.com/watch?v=6RxXCHruap0&t=666s",
            "https://www.youtube.com/watch?v=RekyCDGTwrY",
            "https://www.youtube.com/watch?v=ET1gjQAXrac&t=43s",
            "https://www.youtube.com/watch?v=42LZIShl4II",
            "https://www.youtube.com/watch?v=6rnrAEL8evA"]

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in range(0,len(all_vids)):
        ydl.download([all_vids[url]])
        print(str(int(url+1)) + " out of " + str(len(all_vids)) + " complete")