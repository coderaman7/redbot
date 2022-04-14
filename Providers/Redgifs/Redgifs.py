import os
import requests
import pyperclip as clip
import random
import json
import praw
from GraphicalElements.OptionsMenu import GetRedditSub

# Official Redgifs search link
# https://api.redgifs.com/v2/gifs/search?search_text=anime

class RedGifs:

    def getAllTags():
        olduri = "https://api.redgifs.com/v1/"
        cateogary = requests.get(f'{olduri}tags').json()["tags"]
        gifContent = []
        for tag in cateogary:
            if int(tag["count"]) >= 5000:
                gifContent.append(tag["name"])
        return sorted(gifContent)

    def GetFromRedgifs(userQuery: str):
        newuri = "https://api.redgifs.com/v2/"
        Data = requests.get(
            f"{newuri}gifs/search?search_text={userQuery}&count=80&order=trending").json()
        gifs = Data['gifs']
        giff = []
        for gif in gifs:
            giff.append(f'{gif["urls"]["hd"]}')
        if len(giff) <= 1:
            print("Please Try to Run the Program Again as this tym the API returned nothing to post on Reddit")
        currentPath = RedGifs.RedgifsHome()
        with open("Posted.txt", 'r') as f:
            data = f.readlines()
        RedGifs.home(currentPath)
        isdiffrent = False
        gifff = ""
        while isdiffrent == False:
            linkGen = giff[random.randint(0, len(giff))]
            link = str(str(str(linkGen).replace("thumbs2.", "")).replace(
                "com/", "com/watch/")).replace(".mp4", "")
            if link in data:
                isdiffrent = False
            else:
                clip.copy(link)
                gifff = link
                isdiffrent = True
        return gifff

    def openAndPost(title: str, message: str):
        currentPath = RedGifs.RedgifsHome()
        with open("redgifs-secret.json", "r") as f:
            creds = json.load(f)
        RedGifs.home(currentPath)
        reddit = praw.Reddit(client_id=creds['client_id'],
                            client_secret=creds['client_secret'],
                            user_agent=creds['user_agent'],
                            redirect_uri=creds['redirect_uri'],
                            refresh_token=creds['refresh_token'])
        subreddits = str(creds["subreddits"]).split(",")
        GetRedditSub(subreddits)
        subreddits = str(clip.paste()).split("+")[:-1]
        for i in subreddits:
            subreddit = reddit.subreddit(i)
            reddit.validate_on_submit = True
            # subreddit.submit(title, url=message, nsfw=True)
            print(title, message)
            print(f"Successfully Posted in {i}")

    def getBestTag(tags: list):
        return tags[random.randint(0, len(tags))]

    def GetRedditTags():
        currentPath = RedGifs.RedgifsHome()
        with open("redgifs-secret.json", "r") as f:
            creds = json.load(f)
        RedGifs.home(currentPath)
        subreddits = str(creds["gifSubReddit"]).split(",")
        return list(subreddits)

    def GetFromRedditGif(subReddit: str):
        Data = requests.get(
            f"https://www.reddit.com/r/{subReddit}/new/.json", headers={'User-agent': 'GetTheData'}).json()
        giflist = Data['data']['children']
        gif = []
        title = []
        for gifs in giflist:
            title.append(gifs["data"]["title"])
            gif.append(gifs["data"]["url_overridden_by_dest"])
        isdiffrent = False
        giff = ""
        titlef = ""
        currentPath = RedGifs.RedgifsHome()
        with open("Posted.txt", 'r') as f:
            data = f.readlines()
        RedGifs.home(currentPath)
        while isdiffrent == False:
            randomNumber = random.randint(0, len(gif))
            randomGif = gif[randomNumber]
            if randomGif in data:
                isdiffrent = False
            else:
                clip.copy(randomGif)
                giff = randomGif
                titlef = title[randomNumber]
                isdiffrent = True
        return giff, titlef

    def RedgifsHome():
        currentPath = os.getcwd()
        path = os.path.join(os.getcwd(), "Providers", "Redgifs")
        os.chdir(path)
        return currentPath
    
    def home(currentPath: str):
        os.chdir(currentPath)
