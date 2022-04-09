import json
import praw
import requests
import random
import pymsgbox as pg
import pyperclip as clip

BOTNAME = "Redditor"

# Official Redgifs search link
# https://api.redgifs.com/v2/gifs/search?search_text=anime

uri = "https://api.redgifs.com/v2/"
olduri = "https://api.redgifs.com/v1/"

def getJSON(searchgifs: str):
    return requests.get(f"{uri}gifs/search?search_text={searchgifs}&count=10&order=trending").json()

def getAllTags():
    cateogary = requests.get(f'{olduri}tags').json()["tags"]
    return cateogary[random.randint(0, len(cateogary))]["name"]

def getVideo(tag: str):
    redgifsJSON = getJSON(tag)
    gifs = redgifsJSON['gifs']
    giff = []
    for gif in gifs:
        giff.append(f'{gif["urls"]["hd"]}')
    if len(giff) <= 1:
        print("Please Try to Run the Program Again as this tym the API returned nothing to post on Reddit")
    link = str(str(str(giff[0]).replace("thumbs2.", "")).replace(
        "com/", "com/watch/")).replace(".mp4", "")
    clip.copy(link)
    return link


def openAndPost(title: str, message: str, textMSG: str = None):
    with open("client-secret.json", "r") as f:
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
        if textMSG != None:
            subreddit.submit(textMSG, url=message, nsfw=True)
        else:
            subreddit.submit(title, url=message, nsfw = True)


if __name__ == "__main__":
    AIORNOT = pg.confirm(f"Do you Want {BOTNAME} to Publish Post on Reddit??", BOTNAME, buttons=[
                         "Yes", "No"])
    if AIORNOT.lower() == 'yes':
        tag = getAllTags()
        videoURL = getVideo(tag)
        pg.alert(f'{BOTNAME} is uploading video with Cateogary {tag} with a Video URL of \n {videoURL}')
        openAndPost(tag, videoURL)
    elif AIORNOT.lower() == 'no':
        print('--------------------------Auto Poster on Reddit ( NSFW )--------------------------')
        print('     NOTE: Please do check on the Internet that whatenver cateogary you enter should exist on redgifs')
        cateogary = input("Enter the Cateogary to search and Post on Reddit : ")
        videoURL = getVideo(cateogary)
        print(
            f'Posting Video with URL {videoURL} which is under Cateogary {cateogary}')
        mess = input("Enter the Message You Want to post with it : ")
        openAndPost(cateogary, videoURL, mess)
    else:
        pg.alert(f"The {BOTNAME} was asked to abort.")