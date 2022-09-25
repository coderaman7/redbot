import json, os, random, re, socket, sys, webbrowser, praw
import pymsgbox as pg
from redvid import Downloader
import requests
from GraphicalElements.OptionsMenu import GetRedditSub, GetUserTag
from components.videoPlayer import PlayVideo
import pyperclip as clip
from praw.exceptions import RedditAPIException


class Reddit:

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


# def DownloadSavedVids():

#     reddit, config = readAndGetRedditAndBotConfig()

#     out_filename = 'alreadyDownloaded.txt'
#     try:
#         os.mkdir("Reddit_Saved_Vods")
#     except:
#         pass
#     curretLoc = os.getcwd()
#     os.chdir("Reddit_Saved_Vods")

#     urls = checkOrCreateAFile(out_filename)
#     with open(out_filename, 'a') as out_file:
#         for item in reddit.user.me().saved(limit=None):
#             submission = reddit.submission(id=item.id)
#             try:

#                 url = submission.url
#                 if f'{url}\n' not in urls:

#                     if str(url).split(".")[len(str(url).split("."))-1] == "gifv" or str(url).split(".")[len(str(url).split("."))-1] == "gif" or str(url).split(".")[len(str(url).split("."))-1] == "jpg":
#                         nameOfVid = f'{submission.title}.mp4'.replace(" ", "_")
#                         urllib.request.urlretrieve(url, nameOfVid)

#                     elif str(url).split('/')[2] == 'redgifs.com' or str(url).split('/')[2] == "www.redgifs.com":
#                         redgif_id = re.match(r'.*/(.*?)/?$', url).group(1)
#                         headers = {
#                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                             'Chrome/90.0.4430.93 Safari/537.36',
#                         }
#                         content = requests.get(
#                             f'https://api.redgifs.com/v2/gifs/{redgif_id}', headers=headers).json()
#                         video = requests.get(
#                             url=content['gif']["urls"]['hd'], headers=headers)
#                         open(
#                             f"{str(submission.title).replace(' ', '_').replace('.', '').replace(',', '').replace('?', '').replace('/', '')[:25]}.mp4", 'wb').write(video.content)

#                     elif str(url).split('/')[2] == "v.redd.it":
#                         downloadRedVid = Downloader(max_q=True)
#                         downloadRedVid.url = url
#                         downloadRedVid.download()
#                     else:
#                         print(
#                             f'{url} got an error!! Please check if this is correct or not')

#                     out_file.write(f'{url}\n')

#             except BaseException as e:
#                 print(e)
#             try:
#                 submission.unsave()
#             except:
#                 continue

#     RedGifs.home(curretLoc)

def getURLSfromSaved():
    reddit, config = readAndGetRedditAndBotConfig()
    urls = []
    ids = []
    for item in reddit.user.me().saved(limit=None):
        submission = reddit.submission(id=item.id)
        try:
            urls.append(submission.url)
            ids.append(submission.id)
        except:
            pass
    return urls, ids

def removeFromSaved(idOfPost):
    reddit, config = readAndGetRedditAndBotConfig()
    submission = reddit.submission(id=idOfPost)
    try:
        submission.unsave()
    except:
        pass

def PostOnRedditFromURL(url):
    reddit, config = readAndGetRedditAndBotConfig()
    TitleOfThePost = pg.prompt(
        f"Enter the Title for this video", config["Bot Name"])
    subredditToPromote, crossPost = askIfToPromote()
    PostOnReddit(title=TitleOfThePost, url=url, crossPost=crossPost, toPromote=subredditToPromote)
    writeInPostedDB(url)

def PlayFromRedGifs(url):
    redgif_id = re.match(r'.*/(.*?)/?$', url).group(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/90.0.4430.93 Safari/537.36',
    }
    content = requests.get(
        f'https://api.redgifs.com/v2/gifs/{str(redgif_id).lower()}', allow_redirects=True, headers=headers).json()
    print(redgif_id)
    video = requests.get(
        url=content['gif']["urls"]['hd'], headers=headers)
    open(
        f"{str('tempvid').replace(' ', '_').replace('.', '').replace(',', '').replace('?', '').replace('/', '')[:25]}.mp4", 'wb').write(video.content)
    choice = pg.confirm("Want to Play the Video??",
                        "Play it??", buttons=["Yes", "No"])
    if choice == "Yes":
        PlayVideo('tempvid.mp4')
    os.remove("tempVid.mp4")

def playfromImagurAndVeddit(url):
    downloadRedVid = Downloader(max_q=True)
    downloadRedVid.url = url
    downloadRedVid.download()
    PlayVideo(downloadRedVid.file_name)
    # os.remove(str(downloadRedVid).split("/")[:-1])
    print(str(downloadRedVid).split("/")[:-1])
    # To work on it

def checkForError(tocheckfor, dynamicVar):
    reddit, config = readAndGetRedditAndBotConfig()
    if tocheckfor == "subreddit":
        my_subs = [
            subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
        if dynamicVar in my_subs:
            return dynamicVar
        else:
            exit()

def PostOnReddit(title="Title Not Found", message="", url="", video = "", images = [], crossPost = False, toPromote = ""):
    reddit, config = readAndGetRedditAndBotConfig()
    GetRedditSub(GetSubreddits())
    subreddits = str(clip.paste()).split("+")[:-1]
    if crossPost == False:
        for i in subreddits:
            Poster(reddit, i, message, video, images, url, title)

    if crossPost == True:
        submitID = Poster(reddit, toPromote, message, video, images, url, title)
        submitionn = reddit.submission(submitID)
        for i in subreddits:
            currentPath = RedgifsHome()
            noURLPosts = checkOrCreateAFile("noURLPosts.txt")
            noMessagePosts = checkOrCreateAFile("noMessagePosts.txt")
            noImagePosts = checkOrCreateAFile("noImagePosts.txt")
            noVideoPosts = checkOrCreateAFile("noVideoPosts.txt")
            noCrossPosts = checkOrCreateAFile("noCrossPosts.txt")
            home(currentPath)
            if f"{i}\n" not in noURLPosts and f"{i}\n" not in noMessagePosts and f"{i}\n" not in noImagePosts and f"{i}\n" not in noVideoPosts:
                try:
                    submitionn.crosspost(i, nsfw=True, send_replies=False)
                    print(f"Successfully Cross Posted in {i}")
                except RedditAPIException as e:
                    currentPath = RedgifsHome()
                    with open("noCrossPosts.txt", "a") as f:
                        f.write(f"{i}\n")
                    errors = checkOrCreateAFile("errors.txt")
                    home(currentPath)
                    if f"{e.error_type}\n" not in errors:
                        currentPath = RedgifsHome()
                        with open("errors.txt", "a") as f:
                            f.write(f"Not Posted in {i} due to {e.error_type} error")
                        home(currentPath)
                    elif str(e.error_type) == "NO_CROSSPOSTS":
                        Poster(reddit, i, message, video, images, url, title)
            else:
                print(f"Skipped Sub Reddit {i} because it is has disabled the Cross Posting")

def Poster(reddit, subreddit, message="", video="", images=[], url="", title="Title Not Found"):
    subreddit = reddit.subreddit(subreddit)
    reddit.validate_on_submit = True
    currentPath = RedgifsHome()
    noURLPosts = checkOrCreateAFile("noURLPosts.txt")
    noMessagePosts = checkOrCreateAFile("noMessagePosts.txt")
    noImagePosts = checkOrCreateAFile("noImagePosts.txt")
    noVideoPosts = checkOrCreateAFile("noVideoPosts.txt")
    if f"{subreddit}\n" not in noURLPosts and f"{subreddit}\n" not in noMessagePosts and f"{subreddit}\n" not in noImagePosts and f"{subreddit}\n" not in noVideoPosts:
        submitElem = ""
        if message == "" and video == "" and len(images) == 0 and url != "":
            submitElem = subreddit.submit(title, url=url, nsfw=True)
        elif url == "" and video == "" and len(images) == 0 and message != "":
            try:
                submitElem = subreddit.submit(
                    title, selftext=message, nsfw=False)
            except:
                with open("noMessagePosts.txt", "a") as f:
                    f.write(f"{subreddit}\n")
        elif url == "" and message == "" and video == "" and len(images) != 0:
            try:
                submitElem = subreddit.submit_gallery(title, message)
            except:
                with open("noImagePosts.txt", "a") as f:
                    f.write(f"{subreddit}\n")
        elif url == "" and message == "" and len(images) == 0 and video != "":
            try:
                submitElem = subreddit.submit_video(title, video)
            except:
                with open("noVideoPosts.txt", "a") as f:
                    f.write(f"{subreddit}\n")
        print(f"Successfully Posted in {subreddit}")
        home(currentPath)
        return submitElem
    else:
        print(f"Skipped Sub Reddit {subreddit} because it is BlackListed")
    home(currentPath)

def GetSubreddits(toPost = True):
    reddit, config = readAndGetRedditAndBotConfig()
    my_subs = [
        subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
    my_subs.sort()
    if toPost == False:
        return my_subs
    finalSubreds = []
    currentPath = RedgifsHome()
    bannedSubreddits = checkOrCreateAFile("bannedSubreddits.txt")
    noCrossPosting = checkOrCreateAFile("noCrossPosting.txt")
    home(currentPath)
    for subreddit in my_subs:
        if f'{subreddit}\n' not in noCrossPosting and f'{subreddit}\n' not in bannedSubreddits:
            finalSubreds.append(subreddit)
    return finalSubreds


def GetGifFromReddit(subReddit: str):
    giflist = requests.get(
        f"https://www.reddit.com/r/{subReddit}/new/.json", headers={'User-agent': 'GetTheData'}).json()['data']['children']
    gifs = []
    titles = []
    for gifss in giflist:
        try:
            titles.append(gifss["data"]["title"])
            gifs.append(gifss["data"]["url_overridden_by_dest"])
        except KeyError:
            pass
    isdiffrent = False
    gif, title = "", ""
    data = checkOrCreatePostedFile()
    if len(titles) == 0:
        pg.alert(f"Error! Not a single Media found in {subReddit}")
        exit()
    while isdiffrent == False:
        randomGif = gifs[random.randint(0, len(gifs)-1)]
        if f'{randomGif}\n' in data:
            isdiffrent = False
        else:
            gif = randomGif
            title = titles[gifs.index(randomGif)]
            isdiffrent = True
    return gif, title

# change to the reddit secret api location 
def RedgifsHome():
    currentPath = os.getcwd()
    path = os.path.join(os.getcwd(), "Providers", "Reddit")
    os.chdir(path)
    try:
        os.mkdir("logs")
    except:
        pass
    finally:
        os.chdir(os.path.join(os.getcwd(), "logs"))
    return currentPath

# Move back to the original location 
def home(currentPath: str):
    os.chdir(currentPath)

def checkOrCreatePostedFile() -> str:
    currentPath = RedgifsHome()
    try:
        with open("Posted.txt", 'r') as f:
            data = f.readlines()
    except:
        with open("Posted.txt", 'w') as f:
            f.write("")
    finally:
        with open("Posted.txt", 'r') as f:
            data = f.readlines()
    home(currentPath)
    return data


def readAndGetRedditAndBotConfig():

    # open the config file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Open the Reddit api keys and read it
    currentPath = RedgifsHome()
    try:
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
    except FileNotFoundError:
        Reddit.createRedditApp(config)
    finally:
        with open("reddit-secret.json", "r") as f:
            creds = json.load(f)
    home(currentPath)

    # login to reddit using api
    reddit = praw.Reddit(client_id=creds['client_id'], client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'], redirect_uri=creds['redirect_uri'], refresh_token=creds['refresh_token'])
    return reddit, config

# Delete all the comments which are below to a particular karma level
def DeleteCommentsBelowKarma(karma):
    reddit, config = readAndGetRedditAndBotConfig()
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
    reddit, config = readAndGetRedditAndBotConfig()
    # get particular reddit account's reddit Posts
    user = reddit.redditor(config["username"])
    submissions = user.submissions.new(limit=None)
    # iterate over each Posts
    for link in submissions:
        # check if it's below to the specified karma level then delete it else skip it
        if link.score < karma:
            link.delete()


def checkOrCreateAFile(out_filename):
    try:
        with open(out_filename, 'r') as f:
            pass
    except FileNotFoundError:
        open(out_filename, 'w').write("")
    finally:
        with open(out_filename, 'r') as f:
            urls = f.readlines()
    return urls

def writeInPostedDB(url):
    currentPath = RedgifsHome()
    with open("Posted.txt", 'a') as f:
        f.write(f'{url}\n')
    home(currentPath)

def askIfToPromote():
    subredditToPromote = ""
    crossPost = False
    promotion = pg.confirm(
        "Do you want to Promote a Subreddit??", "Promotion", buttons=['Yes', 'No'])
    if promotion == 'Yes':
        GetUserTag(options=GetSubreddits(toPost=True),
                   title="Select the Subreddit to Promote")
        subredditToPromote = clip.paste()
        crossPost = True
    return subredditToPromote, crossPost


def PlayCustomizedVideo(url):
    if str(url).split('/')[2] in ['redgifs.com', 'www.redgifs.com']:
        PlayFromRedGifs(url)
    elif str(url).split('/')[2] in ['i.imgur.com', 'v.redd.it', 'i.redd.it']:
        try:
            playfromImagurAndVeddit(url)
        except:
            print("Video can't be played due to some error")

