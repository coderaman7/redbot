import json
import os
import random
import re
import socket
import sys
import webbrowser
import praw
import pymsgbox as pg
from redvid import Downloader
import urllib.request
import requests
from Providers.Redgifs.Redgifs import RedGifs


class Reddit:

    # Delete all the comments which are below to a particular karma level 
    def DeleteCommentsBelowKarma(karma):

        # open the config file 
        with open('config.json', 'r') as f:
            config = json.load(f)

        # Open the Reddit api keys and read it 
        currentPath = RedGifs.RedgifsHome()
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
        RedGifs.home(currentPath)

        # login to reddit using api 
        reddit = praw.Reddit(client_id=creds['client_id'], client_secret=creds['client_secret'],
                             user_agent=creds['user_agent'], redirect_uri=creds['redirect_uri'], refresh_token=creds['refresh_token'])

        # get particular reddit account's reddit comments 
        user = reddit.redditor(config["username"])
        submissions = user.comments.new(limit=None)

        # iterate over each comments 
        for link in submissions:

            # check if it's below to the specified karma level then delete it else skip it 
            if link.score < karma:
                link.delete()

    # Delete all the Posts which are below to a particular karma level
    def DeletePostsBelowKarma(karma):

        # open the config file
        with open('config.json', 'r') as f:
            config = json.load(f)

        # Open the Reddit api keys and read it
        currentPath = RedGifs.RedgifsHome()
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
        RedGifs.home(currentPath)

        # login to reddit using api
        reddit = praw.Reddit(client_id=creds['client_id'], client_secret=creds['client_secret'],
                             user_agent=creds['user_agent'], redirect_uri=creds['redirect_uri'], refresh_token=creds['refresh_token'])
        
        # get particular reddit account's reddit Posts
        user = reddit.redditor(config["username"])
        submissions = user.submissions.new(limit=None)

        # iterate over each Posts
        for link in submissions:

            # check if it's below to the specified karma level then delete it else skip it
            if link.score < karma:
                link.delete()


    # Create the Reddit secret api file 

    def createRedditApp(config):

        # Get the Client ID if blank then exit
        clientID = pg.prompt(
            "Enter the Client ID ( Which is just below the Bot Name on Reddit Dev Dashboard )", "Collecting Client ID")
        if clientID == None:
            exit()
        
        # Get the Client Secret if blank then exit 
        clientSecret = pg.prompt(
            "Enter the Client Secret", "Collecting Client Secret")
        if clientSecret == None:
            exit()

        # get and generate refresh token 
        refreshToken = Reddit.main(clientID, clientSecret)

        # if there's no error then create a json and write it to the file 
        if refreshToken != 1:
            dataSet = {
                "client_id": clientID,
                "client_secret": clientSecret,
                "user_agent": config["Bot Name"],
                "redirect_uri": "http://localhost:8080",
                "refresh_token": refreshToken
            }
            with open("reddit-secret.json", 'w') as f:
                json.dump(dataSet, f, indent=4)

    # To Receive connection from the Reddit website itself while generating a refresh token 
    def receive_connection():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 8080))
        server.listen(1)
        client = server.accept()[0]
        server.close()
        return client

    # When generated the close the connection and send a 200 OK message 
    def send_message(client, message):
        client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
        client.close()

    # Start of the refresh token generation with all access to the Reddit Account 
    def main(clientID, ClientSecret):
        client_id = clientID
        client_secret = ClientSecret
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

        client = Reddit.receive_connection()
        data = client.recv(1024).decode("utf-8")
        param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
        params = {
            key: value for (key, value) in [token.split("=") for token in param_tokens]
        }

        if state != params["state"]:
            Reddit.send_message(
                client,
                f"State mismatch. Expected: {state} Received: {params['state']}",
            )
            return 1
        elif "error" in params:
            Reddit.send_message(client, params["error"])
            return 1

        refresh_token = reddit.auth.authorize(params["code"])
        Reddit.send_message(client, f"Refresh token: {refresh_token}")
        return refresh_token


def DownloadSavedVids():

    # open the config file
    with open('config.json', 'r') as f:
        config = json.load(f)

    currentPath = RedGifs.RedgifsHome()
    try:
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
    except FileNotFoundError:
        Reddit.createRedditApp(config)
    finally:
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
    RedGifs.home(currentPath)

    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'],
                         redirect_uri=creds['redirect_uri'],
                         refresh_token=creds['refresh_token'])
    

    out_filename = 'alreadyDownloaded.txt'
    try:
        os.mkdir("Reddit_Saved_Vods")
    except:
        pass
    curretLoc = os.getcwd()
    os.chdir("Reddit_Saved_Vods")

    try:
        with open(f"{out_filename}.txt", 'r') as f:
            pass
    except FileNotFoundError:
        with open(f"{out_filename}.txt", 'w') as f:
            pass
    finally:
        with open(f"{out_filename}.txt", 'r') as f:
            urls = f.readlines()

    with open(out_filename, 'w') as out_file:
        for item in reddit.user.me().saved(limit=None):
            submission = reddit.submission(id=item.id)
            try:

                url = submission.url
                if f'{url}\n' not in urls:

                    if str(url).split(".")[len(str(url).split("."))-1] == "gifv" or str(url).split(".")[len(str(url).split("."))-1] == "gif" or str(url).split(".")[len(str(url).split("."))-1] == "jpg":
                        nameOfVid = f'{submission.title}.mp4'.replace(" ", "_")
                        urllib.request.urlretrieve(url, nameOfVid)

                    elif str(url).split('/')[2] == 'redgifs.com' or str(url).split('/')[2] == "www.redgifs.com":
                        redgif_id = re.match(r'.*/(.*?)/?$', url).group(1)
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/90.0.4430.93 Safari/537.36',
                        }
                        content = requests.get(f'https://api.redgifs.com/v2/gifs/{redgif_id}', headers=headers).json()
                        video = requests.get(url=content['gif']["urls"]['hd'], headers=headers)
                        open(f"{str(submission.title).replace(' ', '_').replace('.', '').replace(',', '').replace('?', '').replace('/', '')}.mp4", 'wb').write(video.content)

                    elif str(url).split('/')[2] == "v.redd.it":
                        downloadRedVid = Downloader(max_q=True)
                        downloadRedVid.url = url
                        downloadRedVid.download()
                    else:
                        print(f'{url} got an error!! Please check if this is correct or not')
                    
                    out_file.write(f'{url}\n')

            except BaseException as e:
                print(e)

            submission.unsave()

    RedGifs.home(curretLoc)