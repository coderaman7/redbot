import json
from Providers.Redgifs.PostOnReddit import PostOnReddit

with open('config.json', 'r') as f:
    config = json.load(f)

if __name__ == "__main__":
    PostOnReddit()