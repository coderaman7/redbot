# Official Redgifs search link
# https://api.redgifs.com/v2/gifs/search?search_text=anime

import requests
import random

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
    return giff[0]

def default():
    tag = getAllTags()
    videoURL = main(tag)
    print(f'Redgif Cateogary = {tag}\n\nRedgif URL = {videoURL}')

default()