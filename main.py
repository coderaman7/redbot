import json
import os
from Providers.Redgifs import Redgifs
import pymsgbox as pg
import pyperclip as clip
from GraphicalElements.OptionsMenu import GetUserTag

with open('config.json', 'r') as f:
    config = json.load(f)


def PostOnRedgifs():
    option = pg.confirm(
        f"Do you want {config['Bot Name']} to Upload on you Behalf??", f'Posting on Reddit : {config["Bot Name"]}', buttons=["Yes", "No", "From Reddit??"])
    if str(option).lower() == 'yes':
        tag = Redgifs.RedGifs.getBestTag(Redgifs.RedGifs.getAllTags())
        videoURL = Redgifs.RedGifs.GetFromRedgifs(tag)
        wantToPlay = pg.confirm("Want to Play the Video??", f'Want to Play the Video Under Cateogary of {tag}', buttons=['Yes', 'No'])
        if str(wantToPlay).lower() == 'yes':
            pg.alert("It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
        elif str(wantToPlay).lower() == 'no':
            clip.copy("")
        Redgifs.RedGifs.openAndPost(TitleOfThePost, videoURL)
    elif str(option).lower() == 'no':
        GetUserTag(Redgifs.RedGifs.getAllTags())
        tag = clip.paste()
        print(tag)
        want = 'Refresh'
        while want == "Refresh":
            videoURL = Redgifs.RedGifs.GetFromRedgifs(tag)
            wantToPlay = pg.confirm(
                "Want to Play the Video??", f'Want to Play the Video Under Cateogary of {tag}', buttons=['Yes', 'No', "Refresh"])
            if str(wantToPlay).lower() == 'yes':
                pg.alert(
                    "It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
            elif str(wantToPlay).lower() == 'no':
                clip.copy("")
            want = wantToPlay
        TitleOfThePost = pg.prompt(
            "Enter the Title of the Post", "Enter the Title of the Post")
        Redgifs.RedGifs.openAndPost(TitleOfThePost, videoURL)
    elif str(option).lower() == 'from reddit??':
        print('Posting on Reddit using Reddit Service')
    else:
        pg.alert(f"{config['Bot Name']} was exited Abnormally")


if __name__ == "__main__":
    PostOnRedgifs()