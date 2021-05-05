# LG TV cannot process tv_channels_8098306839_plus.m3u due to lack of RAM
# Need to remove unnecessary list from file and save it
from urllib import request

liveList={"USA:","UK:","CA:","ESPN+ TV"}
vodList={"MUSIC"," REPLAYS", "NEW RELEASE","COMEDY","ACTION","CHRISTMAS","DRAMA","THRILLER",
         "HORROR","4K MOVIES","DOCUMENTARY","FAMILY","SCI-FI","WESTERNS","STAND-UP","MYSTERY"}
startVod    ="#Reality"
startSeries ="S01 E01"
vodStarted  = 0
writeUrl    = 0
lineCount   = 0
url         = "https://worldagnetwork.com/"

originalFile= open("tv_channels_8098306839_plus.m3u", "r", encoding = "utf8")
targetFile  = open("short_tv.m3u", "w", encoding = "utf8")
a           = open("test.txt", "w",  encoding = "utf8")

targetFile.write("#EXTM3U\n")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
resp = request.openurl (url)
string = str(resp.read().decode("utf-8"))
a.write(string)
a.close()

for x in originalFile:
    lineCount += 1
    # Don't check until lineCount reach to 8000
    if lineCount > 8000:
        # Don't check until lineCount reach to 19000
        if (lineCount > 19000) :
            # Reached to the beginning of Series. Terminate process.
            if x.find(startSeries) != -1:
                break
        elif vodStarted == 0:
            # Reached to the beginning of VOD
            if x.find(startVod) != -1:
                vodStarted = 1
    if writeUrl:
        targetFile.write(x)
        writeUrl = 0
    else:
        # Search from VOD List
        if vodStarted:
            for t in vodList:
                if x.find(t) != -1:
                    writeUrl = 1
                    targetFile.write(x)
                    break
        # Search from LIVE TV List
        else:
            for t in liveList:
                if x.find(t) != -1:
                    writeUrl = 1
                    targetFile.write(x)
                    break
