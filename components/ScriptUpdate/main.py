import requests
from BotVersion import Bot_Version as version


def GetUpdate():
    def printMSG(message):
        space = int(len(message)+6)
        preStoredMessage = 'A new Update is available use `git pull` command to update'
        if space <= len(preStoredMessage):
            space += 76-space
        firstMessgaeSpace = int((space-len(preStoredMessage))/2)*" "
        SecondMessageSpace = int((space-len(message))/2)*" "
        print("*"*(space+2))
        print(f"*{space*' '}*")
        print(f"*{firstMessgaeSpace}{preStoredMessage}{firstMessgaeSpace}*")
        print(f"*{SecondMessageSpace}{message}{SecondMessageSpace}*")
        print(f"*{space*' '}*")
        print("*"*(space+2))

    res = requests.get(
        "https://raw.githubusercontent.com/coderaman7/redbot/master/BotVersion.py").text
    LatestVersion = str(res).split("=")[1].replace(
        "'", "").replace('"', "").split(".")
    CurrentVersion = str(version).split(".")
    MajorUpdate, MinorUpdate, BugFixorPatches = False, False, False
    if (LatestVersion[0] > CurrentVersion[0]):
        MajorUpdate = True
    if (LatestVersion[1] > CurrentVersion[1]):
        MinorUpdate = True
    if (LatestVersion[2] > CurrentVersion[2]):
        BugFixorPatches = True

    if MajorUpdate is True:
        if MinorUpdate is True or BugFixorPatches is True:
            MinorUpdate, BugFixorPatches = False, False
        printMSG("It's a Major Update. Update it as soon as possible")
    if MinorUpdate is True:
        if BugFixorPatches is True:
            BugFixorPatches = False
        printMSG("It's a Minor Update. Update it as you will get new features")
    if BugFixorPatches is True:
        printMSG(
            "It's a Bug Fix. Try Updating it as It may be related with your Privacy")
