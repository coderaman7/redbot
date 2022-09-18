import os
import requests
import pyperclip as clip
import random
import json
import praw
from GraphicalElements.OptionsMenu import GetRedditSub
from praw.exceptions import RedditAPIException
import pymsgbox as pg

from GraphicalElements.OptionsMenu import GetRedditTag

from Providers.Reddit import Reddit

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
            if int(tag["count"]) >= 5000:
                gifContent.append(tag["name"])

        # return all the tags sorted based on the alphabets 
        return sorted(gifContent)


    # Get all the videos based on tags 
    def GetFromRedgifs(userQuery: str):

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

        
        # Get all the links from the posted links 
        currentPath = RedGifs.RedgifsHome()
        try:
            with open("Posted.txt", 'r') as f:
                data = f.readlines()
        except:
            with open("Posted.txt", 'w') as f:
                f.write("")
        finally:
            with open("Posted.txt", 'r') as f:
                data = f.readlines()
        RedGifs.home(currentPath)

        # Generate the links and copy to clipboard and return it
        isdiffrent = False
        gifff = ""
        while isdiffrent == False:
            linkGen = giff[random.randint(0, len(giff))]
            link = str(str(str(linkGen).replace("thumbs2.", "")).replace(
                "com/", "com/watch/")).replace(".mp4", "")
            if link in data:
                isdiffrent = False
            else:
                gifff = link
                isdiffrent = True

        return gifff, linkGen


    # Module to Post on Reddit with or without crosspost 
    def openAndPost(title, message, crossPost = False, toPromote = ""):

        # open the config file
        with open('config.json', 'r') as f:
            config = json.load(f)

        currentPath = RedGifs.RedgifsHome()
        try:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        except FileNotFoundError:
            Reddit.Reddit.createRedditApp(config)
        finally:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        RedGifs.home(currentPath)

        # Login to Reddit using api 
        reddit = praw.Reddit(client_id=creds['client_id'],
                            client_secret=creds['client_secret'],
                            user_agent=creds['user_agent'],
                            redirect_uri=creds['redirect_uri'],
                            refresh_token=creds['refresh_token'])

        # getting all the subreddits from Reddit 
        subreddits = RedGifs.GetRedditTags()

        # Get the Subreddits 
        GetRedditSub(subreddits)
        subreddits = str(clip.paste()).split("+")[:-1]
        if crossPost == False:
            for i in subreddits:
                subreddit = reddit.subreddit(i)
                reddit.validate_on_submit = True
                try:
                    with open("bannedSubreddits.txt", 'r') as f:
                        subreds = f.readlines()
                except FileNotFoundError:
                    with open("bannedSubreddits.txt", 'w') as f:
                        f.write("")
                finally:
                    with open("bannedSubreddits.txt", 'r') as f:
                        subreds = f.readlines()
                if f"{i}\n" not in subreds:
                    try:
                        subreddit.submit(title, url=message, nsfw=True)
                        print(f"Successfully Posted in {i}")
                    except RedditAPIException:
                        with open("bannedSubreddits.txt", "a") as f:
                            f.write(f"{i}\n")
                else:
                    print(f"Skipped Sub Reddit {i} because it is BlackListed")
                # print(title, message)
        if crossPost == True:
            subredditt = reddit.subreddit(toPromote)
            submitID = subredditt.submit(title, url=message, nsfw=True)
            submitionn = reddit.submission(submitID)
            for i in subreddits:
                try:
                    with open("noCrossPosting.txt", 'r') as f:
                        subreds = f.readlines()
                except FileNotFoundError:
                    with open("noCrossPosting.txt", 'w') as f:
                        f.write("")
                finally:
                    with open("noCrossPosting.txt", 'r') as f:
                        subreds = f.readlines()
                if f"{i}\n" not in subreds:
                    try:
                        cross_Post = submitionn.crosspost(
                            i, nsfw=True, send_replies=False)
                        print(f"Successfully Cross Posted in {i}")
                    except RedditAPIException as e:
                        with open("noCrossPosting.txt", "a") as f:
                            f.write(f"{i}\n")
                        try:
                            with open("errors.txt", "r") as f:
                                errors = f.readlines()
                        except FileNotFoundError:
                            with open("errors.txt", "w") as f:
                                f.write("")
                        finally:
                            with open("errors.txt", "r") as f:
                                errors = f.readlines()

                        if f"{e.error_type}\n" not in errors:
                            with open("errors.txt", "a") as f:
                                f.write(f"{e.error_type}\n")
                        else:
                            subreddit = reddit.subreddit(i)
                            reddit.validate_on_submit = True
                            try:
                                with open("bannedSubreddits.txt", 'r') as f:
                                    subreds = f.readlines()
                            except FileNotFoundError:
                                with open("bannedSubreddits.txt", 'w') as f:
                                    f.write("")
                            finally:
                                with open("bannedSubreddits.txt", 'r') as f:
                                    subreds = f.readlines()
                            if f"{i}\n" not in subreds:
                                try:
                                    subreddit.submit(title, url=message, nsfw=True)
                                    print(f"Successfully Posted in {i}")
                                except RedditAPIException:
                                    with open("bannedSubreddits.txt", "a") as f:
                                        f.write(f"{i}\n")
                            else:
                                print(f"Skipped Sub Reddit {i} because it is BlackListed")
                else:
                    print(f"Skipped Sub Reddit {i} because it is BlackListed")
    # Module to Post on Reddit with or without crosspost 
    def openAndPost(title, message, crossPost = False, toPromote = ""):

        # open the config file
        with open('config.json', 'r') as f:
            config = json.load(f)

        currentPath = RedGifs.RedgifsHome()
        try:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        except FileNotFoundError:
            Reddit.Reddit.createRedditApp(config)
        finally:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        RedGifs.home(currentPath)

        # Login to Reddit using api 
        reddit = praw.Reddit(client_id=creds['client_id'],
                            client_secret=creds['client_secret'],
                            user_agent=creds['user_agent'],
                            redirect_uri=creds['redirect_uri'],
                            refresh_token=creds['refresh_token'])

        # getting all the subreddits from Reddit 
        subreddits = RedGifs.GetRedditTags()

        # Get the Subreddits 
        GetRedditSub(subreddits)
        subreddits = str(clip.paste()).split("+")[:-1]
        if crossPost == False:
            for i in subreddits:
                subreddit = reddit.subreddit(i)
                reddit.validate_on_submit = True
                try:
                    with open("bannedSubreddits.txt", 'r') as f:
                        subreds = f.readlines()
                except FileNotFoundError:
                    with open("bannedSubreddits.txt", 'w') as f:
                        f.write("")
                finally:
                    with open("bannedSubreddits.txt", 'r') as f:
                        subreds = f.readlines()
                if f"{i}\n" not in subreds:
                    try:
                        subreddit.submit(title, url=message, nsfw=True)
                        print(f"Successfully Posted in {i}")
                    except RedditAPIException:
                        with open("bannedSubreddits.txt", "a") as f:
                            f.write(f"{i}\n")
                else:
                    print(f"Skipped Sub Reddit {i} because it is BlackListed")
                # print(title, message)
        if crossPost == True:
            subredditt = reddit.subreddit(toPromote)
            submitID = subredditt.submit(title, url=message, nsfw=True)
            submitionn = reddit.submission(submitID)
            for i in subreddits:
                try:
                    with open("noCrossPosting.txt", 'r') as f:
                        subreds = f.readlines()
                except FileNotFoundError:
                    with open("noCrossPosting.txt", 'w') as f:
                        f.write("")
                finally:
                    with open("noCrossPosting.txt", 'r') as f:
                        subreds = f.readlines()
                if f"{i}\n" not in subreds:
                    try:
                        cross_Post = submitionn.crosspost(
                            i, nsfw=True, send_replies=False)
                        print(f"Successfully Cross Posted in {i}")
                    except RedditAPIException as e:
                        with open("noCrossPosting.txt", "a") as f:
                            f.write(f"{i}\n")
                        try:
                            with open("errors.txt", "r") as f:
                                errors = f.readlines()
                        except FileNotFoundError:
                            with open("errors.txt", "w") as f:
                                f.write("")
                        finally:
                            with open("errors.txt", "r") as f:
                                errors = f.readlines()

                        if f"{e.error_type}\n" not in errors:
                            with open("errors.txt", "a") as f:
                                f.write(f"{e.error_type}\n")
                        else:
                            subreddit = reddit.subreddit(i)
                            reddit.validate_on_submit = True
                            try:
                                with open("bannedSubreddits.txt", 'r') as f:
                                    subreds = f.readlines()
                            except FileNotFoundError:
                                with open("bannedSubreddits.txt", 'w') as f:
                                    f.write("")
                            finally:
                                with open("bannedSubreddits.txt", 'r') as f:
                                    subreds = f.readlines()
                            if f"{i}\n" not in subreds:
                                try:
                                    subreddit.submit(title, url=message, nsfw=True)
                                    print(f"Successfully Posted in {i}")
                                except RedditAPIException:
                                    with open("bannedSubreddits.txt", "a") as f:
                                        f.write(f"{i}\n")
                            else:
                                print(f"Skipped Sub Reddit {i} because it is BlackListed")
                else:
                    print(f"Skipped Sub Reddit {i} because it is BlackListed")


    # Module to Post on Reddit with or without crosspost 
    def openAndPostText(title, message):

        # open the config file
        with open('config.json', 'r') as f:
            config = json.load(f)

        currentPath = RedGifs.RedgifsHome()
        try:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        except FileNotFoundError:
            Reddit.Reddit.createRedditApp(config)
        finally:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        RedGifs.home(currentPath)

        # Login to Reddit using api 
        reddit = praw.Reddit(client_id=creds['client_id'],
                            client_secret=creds['client_secret'],
                            user_agent=creds['user_agent'],
                            redirect_uri=creds['redirect_uri'],
                            refresh_token=creds['refresh_token'])

        # getting all the subreddits from Reddit 
        subreddits = RedGifs.GetRedditTags()

        # Get the Subreddits 
        GetRedditSub(subreddits)
        subreddits = str(clip.paste()).split("+")[:-1]
        for i in subreddits:
            subreddit = reddit.subreddit(i)
            reddit.validate_on_submit = True
            try:
                with open("noTextPost.txt", 'r') as f:
                    subreds = f.readlines()
            except FileNotFoundError:
                with open("noTextPost.txt", 'w') as f:
                    f.write("")
            finally:
                with open("noTextPost.txt", 'r') as f:
                    subreds = f.readlines()
            if f"{i}\n" not in subreds:
                try:
                    subreddit.submit(title, selftext=message, nsfw=False)
                    print(f"Successfully Posted in {i}")
                except RedditAPIException:
                    if len(subreddits) != 0:
                        with open("noTextPost.txt", "a") as f:
                            f.write(f"{i}\n")
            else:
                print(f"Skipped Sub Reddit {i} because it is BlackListed")
            # print(title, message)
            

    def getBestTag(tags: list):
        return tags[random.randint(0, len(tags)-(len(tags)/2))]


    # Get all the Subreddit's a user is in 
    def GetRedditTags():

        # open the config file
        with open('config.json', 'r') as f:
            config = json.load(f)

        # Try and open the reddit secret file and if not exist then create 
        currentPath = RedGifs.RedgifsHome()
        try:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        except FileNotFoundError:
            Reddit.Reddit.createRedditApp(config)
            # pass
        finally:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)

        # login to reddit 
        reddit = praw.Reddit(client_id=creds['client_id'],
                             client_secret=creds['client_secret'],
                             user_agent=creds['user_agent'],
                             redirect_uri=creds['redirect_uri'],
                             refresh_token=creds['refresh_token'])
        
        # get and sort all the subreddits and return the subreddit's
        my_subs = [
            subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
        my_subs.sort()
        finalSubreddits, finalSubreds = [], []
        RedGifs.home(currentPath)
        try:
            with open("bannedSubreddits.txt", 'r') as f:
                subreds = f.readlines()
        except FileNotFoundError:
            with open("bannedSubreddits.txt", 'w') as f:
                f.write("")
        finally:
            with open("bannedSubreddits.txt", 'r') as f:
                subreds = f.readlines()
        try:
            with open("noCrossPosting.txt", 'r') as f:
                subreds = f.readlines()
        except FileNotFoundError:
            with open("noCrossPosting.txt", 'w') as f:
                f.write("")
        finally:
            with open("noCrossPosting.txt", 'r') as f:
                noCrosPost = f.readlines()
        for i in my_subs:
            if f'{i}\n' not in subreds:
                finalSubreddits.append(i)
        for i in finalSubreddits:
            if f'{i}\n' not in noCrosPost:
                finalSubreds.append(i)
        return finalSubreds


    # Get gifs and title from a subreddit
    def GetFromRedditGif(subReddit: str):

        # get the json from a subreddit 
        giflist = requests.get(
            f"https://www.reddit.com/r/{subReddit}/new/.json", headers={'User-agent': 'GetTheData'}).json()['data']['children']

        # store all the gifs and title in deffrent list and return a random gif and title 
        gif, title = [], []
        for gifs in giflist:
            try:
                title.append(gifs["data"]["title"])
                gif.append(gifs["data"]["url_overridden_by_dest"])
            except KeyError:
                pass
        isdiffrent = False
        giff, titlef = "", ""

        # keeping in mind that the generated link is not repeated 
        currentPath = RedGifs.RedgifsHome()
        try:
            with open("Posted.txt", 'r') as f:
                data = f.readlines()
        except:
            with open("Posted.txt", 'w') as f:
                f.write("")
        finally:
            with open("Posted.txt", 'r') as f:
                data = f.readlines()
        RedGifs.home(currentPath)

        # If No Media found then exit 
        if len(title) == 0:
            pg.alert(f"Error! Not a single Media found in {subReddit}")
            exit()

        # Else just select a random video from it and return it
        while isdiffrent == False:
            randomNumber = random.randint(0, len(gif)-1)
            randomGif = gif[randomNumber]
            try:
                VideoURL = str(giflist[randomNumber]["data"]["media"]["oembed"]["thumbnail_url"]).replace(
                    "-mobile.jpg", ".mp4")
            except:
                VideoURL = ""
            if randomGif in data:
                isdiffrent = False
            else:
                clip.copy(randomGif)
                giff = randomGif
                titlef = title[randomNumber]
                isdiffrent = True
        return giff, titlef, VideoURL

    # change to the reddit secret api location 
    def RedgifsHome():
        
        # get the current location of the script 
        currentPath = os.getcwd()

        # Move to the dezired location 
        path = os.path.join(os.getcwd(), "Providers", "Reddit")
        os.chdir(path)

        # now return the current location 
        return currentPath

    
    # Move back to the original location 
    def home(currentPath: str):
        os.chdir(currentPath)

    def UploadImages(crossPost, message, title, toPromote):
        # open the config file
        with open('config.json', 'r') as f:
            config = json.load(f)

        currentPath = RedGifs.RedgifsHome()
        try:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        except FileNotFoundError:
            Reddit.Reddit.createRedditApp(config)
        finally:
            with open("reddit-secret.json", "r") as f:
                creds = json.load(f)
        RedGifs.home(currentPath)

        # Login to Reddit using api
        reddit = praw.Reddit(client_id=creds['client_id'],
                             client_secret=creds['client_secret'],
                             user_agent=creds['user_agent'],
                             redirect_uri=creds['redirect_uri'],
                             refresh_token=creds['refresh_token'])

        # getting all the subreddits from Reddit
        subreddits = RedGifs.GetRedditTags()

        # Get the Subreddits
        GetRedditSub(subreddits)
        subreddits = str(clip.paste()).split("+")[:-1]
        if crossPost == False:
            for i in subreddits:
                subreddit = reddit.subreddit(i)
                reddit.validate_on_submit = True
                try:
                    with open("bannedSubreddits.txt", 'r') as f:
                        subreds = f.readlines()
                except FileNotFoundError:
                    with open("bannedSubreddits.txt", 'w') as f:
                        f.write("")
                finally:
                    with open("bannedSubreddits.txt", 'r') as f:
                        subreds = f.readlines()
                if f"{i}\n" not in subreds:
                    try:
                        subreddit.submit_gallery(title, message)
                        print(f"Successfully Posted in {i}")
                    except RedditAPIException as e:
                        # with open("bannedSubreddits.txt", "a") as f:
                        #     f.write(f"{i}\n")
                        print(e)
                else:
                    print(f"Skipped Sub Reddit {i} because it is BlackListed")
                # print(title, message)
        else:
            subredditt = reddit.subreddit(toPromote)
            submitID = subredditt.submit(title, url=message, nsfw=True)
            submitionn = reddit.submission(submitID)
            for i in subreddits:
                try:
                    with open("noCrossPosting.txt", 'r') as f:
                        subreds = f.readlines()
                except FileNotFoundError:
                    with open("noCrossPosting.txt", 'w') as f:
                        f.write("")
                finally:
                    with open("noCrossPosting.txt", 'r') as f:
                        subreds = f.readlines()
                if f"{i}\n" not in subreds:
                    try:
                        cross_Post = submitionn.crosspost(
                            i, nsfw=True, send_replies=False)
                        print(f"Successfully Cross Posted in {i}")
                    except RedditAPIException as e:
                        with open("noCrossPosting.txt", "a") as f:
                            f.write(f"{i}\n")
                        try:
                            with open("errors.txt", "r") as f:
                                errors = f.readlines()
                        except FileNotFoundError:
                            with open("errors.txt", "w") as f:
                                f.write("")
                        finally:
                            with open("errors.txt", "r") as f:
                                errors = f.readlines()

                        if f"{e.error_type}\n" not in errors:
                            with open("errors.txt", "a") as f:
                                f.write(f"{e.error_type}\n")
                        else:
                            print(
                                f"Skipped Sub Reddit {i} because it's error is not handled")
                else:
                    print(f"Skipped Sub Reddit {i} because it is BlackListed")

#     def getRedGifsVideos(self):
#         print(requests.get('https://api.redgifs.com/v1/me/collections'))

# RedGifs.getRedGifsVideos("")
# dataUrl = "https://www.redgifs.com/users/shawmir/collections/3c13a0673f"
# RedGifs.GetRedditTags()