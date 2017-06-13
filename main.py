import os
import errno
import rumps
import requests
import random
import sys
import shutil
from appscript import app, mactypes

SUBREDDITS = ["earthporn"]


def get_wallpaper():
    subreddit = random.choice(SUBREDDITS)
    r = requests.get("https://www.reddit.com/r/" + subreddit + ".json",
                     headers={'User-agent': 'mac-os-wallpaper-0.1'})
    json = r.json()["data"]["children"]
    posts = [post["data"] for post in json if "preview" in post["data"]]
    post = random.choice(posts)
    return post["preview"]["images"][0]["source"]["url"]


def store_image(url):
    filename = "/usr/local/var/mac-os-wallpaper/" + os.path.basename(url)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    return filename


class RedditWallpaperApp(rumps.App):
    def __init__(self):
        super(RedditWallpaperApp, self).__init__("Awesome App")
        self.menu = ["Preferences", "Silly button", "Say hi"]
        self.icon = "icon.png"

    @rumps.clicked("Random image")
    def set_image(self, _):
        try:
            filename = store_image(get_wallpaper())
            app('Finder').desktop_picture.set(mactypes.File(filename))
        except Exception as e:
            print(sys.exc_info()[0], e)


if __name__ == "__main__":
    RedditWallpaperApp().run()
