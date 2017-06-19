from os import path
import random
import requests
from var import store_image
from config import preferences


class RedditPost:
    def __init__(self, d):
        self.permalink = d["permalink"]
        self.title = d["title"]
        self.image_url = d["preview"]["images"][0]["source"]["url"]
        self.subreddit = d["subreddit"]
        self.filename = path.basename(self.image_url)
        self.local_path = store_image(self)


def get_random_post():
    subreddit = random.choice(preferences.subreddits)
    r = requests.get("https://www.reddit.com/r/" + subreddit + ".json",
                     headers={"User-agent": "reddit-wallpapers-macosx-0.1"})
    json = r.json()["data"]["children"]
    posts = [post["data"] for post in json if "preview" in post["data"]]
    return RedditPost(random.choice(posts))
