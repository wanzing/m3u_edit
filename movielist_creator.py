# This creator is to create base movie_list_new.m3u file
# movie_list.m3u file은 새로 저장한 tv_channels.m3u 과 비교해서
# 불필요한 파일들과 LG TV에서 지원하지 않는 keyword 등을 제거하고 group-title이 없는 
# 것들은 NEWLY ADDED group으로 할당한다.

groupString = "group-title=\"NEWLY ADDED\","

foundMatch  = 0
newEntry    = 0
vodStarted  = 0

newSourceFile= open("tv_channels.m3u", "r", encoding = "ISO-8859-1")
oldSourceFile  = open("movie_list.m3u", "r", encoding = "ISO-8859-1")
targetFile  = open("movie_list_new.m3u", "w", encoding = "ISO-8859-1")


for x in newSourceFile:
    # Reached to the beginning of VOD
    if x.find("#Real") == -1 and vodStarted == 0:
        continue
    else:
        vodStarted = 1
    # Reached to the beginning of Series
    if x.find("S01 E01") != -1:
        break

    strVLCOPT = strVLCOPTSrc = ""
    foundMatch  = 0
    if x.startswith("#EXTINF"):
        strHeader = x
        strHttp = next(newSourceFile)
        if strHttp.startswith("http") != True:
            # Check if it has "#EXTVLCOPT:network-caching=1000"
            # if yes, add it to the Header
            strHeader += strHttp
            strHttp = next(newSourceFile)

        for line in oldSourceFile:
            strHeaderSrc = line
            strHttpSrc = next(oldSourceFile)
            if strHttpSrc.startswith("http") != True:
                # Check if it has "#EXTVLCOPT:network-caching=1000"
                # if yes, add it to the Header
                strHeaderSrc += strHttpSrc
                strHttpSrc = next(oldSourceFile)

            if strHttp == strHttpSrc:
                # print("Found Match!")
                # New source has the same link as in the previous one
                # Write the header and link from the previous list that has a group-title(movie_list.m3u) to targetFile 
                targetFile.write(strHeaderSrc)
                targetFile.write(strHttpSrc)
                foundMatch = 1
                break
        if foundMatch == 0 :
            # print("No Match! Search from beginning!")
            newEntry += 1
            oldSourceFile.seek(0)
            # Check if it has group-title and remove it
            # Because some keywords are not supported by LG TV
            if strHeader.find("group-title") != -1:
                index = strHeader.rfind("\"")
            else:
                index = 8
            # Create new Header
            newHeader = strHeader[:10] + groupString + strHeader[index+2:]
            # Write the header and link from tv_channels.m3u to targetFile
            targetFile.write(newHeader)
            targetFile.write(strHttp)

print("Newly added movies: "+newEntry)
targetFile.close()
newSourceFile.close()
oldSourceFile.close()