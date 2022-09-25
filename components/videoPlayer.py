import time
import vlc

def PlayVideo(videoURL):
    media = vlc.MediaPlayer(videoURL)
    media.play()
    time.sleep(5)
    while media.is_playing():
        time.sleep(1)
    media.stop()
    
