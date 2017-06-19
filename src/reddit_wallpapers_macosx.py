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
from traceback import format_exc
from appscript import app, mactypes

from config import (
    resources_folder,
    preferences,
    create_preference_file,
    preferences_file,
)

log_file_name = "/usr/local/var/reddit-wallpapers-macosx/errors.log"


def handle_error(e):
    f = open(log_file_name, 'a')
    f.write(e.message)
    f.write(format_exc())
    f.close()


def reload_config():
    load_preferences()

    # Run on startup
    target = os.path.expanduser(
        "~/Library/LaunchAgents/" +
        "io.github.mariolamacchia.reddit-wallpapers-macosx.plist"
        )
    if preferences.run_on_boot:
        shutil.copyfile(resources_folder + "/startup.plist", target)
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
    subreddit = random.choice(preferences.subreddits)
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
        self.icon = resources_folder + "/icon.png"
        self.current_menu = rumps.MenuItem("", callback=self.open_post)
        self.quit_button = "Quite Reddit Wallpapers"
        self.menu = [
            self.current_menu,
            rumps.MenuItem("Change wallpaper",
                           key="change",
                           callback=self.set_image,
                           ),
            rumps.separator,
            "Preferences",
            rumps.separator,
        ]
        self.set_image(None)

    def set_image(self, _):
        def timeout():
            self.set_image(_)

        try:
            preferences.load()

            auto_reload = preferences.auto_reload
            if auto_reload:
                Timer(auto_reload, timeout).start()
            self.set_post(get_post())
        except Exception as e:
            handle_error(e)

    @rumps.clicked("Preferences")
    def change_preferences(self, _):
        try:
            create_preference_file()
            os.system("open " + preferences_file)
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
        menu_max_length = preferences.max_length
        if menu_max_length > 0 and len(title) > menu_max_length:
            title = title[:menu_max_length] + "..."
        title = title + " [/r/" + post["subreddit"] + "]"
        self.current_menu.title = title


if __name__ == "__main__":
    RedditWallpaperApp().run()
