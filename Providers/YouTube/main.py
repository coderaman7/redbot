
def parseVideo(videoURL):
    videoStripID = str(videoURL).split("/")
    try:
        if videoStripID[2] == "thumbs2.redgifs.com":
            return videoURL
        if videoStripID[2] in ["www.youtube.com", "youtu.be"]:
            print("In Development")
            exit()
    except IndexError:
        return videoURL
