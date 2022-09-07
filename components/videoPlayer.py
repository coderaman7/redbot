import time
import vlc

def PlayVideo(videoURL):
    media = vlc.MediaPlayer(videoURL)
    try:
        media.play()
        time.sleep(5)
        while media.is_playing():
            time.sleep(1)
    except:
        media.stop()
