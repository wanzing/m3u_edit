# My LG TV cannot process tv_channels.m3u due to the small size of RAM
# Need to remove unnecessary list from file and save it
# m3u file can be get from
# mains.vip:2086/get.php?username=8098306839&password=8412549&type=m3u_plus&output=mpegts
# No more VOD lists in m3u file
# TV Channels: US, UK, CA, SPORTS channels will be kept
# Movies will be kept except STAND-UP, BLACK, 3D, 4K, SPORTS REPLAYS, HD CAM
# The group name of the Movies are created from movie_list_new.m3u
# Refer to movielist_creator.py how to create movie_list_new.m3u file

keepList={"\"CA :","FRCAN", "GB :", "\"US :","US-720 :", "SPORTS :", "PREMIUM SPORTS", "MUSIC :", "UK EPL", "KR :"}
# groupArray= ["\"CANADIAN TV\",", "\"UK TV\",", "\"SPORTS TV\",", "\"USA TV\",", "\"NEW RELEASE\","]
removeList={"LOCALS\""," NFL", " NHL", "\"FOX SPORT", "BLEACHER",}


originalFile    = open("tv_channels_8098306839_plus.m3u", "r", encoding = "ISO-8859-1")
targetFile      = open("short_tv_new.m3u", "w", encoding = "ISO-8859-1")

targetFile.write("#EXTM3U\n")
# Don't check until lineCount reach to 2500. This is used just for speedup.
# Canadian channel starts from around line 2500 and previous channels are not necessary
originalFile.readline()[2500:]
for x in originalFile:
    ######################
    # Check TV Channel

    for t in keepList:
        index = x.find(t)
        if index != -1:
            for rlist in removeList:
                index = x.find(rlist)
                if index != -1:
                    # Skip 2 lines
                    next(originalFile)
                    next(originalFile)
                    break
            else:
                newHeader = x
                strHttp = next(originalFile)
                if strHttp.startswith("http") != True:
                    newHeader += strHttp
                    strHttp = next(originalFile)
                targetFile.write(newHeader)
                targetFile.write(strHttp)
                break

targetFile.close()
originalFile.close()
