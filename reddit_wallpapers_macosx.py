import os
import ConfigParser
import errno
import rumps
import requests
import random
import sys
import shutil
from threading import Timer
import webbrowser
from appscript import app, mactypes

config = ConfigParser.ConfigParser()
user_config_file_name = os.path.expanduser("~/.wallpapers")


def handle_error(e):
    os.system("""
          osascript -e 'display notification "{}" with title "{}"'
          """.format(e.message, "Error! :S"))


def get_resource_path(relative_path):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path + "/resources/" + relative_path


def reload_config():
    config.readfp(open(get_resource_path("defaults.cfg")))
    config.read([user_config_file_name])

    # Run on startup
    target = os.path.expanduser(
        "~/Library/LaunchAgents/" +
        "io.github.mariolamacchia.reddit-wallpapers-macosx.plist"
        )
    if config.getboolean("DEFAULT", "run_on_boot"):
        shutil.copyfile(get_resource_path("startup.plist"), target)
    else:
        try:
            os.remove(target)
        except OSError:
            pass


def get_img_url_from_post(post):
    return post["preview"]["images"][0]["source"]["url"]


def get_filename_from_post(post):
    url = get_img_url_from_post(post)
    return "/usr/local/var/reddit-wallpapers-macosx/" + os.path.basename(url)


def get_post():
    subreddit = random.choice(config.get("DEFAULT", "subreddits").split(","))
    r = requests.get("https://www.reddit.com/r/" + subreddit + ".json",
                     headers={"User-agent": "reddit-wallpapers-macosx-0.1"})
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
        super(RedditWallpaperApp, self).__init__("Wallpapers from Reddit")
        self.icon = get_resource_path("icon.png")
        self.current_menu = rumps.MenuItem("", callback=self.open_post)
        self.menu = [
            self.current_menu,
            "Reload...",
            rumps.separator,
            "Preferences",
            rumps.separator,
        ]
        self.set_image(None)

    @rumps.clicked("Reload...")
    def set_image(self, _):
        def timeout():
            self.set_image(_)

        try:
            reload_config()

            auto_reload = config.getint("DEFAULT", "auto_reload")
            if auto_reload:
                Timer(auto_reload, timeout).start()

            self.set_post(get_post())

        except Exception as e:
            handle_error(e)

    @rumps.clicked("Preferences")
    def change_preferences(self, _):
        try:
            if not os.path.exists(user_config_file_name):
                shutil.copyfile(get_resource_path("defaults.cfg"),
                                user_config_file_name)
            os.system("open ~/.wallpapers")
        except Exception as e:
            handle_error(e)

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
            handle_error(e)

    def update_menu(self):
        post = self.current_post
        title = post["title"]
        menu_max_length = config.getint("DEFAULT", "max_length")
        if menu_max_length > 0 and len(title) > menu_max_length:
            title = title[:menu_max_length] + "..."
        title = title + " [/r/" + post["subreddit"] + "]"
        self.current_menu.title = title


if __name__ == "__main__":
    RedditWallpaperApp().run()
