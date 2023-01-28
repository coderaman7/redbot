import requests
import random
import json
import pymsgbox as pg

from Providers.Reddit.Reddit import RedgifsHome, checkOrCreateAFile, checkOrCreatePostedFile, home

# Official Redgifs search link
# https://api.redgifs.com/v2/gifs/search?search_text=anime


class RedGifs:

    # Get All the Tags of Redgifs
    def getAllTags():

        # old version of Redgifs API
        olduri = "https://api.redgifs.com/v1/"

        # get all the Redgifs Tags and select only tags
        cateogary = requests.get(f'{olduri}tags').json()["tags"]
        gifContent = []

        # filter all the tags who are used for over more than 5000 videos
        for tag in cateogary:
            if int(tag["count"]) >= 10000:
                gifContent.append(tag["name"])

        # return all the tags sorted based on the alphabets
        return sorted(gifContent)

    # Get all the videos based on tags

    def GetFromRedgifs(userQuery: str) -> str:

        with open('config.json', 'r') as f:
            config = json.load(f)

        # new redgifs api
        newuri = "https://api.redgifs.com/v2/"

        # get the videos based on tags
        Data = requests.get(
            f"{newuri}gifs/search?search_text={userQuery}&count=80&order=trending").json()
        gifs = Data['gifs']
        giff = []

        # get all the videos of quality hd
        for gif in gifs:
            giff.append(f'{gif["urls"]["hd"]}')

        # if nothing returned from redgifs then alert and quit
        if len(giff) <= 1:
            pg.alert(
                "Please Try to Run the Program Again as this tym the API returned nothing to post on Reddit", config["Bot Name"])
            exit()

        data = checkOrCreatePostedFile()

        # Generate the links and copy to clipboard and return it
        isdiffrent = False
        gif = ""
        while isdiffrent == False:
            link = giff[random.randint(0, len(giff))]
            if f'{link}\n' in data:
                isdiffrent = False
            else:
                gif = link
                isdiffrent = True
        id = str(gif).split(".")[2]
        return f'https://redgifs.{id}'.replace("com/", "com/watch/")


def getBestTag(tags: list) -> str:
    return tags[random.randint(0, int(len(tags)-1))]
