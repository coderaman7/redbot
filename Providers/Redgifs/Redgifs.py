import os
import socket
import sys
import webbrowser
import requests
import pyperclip as clip
import random
import json
import praw
from GraphicalElements.OptionsMenu import GetRedditSub
from praw.exceptions import RedditAPIException
import pymsgbox as pg

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
        subreddits = RedGifs.GetRedditTags()
        GetRedditSub(subreddits)
        subreddits = str(clip.paste()).split("+")[:-1]
        for i in subreddits:
            subreddit = reddit.subreddit(i)
            reddit.validate_on_submit = True
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

    def getBestTag(tags: list):
        return tags[random.randint(0, len(tags))]

    def GetRedditTags():
        with open('config.json', 'r') as f:
            config = json.load(f)
        currentPath = RedGifs.RedgifsHome()
        try:
            with open("redgifs-secret.json", "r") as f:
                creds = json.load(f)
        except FileNotFoundError:
            clientID = pg.prompt("Enter the Client ID ( Which is just below the Bot Name on Reddit Dev Dashboard )", "Collecting Client ID")
            if clientID == None:
                exit()
            clientSecret = pg.prompt("Enter the Client Secret",
                                    "Collecting Client Secret")
            if clientSecret == None:
                exit()
            refreshToken = RedGifs.main(clientID, clientSecret)
            if refreshToken != 1:
                dataSet = {
                    "client_id": clientID,
                    "client_secret": clientSecret,
                    "user_agent": config["Bot Name"],
                    "redirect_uri": "http://localhost:8080",
                    "refresh_token": refreshToken
                }
                with open("redgifs-secret.json", 'w') as f:
                    json.dump(dataSet, f, indent=4)
        finally:
            with open("redgifs-secret.json", "r") as f:
                creds = json.load(f)
        reddit = praw.Reddit(client_id=creds['client_id'],
                             client_secret=creds['client_secret'],
                             user_agent=creds['user_agent'],
                             redirect_uri=creds['redirect_uri'],
                             refresh_token=creds['refresh_token'])
        my_subs = [
            subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
        my_subs.sort()
        RedGifs.home(currentPath)
        return my_subs

    def GetFromRedditGif(subReddit: str):
        Data = requests.get(
            f"https://www.reddit.com/r/{subReddit}/new/.json", headers={'User-agent': 'GetTheData'}).json()
        giflist = Data['data']['children']
        gif = []
        title = []
        for gifs in giflist:
            try:
                title.append(gifs["data"]["title"])
                gif.append(gifs["data"]["url_overridden_by_dest"])
            except KeyError:
                pass
        isdiffrent = False
        giff = ""
        titlef = ""
        currentPath = RedGifs.RedgifsHome()
        with open("Posted.txt", 'r') as f:
            data = f.readlines()
        RedGifs.home(currentPath)
        if len(title) == 0:
            pg.alert(f"Error! Not a single Media found in {subReddit}")
            exit()
        while isdiffrent == False:
            randomNumber = random.randint(0, len(gif)-1)
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
    

    def receive_connection():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        server.listen(1)
        client = server.accept()[0]
        server.close()
        return client


    def send_message(client, message):
        """Send message to client and close the connection."""
        print(message)
        client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
        client.close()


    def main(clientID, ClientSecret):
        """Provide the program's entry point when directly executed."""
        print(
            "Go here while logged into the account you want to create a token for: "
            "https://www.reddit.com/prefs/apps/"
        )
        print(
            "Click the create an app button. Put something in the name field and select the"
            " script radio button."
        )
        print("Put http://localhost:8080 in the redirect uri field and click create app")
        client_id = clientID
        client_secret = ClientSecret
        # client_id = pg.prompt(
        #     "Enter the client ID, it's the line just under Personal use script at the top: ",
        #     "Enter the client ID, it's the line just under Personal use script at the top: "
        # )
        # client_secret = pg.prompt(
        #     "Enter the client secret, it's the line next to secret: ",
        #     "Enter the client secret, it's the line next to secret: ")
        commaScopes = 'all'

        if commaScopes.lower() == "all":
            scopes = ["*"]
        else:
            scopes = commaScopes.strip().split(",")

        reddit = praw.Reddit(
            client_id=client_id.strip(),
            client_secret=client_secret.strip(),
            redirect_uri="http://localhost:8080",
            user_agent="praw_refresh_token_example",
        )
        state = str(random.randint(0, 65000))
        url = reddit.auth.url(scopes, state, "permanent")
        webbrowser.open_new(url)
        sys.stdout.flush()

        client = RedGifs.receive_connection()
        data = client.recv(1024).decode("utf-8")
        param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
        params = {
            key: value for (key, value) in [token.split("=") for token in param_tokens]
        }

        if state != params["state"]:
            RedGifs.send_message(
                client,
                f"State mismatch. Expected: {state} Received: {params['state']}",
            )
            return 1
        elif "error" in params:
            RedGifs.send_message(client, params["error"])
            return 1

        refresh_token = reddit.auth.authorize(params["code"])
        RedGifs.send_message(client, f"Refresh token: {refresh_token}")
        return refresh_token

    def home(currentPath: str):
        os.chdir(currentPath)
