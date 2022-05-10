import json
import pymsgbox as pg
import os
import pyperclip as clip
from GraphicalElements.OptionsMenu import GetRedditTag, GetUserTag
from Providers.Reddit.Reddit import Reddit
from Providers.Redgifs.Redgifs import RedGifs

BotVersion = "1.1.2"

# To Do for this Bot
# Discord Reddit Twitter YouTube Snapchat Instagram

# Open config file for this bot else create
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    BotName = pg.prompt("What do you want to call this BOT",
                        "BOT Name", f"{os.getlogin()}'s BOT")
    username = pg.prompt("What's your Reddit Username",
                        "Reddit username")
    Version = BotVersion
    dataToJSON = {"Bot Name": BotName, "Version": Version, "username": username}
    with open("config.json", "a") as f:
        json.dump(dataToJSON, f, indent=4)
finally:
    with open('config.json', 'r') as f:
        config = json.load(f)


# User Options to choose from
option = pg.confirm(f"Reddit NSFW Automator", f'Posting on Reddit : {config["Bot Name"]}', buttons=[
                    "Automate", "Post by Own", "Delete Post/Comments Based on Karma"])

# If User wants to automate each and every process 
if str(option) == 'Automate':
    tag = RedGifs.getBestTag(RedGifs.getAllTags())
    videoURL = RedGifs.GetFromRedgifs(tag)

    # Alert if User wants to see the vide ( which can't be changed )
    wantToPlay = pg.confirm("Want to Play the Video??", f'Want to Play the Video Under Cateogary of {tag}', buttons=['Yes', 'No'])
    if str(wantToPlay).lower() == 'yes':
        pg.alert("It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
    elif str(wantToPlay).lower() == 'no':
        clip.copy("")
    else:
        pg.alert("Program Exited")
        exit()

    # Title of the Post will be the Tag itself 
    TitleOfThePost = tag
    
    # Post on Reddit 
    RedGifs.openAndPost(TitleOfThePost, videoURL)

    # Change the Path and write the vedio url to a file so that next time that won't be uploaded on Reddit 
    currentPath = RedGifs.RedgifsHome()
    with open("Posted.txt", 'a') as f:
        f.write(f'{videoURL}\n')
    RedGifs.home(currentPath)


# Delete Posts or Comments based on Karma 
elif option == "Delete Post/Comments Based on Karma":

    # option to choose what to delete 
    secondOption = pg.confirm("What You Want To Delete??", f"Delete from Reddit", buttons=["Comments", "Posts"])

    # If Comment selected
    if secondOption == "Comments":
        karma = pg.prompt("Enter the Karma level to be maintained on Comments", "Delete Comments based on Karma") 
        try:
            integerKarma = int(karma)
            Reddit.DeleteCommentsBelowKarma(integerKarma)
        except:
            pg.alert("Non-Integer Value Entered Program Exiting",config["Bot Name"])

    # If Post selected
    elif secondOption == "Posts":
        karma = pg.prompt("Enter the Karma level to be maintained on Posts", "Delete Posts based on Karma")
        try:
            integerKarma = int(karma)
            Reddit.DeletePostsBelowKarma(integerKarma)
        except:
            pg.alert("Non-Integer Value Entered Program Exiting",config["Bot Name"])

elif option == "Post by Own":
    secondOption = pg.confirm("Posting to Reddit by Own", config["Bot Name"], buttons=[
                              "Mine Video", "From Reddit", "Post a Particular Link"])

    # If the User want to Customize each and every part of upload and mine the best video
    if secondOption == "Mine Video":

        # Get Tag from user and copy it to clipboard and paste it here so that we can use it for video fetching based on that tag
        GetUserTag(RedGifs.getAllTags(), "Select the Tag from the List")
        tag = clip.paste()
        want = 'Refresh'

        # while loop so that we can refresh the video urls and the user can get option to change video urls which is to be uploaded
        while want == "Refresh":
            videoURL = RedGifs.GetFromRedgifs(tag)
            wantToPlay = pg.confirm("Want to Play the Video??", f'Want to Play the Video Under Cateogary of {tag}', buttons=[
                                    'Yes', 'No', "Refresh"])
            if str(wantToPlay).lower() == 'yes':
                pg.alert(
                    "It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
            elif str(wantToPlay).lower() == 'no':
                clip.copy("")
            elif str(wantToPlay).lower() == 'refresh':
                clip.copy("")
            else:
                exit()
            want = wantToPlay

        # Option so that User can change the Title for the video and can customize it
        TitleOfThePost = pg.prompt(
            "Enter the Title of the Post", "Enter the Title of the Post")

        subredditToPromote = ""
        crossPost = False
        promotion = pg.confirm("Do you want to Promote a Subreddit??", "Promotion", buttons=['Yes', 'No'])
        if promotion == 'Yes':
            GetUserTag(options=RedGifs.GetRedditTags(), title="Select the Subreddit to Promote")
            subredditToPromote = clip.paste()
            crossPost = True


        # Post to Reddit
        RedGifs.openAndPost(TitleOfThePost, videoURL, crossPost=crossPost, toPromote=subredditToPromote)

        # Change the Path and write the vedio url to a file so that next time that won't be uploaded on Reddit
        currentPath = RedGifs.RedgifsHome()
        with open("Posted.txt", 'a') as f:
            f.write(f'{videoURL}\n')
        RedGifs.home(currentPath)
    
    # If User Wants to Grab a link from a Sub-Reddit
    elif secondOption == "From Reddit":

        # Get Tag from user and copy it to clipboard and paste it here so that we can use it for video fetching based on that tag
        subreddit = RedGifs.GetRedditTags()
        GetRedditTag(subreddit)
        sub = clip.paste()
        want = 'Refresh'

        # while loop so that we can refresh the video urls and the user can get option to change video urls which is to be uploaded
        while want == "Refresh":

            # Get Video Url and title and then strip it to make it a better video with SEO 
            videoURL, title = RedGifs.GetFromRedditGif(sub)
            Source = str(videoURL).split("/")[2]

            # If a user wants to play the video then copy the url to clipboard else clear clipboard 
            wantToPlay = pg.confirm(f"Want to Play the Video with title {title}?? \n\nSource = {Source}",
                                    f'Want to Play the Video from Sub-Reddit {sub}', buttons=['Yes', 'No', "Refresh"])
            if str(wantToPlay).lower() == 'yes':
                pg.alert(
                    "It's been already Copied to your Clipboard. Just Open any private Browser and watch it")
            elif str(wantToPlay).lower() == 'no':
                clip.copy("")
            want = wantToPlay

        # Option so that User can change the Title for the video and can customize it
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

        subredditToPromote = ""
        crossPost = False
        promotion = pg.confirm(
            "Do you want to Promote a Subreddit??", "Promotion", buttons=['Yes', 'No'])
        if promotion == 'Yes':
            GetUserTag(options=RedGifs.GetRedditTags(),
                       title="Select the Subreddit to Promote")
            subredditToPromote = clip.paste()
            crossPost = True

        # Post to Reddit
        RedGifs.openAndPost(TitleOfThePost, videoURL,
                            crossPost=crossPost, toPromote=subredditToPromote)

        # Change the Path and write the video url to a file so that next time that won't be uploaded on Reddit
        currentPath = RedGifs.RedgifsHome()
        with open("Posted.txt", 'a') as f:
            f.write(f'{videoURL}\n')
        RedGifs.home(currentPath)

    # If User Wants to Post a Particular Link to Reddit
    elif secondOption == "Post a Particular Link":

        # Get Video URL
        videoURL = pg.prompt(f"Enter the URL", config["Bot Name"])

        # Title for the Video
        TitleOfThePost = pg.prompt(
            f"Enter the Title for this video", config["Bot Name"])

        subredditToPromote = ""
        crossPost = False
        promotion = pg.confirm(
            "Do you want to Promote a Subreddit??", "Promotion", buttons=['Yes', 'No'])
        if promotion == 'Yes':
            GetUserTag(options=RedGifs.GetRedditTags(),
                       title="Select the Subreddit to Promote")
            subredditToPromote = clip.paste()
            crossPost = True

        # Post to Reddit
        RedGifs.openAndPost(TitleOfThePost, videoURL,
                            crossPost=crossPost, toPromote=subredditToPromote)

        # Change the Path and write the vedio url to a file so that next time that won't be uploaded on Reddit
        currentPath = RedGifs.RedgifsHome()
        with open("Posted.txt", 'a') as f:
            f.write(f'{videoURL}\n')
        RedGifs.home(currentPath)

else:
    exit()
