import json
import os
from Providers.Redgifs import Redgifs
import pymsgbox as pg
import pyperclip as clip
from GraphicalElements.OptionsMenu import GetRedditTag, GetUserTag

with open('config.json', 'r') as f:
    config = json.load(f)


def PostOnReddit():
    option = pg.confirm(
        f"Do you want {config['Bot Name']} to Upload on you Behalf??", f'Posting on Reddit : {config["Bot Name"]}', buttons=["Yes", "No", "From Reddit??"])
    if str(option).lower() == 'yes':
        tag = Redgifs.RedGifs.getBestTag(Redgifs.RedGifs.getAllTags())
        videoURL = Redgifs.RedGifs.GetFromRedgifs(tag)
        wantToPlay = pg.confirm(
            "Want to Play the Video??", f'Want to Play the Video Under Cateogary of {tag}', buttons=['Yes', 'No'])
        if str(wantToPlay).lower() == 'yes':
            pg.alert(
                "It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
        elif str(wantToPlay).lower() == 'no':
            clip.copy("")
        else:
            pg.alert("Program Exited")
            exit()
        TitleOfThePost = tag
        Redgifs.RedGifs.openAndPost(TitleOfThePost, videoURL)
        currentPath = Redgifs.RedGifs.RedgifsHome()
        with open("Posted.txt", 'a') as f:
            f.write(f'{videoURL}\n')
        Redgifs.RedGifs.home(currentPath)
    elif str(option).lower() == 'no':
        GetUserTag(Redgifs.RedGifs.getAllTags())
        tag = clip.paste()
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
            elif str(wantToPlay).lower() == 'refresh':
                clip.copy("")
            else:
                exit()
            want = wantToPlay
        TitleOfThePost = pg.prompt(
            "Enter the Title of the Post", "Enter the Title of the Post")
        Redgifs.RedGifs.openAndPost(TitleOfThePost, videoURL)
        currentPath = Redgifs.RedGifs.RedgifsHome()
        with open("Posted.txt", 'a') as f:
            f.write(f'{videoURL}\n')
        Redgifs.RedGifs.home(currentPath)
    elif str(option).lower() == 'from reddit??':
        subreddit = Redgifs.RedGifs.GetRedditTags()
        GetRedditTag(subreddit)
        sub = clip.paste()
        want = 'Refresh'
        while want == "Refresh":
            videoURL, title = Redgifs.RedGifs.GetFromRedditGif(sub)
            wantToPlay = pg.confirm(
                f"Want to Play the Video with title {title}??", f'Want to Play the Video from Sub-Reddit {sub}', buttons=['Yes', 'No', "Refresh"])
            if str(wantToPlay).lower() == 'yes':
                pg.alert(
                    "It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
            elif str(wantToPlay).lower() == 'no':
                clip.copy("")
            want = wantToPlay
        TitleOfThePost = title
        Redgifs.RedGifs.openAndPost(TitleOfThePost, videoURL)
        currentPath = Redgifs.RedGifs.RedgifsHome()
        with open("Posted.txt", 'a') as f:
            f.write(f'{videoURL}\n')
        Redgifs.RedGifs.home(currentPath)
    else:
        pg.alert(f"{config['Bot Name']} was exited Abnormally")
