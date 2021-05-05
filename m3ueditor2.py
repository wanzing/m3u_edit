# LG TV cannot process tv_channels_8098306839_plus.m3u due to lack of RAM
# Need to remove unnecessary list from file and save it
# TV Channels: US, UK, CA, ESPN+ will be kept, 
from urllib import request

liveList={"CA :","CANADIAN TV", "GB :","SPORTS :","US :"}
groupArray= ["\"CANADIAN TV\",", "\"UK TV\",", "\"SPORTS TV\",", "\"USA TV\",", "\"ALL MOVIES\","]

startVod    ="#RealityHigh"
startSeries ="S01 E01"
vodStarted  = 0
writeUrl    = 0
lineCount   = 0
url         = "https://worldagnetwork.com/"

originalFile= open("tv_channels_8098306839_plus_new.m3u", "r", encoding = "ISO-8859-1")
targetFile  = open("short_tv_new.m3u", "w", encoding = "ISO-8859-1")
# a           = open("test.txt", "w",  encoding = "utf8")

# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# resp = request.openurl(url)
# string = str(resp.read().decode("utf-8"))
# a.write(string)
# a.close()


targetFile.write("#EXTM3U\n")

for x in originalFile:
    lineCount += 1
    # Don't check until lineCount reach to 3000
    # Canadian channel starts from around line 3000 and previous channels are not necessary
    if lineCount < 3000:
        continue
    if (lineCount > 31600) :
        # Don't check until lineCount reach to 31600
        # Series starts from around 31700
        if x.find(startSeries) != -1:
            # Reached to the beginning of Series. Terminate process.
            break
    elif vodStarted == 0:
        # Reached to the beginning of VOD
        if x.find(startVod) != -1:
            vodStarted = 1
            groupString = "group-title="+groupArray[4]


    if writeUrl: 
        targetFile.write(x)
        # Write 1 more line if #EXTVLCOPT exists
        if x.find("#EXTVLCOPT") != -1:
            writeUrl += 1
        else:
            writeUrl = 0
    if  vodStarted:            
        # Write 2 lines after matching liveList
        # If #EXTVLCOPT line exists, then write next line.
        if x.find("#EXTINF") != -1:
            if x.find("group-title") != -1:
                targetFile.write(x)
                # index = x.rfind("\"")
                # print(index)
                # new_string = x[:10] + groupString + x[index+1:]
            else:
                new_string = x[:10] + groupString + x[10:]
                targetFile.write(new_string)

        else:
            targetFile.write(x)
    else:
        for t in liveList:
            index = x.find(t)
            if index != -1:
                if t == "CA :" or t == "FRCAN":
                    i = 0
                elif t =="GB :":
                    i = 1
                elif t =="SPORTS :":
                    i = 2
                else:
                    i = 3
                
                groupString = "group-title="+groupArray[i]
                new_string = x[:10] + groupString + x[index:]
                writeUrl = 1
                targetFile.write(new_string)
                break

targetFile.close()
originalFile.close()