import pymsgbox as pg
import os, json
import pyperclip as clip
from GraphicalElements.OptionsMenu import GetRedditTag, GetUserTag
from GraphicalElements.PostBox import PostBox
from Providers.Reddit.Reddit import DeleteCommentsBelowKarma, DeletePostsBelowKarma, GetGifFromReddit, GetSubreddits, PlayCustomizedVideo, PlayFromRedGifs, PostOnReddit, PostOnRedditFromURL, Reddit, askIfToPromote, checkForError, getURLSfromSaved, playfromImagurAndVeddit, removeFromSaved, writeInPostedDB
from Providers.Redgifs.Redgifs import RedGifs, getBestTag

from Providers.YouTube.main import parseVideo
from components.videoPlayer import PlayVideo
from BotVersion import Bot_Version
from components.ScriptUpdate.main import GetUpdate

# GetUpdate()

# Open config file for this bot else create
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    BotName = pg.prompt("What do you want to call this BOT",
                        "BOT Name", f"{os.getlogin()}'s BOT")
    username = pg.prompt("What's your Reddit Username",
                        "Reddit username")
    Version = Bot_Version
    dataToJSON = {"Bot Name": BotName, "Version": Version, "username": username, "nsfw": False}
    with open("config.json", "a") as f:
        json.dump(dataToJSON, f, indent=4)
finally:
    with open('config.json', 'r') as f:
        config = json.load(f)

options = [
    "Automate",
    "Post by Own",
    "Delete Post/Comments Based on Karma"
]

if config["nsfw"] == "false":
    options.pop(options.index("Automate"))

# User Options to choose from
option = pg.confirm(f"Reddit Automator", f'Posting on Reddit : {config["Bot Name"]}', buttons=options)

# If User wants to automate each and every process 
if str(option) == 'Automate':
    want = "Yes"
    while want == "Yes":
        tag = getBestTag(RedGifs.getAllTags())
        videoURL = RedGifs.GetFromRedgifs(tag)
        PlayFromRedGifs(videoURL)
        want = pg.confirm("Do you want to change the Video??", "Confirmation", buttons=["Yes", "No"])
    TitleOfThePost = f'#{tag}'
    PostOnReddit(title = TitleOfThePost, url = videoURL)
    writeInPostedDB(videoURL)

# Delete Posts or Comments based on Karma 
elif option == "Delete Post/Comments Based on Karma":

    # option to choose what to delete 
    secondOption = pg.confirm("What You Want To Delete??", f"Delete from Reddit", buttons=["Comments", "Posts"])

    # If Comment selected
    if secondOption == "Comments":
        karma = pg.prompt("Enter the Karma level to be maintained on Comments", "Delete Comments based on Karma") 
        try:
            DeleteCommentsBelowKarma(int(karma))
        except:
            pg.alert("Non-Integer Value Entered Program Exiting",config["Bot Name"])

    # If Post selected
    elif secondOption == "Posts":
        karma = pg.prompt("Enter the Karma level to be maintained on Posts", "Delete Posts based on Karma")
        try:
            DeletePostsBelowKarma(int(karma))
        except:
            pg.alert("Non-Integer Value Entered Program Exiting",config["Bot Name"])

elif option == "Post by Own":
    optionsForPostByOwn = [
        "Mine Video",
        "From Reddit",
        "Post from Saved Vids",
        "Post a Particular Link",
        "Post Images",
        "Post Text"
    ]

    if config["nsfw"] == "false":
        optionsForPostByOwn.pop(optionsForPostByOwn.index("Mine Video"))

    secondOption = pg.confirm("Posting to Reddit by Own", config["Bot Name"], buttons=optionsForPostByOwn)

    if secondOption == "Mine Video":
        GetUserTag(RedGifs.getAllTags(), "Select the Tag from the List")
        tag = clip.paste()
        want = 'Refresh'
        while want == "Refresh":
            videoURL = RedGifs.GetFromRedgifs(tag)
            wantToPlay = pg.confirm("Want to Play the Video??", f'Want to Play the Video Under Cateogary of {tag}', buttons=[
                                    'Yes', 'No', "Refresh"])
            PlayFromRedGifs(videoURL)
            want = wantToPlay
        TitleOfThePost = pg.prompt("Enter the Title of the Post", "Enter the Title of the Post")
        subredditToPromote, crossPost = askIfToPromote()
        PostOnReddit(title=TitleOfThePost, url=videoURL, crossPost=crossPost, toPromote=subredditToPromote)
        writeInPostedDB(videoURL)
    
    elif secondOption == "From Reddit":
        GetRedditTag(GetSubreddits(toPost=False))
        sub = clip.paste()
        checkForError("subreddit", sub)
        want = 'Refresh'
        while want == "Refresh":
            videoURL, title = GetGifFromReddit(sub)
            if str(videoURL).split("/")[2] in ['redgifs.com', 'www.redgifs.com', 'i.imgur.com', 'v.redd.it', 'i.redd.it']:
                if str(videoURL).split("/")[2] in ['redgifs.com', 'www.redgifs.com']:
                    PlayFromRedGifs(videoURL)
                elif str(videoURL).split("/")[2] in ['i.imgur.com', 'v.redd.it', 'i.redd.it']:
                    playfromImagurAndVeddit(videoURL)
            else:
                clip.copy(videoURL)
                pg.alert(f"Video can't be played in {config['Bot Name']}. It's Location has been copied to your clipboard.\nUse any browser's incognito mode to view the video.")
                pg.alert("Software is paused while you watch the video.\nClick OK when you've watched the video.")
            want = pg.confirm("Post this Video on Reddit or fetch another one??",
                              "Confirm Dialogue", buttons=["Post", "Refresh"])
        CustomTitle = pg.confirm(
            f"Want to Change the title : {title}", config["Bot Name"], buttons=["Yes", "NO"])
        if str(CustomTitle).lower() == "yes":
            CustomTitle = pg.prompt(
                "Enter the Title You Want to Enter", config["Bot Name"], default=title)
            TitleOfThePost = CustomTitle
        elif str(CustomTitle).lower() == 'no':
            TitleOfThePost = title
        else:
            exit()
        subredditToPromote, crossPost = askIfToPromote()
        PostOnReddit(title = TitleOfThePost, url=videoURL, crossPost=crossPost, toPromote=subredditToPromote)
        writeInPostedDB(videoURL)

    elif secondOption == "Post a Particular Link":
        videoURL = pg.prompt(f"Enter the URL", config["Bot Name"])
        PostOnRedditFromURL(videoURL)

    elif secondOption == "Post Text":
        PostBox("Enter the Text", False)
        text = str(clip.paste()).split('+')[0]
        TitleOfThePost = pg.prompt(f"Enter the Title for this video", config["Bot Name"])
        PostOnReddit(title=TitleOfThePost, message=text)

    elif secondOption == "Post Images":
        PostBox("Upload Images")
        TitleOfThePost, videoURL = str(clip.paste()).split("+")
        videoURL = videoURL.replace("(", "").replace(")", "").replace(" ", "").replace("'", "").split(",")
        images = []
        num = 0
        for i in videoURL:
            num += 1
            imageDict = {}
            imageDict["image_path"] = i
            images.append(imageDict)
        subredditToPromote, crossPost = askIfToPromote()
        PostOnReddit(images = images, title = TitleOfThePost, toPromote=subredditToPromote, crossPost=crossPost)

    elif secondOption == "Post from Saved Vids":
        urls, idOfPosts = getURLSfromSaved()
        urlIndex = 0
        toPost = "False"
        print("Got all the links from reddit")
        while toPost == "False":
            PlayCustomizedVideo(urls[urlIndex])
            toPost = pg.confirm("Do you want to Post this??", "Post it??", buttons=["True", "False"])
            if toPost == "False":
                urlIndex += 1
        PostOnRedditFromURL(urls[urlIndex])
        removeFromSaved(idOfPosts[urlIndex])

# elif option == "Download Saved Vids of Reddit":
#     DownloadSavedVids()

else:
    exit()
