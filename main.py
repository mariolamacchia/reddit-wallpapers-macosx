import os
import ConfigParser
import errno
import rumps
import requests
import random
import sys
import shutil
import webbrowser
from traceback import print_exc
from appscript import app, mactypes

config = ConfigParser.ConfigParser()


def reload_config():
    config.readfp(open("defaults.cfg"))
    config.read([os.path.expanduser("~/.wallpapers")])


def get_img_url_from_post(post):
    return post["preview"]["images"][0]["source"]["url"]


def get_filename_from_post(post):
    url = get_img_url_from_post(post)
    return "/usr/local/var/mac-os-wallpaper/" + os.path.basename(url)


def get_post():
    subreddit = random.choice(config.get("DEFAULT", "subreddits").split(","))
    r = requests.get("https://www.reddit.com/r/" + subreddit + ".json",
                     headers={"User-agent": "mac-os-wallpaper-0.1"})
    json = r.json()["data"]["children"]
    posts = [post["data"] for post in json if "preview" in post["data"]]
    return random.choice(posts)


def store_image_from_post(post):
    filename = get_filename_from_post(post)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    r = requests.get(get_img_url_from_post(post), stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def set_background(filename):
    app("Finder").desktop_picture.set(mactypes.File(filename))


class RedditWallpaperApp(rumps.App):
    def __init__(self):
        reload_config
        super(RedditWallpaperApp, self).__init__("Wallpapers from Reddit")
        self.icon = "icon.png"
        self.current_menu = rumps.MenuItem("", callback=self.open_post)
        self.menu = [
            self.current_menu,
            "Reload",
            rumps.separator,
        ]
        self.set_image(None)

    @rumps.clicked("Reload")
    def set_image(self, _):
        try:
            reload_config()
            self.set_post(get_post())
        except Exception as e:
            print_exc()

    def set_post(self, post):
        self.current_post = post
        store_image_from_post(post)
        filename = get_filename_from_post(post)
        set_background(filename)
        self.update_menu()

    def open_post(self, post):
        try:
            uri = self.current_post["permalink"]
            webbrowser.open("https://www.reddit.com" + uri)
        except Exception as e:
            print_exc()

    def update_menu(self):
        post = self.current_post
        title = post["title"]
        menu_max_length = config.getint("DEFAULT", "max_length")
        if len(title) > menu_max_length:
            title = title[:menu_max_length] + "..."
        title = title + " [/r/" + post["subreddit"] + "]"
        self.current_menu.title = title


if __name__ == "__main__":
    RedditWallpaperApp().run()
