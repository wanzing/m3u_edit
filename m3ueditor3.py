# My LG TV cannot process tv_channels.m3u due to the small size of RAM
# Need to remove unnecessary list from file and save it
# TV Channels: US, UK, CA, SPORTS channels will be kept
# Movies will be kept except STAND-UP, BLACK, 3D, 4K, SPORTS REPLAYS, HD CAM
# The group name of the Movies are created from movie_list_new.m3u
# Refer to movielist_creator.py how to create movie_list_new.m3u file

liveList={"CA :","CANADIAN TV", "GB :","SPORTS :","US :"}
groupArray= ["\"CANADIAN TV\",", "\"UK TV\",", "\"SPORTS TV\",", "\"USA TV\",", "\"NEWLY ADDED\","]
blackList={"STAND-UP","BLACK","3D","4K","SPORTS","WWE","HD CAM","UFC"}

vodKeyword    ="#Real"
seriesKeyword ="S01 E01"
vodStarted  = 0
lineCount   = 0
inList    = 0
foundMatch    = 0

originalFile    = open("tv_channels.m3u", "r", encoding = "ISO-8859-1")
movieListFile   = open("movie_list_new.m3u", "r", encoding = "ISO-8859-1")
targetFile      = open("short_tv_new.m3u", "w", encoding = "ISO-8859-1")

targetFile.write("#EXTM3U\n")

for x in originalFile:
    lineCount += 1
    # Don't check until lineCount reach to 3000. This is used just for speedup.
    # Better to use seek()
    # Canadian channel starts from around line 3000 and previous channels are not necessary
    if lineCount < 3000:
        continue
    if vodStarted == 0:
        # Reached to the beginning of VOD
        if x.find(vodKeyword) != -1:
            vodStarted = 1
            groupString = "group-title="+groupArray[4]
            print("VOD Started")
    elif x.find(seriesKeyword) != -1:
        # Reached to the beginning of Series. Terminate process.
        # print("End of Process")
        break

    ######################
    # Checking VOD part
    if  vodStarted:            
        # If #EXTVLCOPT line exists, then write next line.
        foundMatch  = 0
        if x.startswith("#EXTINF"):
            strHeader = x
            strHttp = next(originalFile)
            if strHttp.startswith("http") != True:
                strHeader += strHttp
                strHttp = next(originalFile)
            
            for line in movieListFile:
                strHeaderSrc = line
                strHttpSrc = next(movieListFile)
                if strHttpSrc.startswith("http") != True:
                    # if the next line is not http://
                    # Then add it to Header and read next line for the link
                    strHeaderSrc += strHttpSrc
                    strHttpSrc = next(movieListFile)
                if strHttp == strHttpSrc:
                    # print("Found Match!")
                    foundMatch = 1
                    for strBList in blackList:
                        if strHeaderSrc.find(strBList) != -1 or strHeader.find(strBList) != -1:
                            inList = 1
                            break
                    if inList:
                        inList = 0
                        # print("In the Black List!")
                        break
                    targetFile.write(strHeaderSrc)
                    targetFile.write(strHttpSrc)
                    # print(strHeaderSrc)
                    break
            if foundMatch == 0 :
                # print("No Match! Search from beginning!")
                lineCount += 1
                movieListFile.seek(0)
                # Check if it has group-title
                for strBList in blackList:
                    if strHeader.find(strBList) != -1:
                        inList = 1
                        break
                if inList:
                    inList = 0
                    continue
                if strHeader.find("group-title") != -1:
                    index = strHeader.rfind("\"")
                else:
                    index = 8
                newHeader = strHeader[:10] + groupString + strHeader[index+2:]
                targetFile.write(newHeader)
                targetFile.write(strHttp)
    ######################
    # Check TV Channel
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
                newHeader = x[:10] + groupString + x[index:]
                strHttp = next(originalFile)
                if strHttp.startswith("http") != True:
                    newHeader += strHttp
                    strHttp = next(originalFile)
                targetFile.write(newHeader)
                targetFile.write(strHttp)
                break

targetFile.close()
originalFile.close()
movieListFile.close()
