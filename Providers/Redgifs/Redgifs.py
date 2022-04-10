import os
import requests
import pyperclip as clip
import random
import json
import praw

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
        linkGen = giff[random.randint(0, len(giff))]
        link = str(str(str(linkGen).replace("thumbs2.", "")).replace(
            "com/", "com/watch/")).replace(".mp4", "")
        clip.copy(linkGen)
        return link

    def openAndPost(title: str, message: str):
        path = os.path.join(os.getcwd(), "Providers", "Redgifs")
        os.chdir(path)
        with open("redgifs-secret.json", "r") as f:
            creds = json.load(f)
        reddit = praw.Reddit(client_id=creds['client_id'],
                            client_secret=creds['client_secret'],
                            user_agent=creds['user_agent'],
                            redirect_uri=creds['redirect_uri'],
                            refresh_token=creds['refresh_token'])
        subreddits = str(creds["subreddits"]).split(",")
        for i in subreddits:
            print(i)
            subreddit = reddit.subreddit(i)
            reddit.validate_on_submit = True
            subreddit.submit(title, url=message, nsfw=True)

    def getBestTag(tags: list):
        return tags[random.randint(0, len(tags))]

    def GetRedditTags():
        path = os.path.join(os.getcwd(), "Providers", "Redgifs")
        os.chdir(path)
        with open("redgifs-secret.json", "r") as f:
            creds = json.load(f)
        subreddits = str(creds["gifSubReddit"]).split(",")
        return list(subreddits)

    def GetFromRedditGif(subReddit: str):
        Data = requests.get(
            f"https://www.reddit.com/r/{subReddit}/new/.json").json()
        print(Data)
        gifs = Data['data']['children']
        print(len(gifs))
        exit()
        giff = []
        for gif in gifs:
            giff.append(f'{gif["urls"]["hd"]}')
        if len(giff) <= 1:
            print(
                "Please Try to Run the Program Again as this tym the API returned nothing to post on Reddit")
        linkGen = giff[random.randint(0, len(giff))]
        link = str(str(str(linkGen).replace("thumbs2.", "")).replace(
            "com/", "com/watch/")).replace(".mp4", "")
        clip.copy(linkGen)
        return link
