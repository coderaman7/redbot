import json
from Providers.Redgifs.PostOnReddit import PostOnReddit
import pymsgbox as pg
import os

# Discord Reddit Twitter YouTube Snapchat Instagram

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    BotName = pg.prompt("What do you want to call this BOT", "BOT Name", f"{os.getlogin()}'s BOT")
    Version = "1.0.2"
    dataToJSON = {"Bot Name": BotName, "Version": Version}
    with open("config.json", "a") as f:
        json.dump(dataToJSON, f)
finally:
    with open('config.json', 'r') as f:
        config = json.load(f)

if __name__ == "__main__":
    PostOnReddit()