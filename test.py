# Official Redgifs search link
# https://api.redgifs.com/v2/gifs/search?search_text=anime

import requests
import random
import pyperclip as clip

uri = "https://api.redgifs.com/v2/"
olduri = "https://api.redgifs.com/v1/"


def getJSON(searchgifs: str):
    # searchgifs = input("Enter the Type of the GIFS you want : ")
    # return requests.get(f"https://api.redgifs.com/v2/gifs/search?search_text={searchgifs}&count=10&order=trending").json()
    return requests.get(f"{uri}gifs/search?search_text={searchgifs}&count=10&order=trending").json()

def getAllTags():
    cateogary = requests.get(f'{olduri}tags').json()["tags"]
    return cateogary[random.randint(0, len(cateogary))]["name"]

def main(tag: str):
    redgifsJSON = getJSON(tag)
    gifs = redgifsJSON['gifs']
    giff = []
    for gif in gifs:
        giff.append(f'{gif["urls"]["hd"]}')
    if len(giff) <= 1:
        print("Please Try to Run the Program Again as this tym the API returned nothing to post on Reddit")
    link = str(str(str(giff[0]).replace("thumbs2.", "")).replace("com/", "com/watch/")).replace(".mp4","")
    clip.copy(link)
    return link
    

def default():
    tag = getAllTags()
    videoURL = main(tag)
    print(f'Redgif Cateogary = {tag}\n\nRedgif URL = {videoURL}')

default()