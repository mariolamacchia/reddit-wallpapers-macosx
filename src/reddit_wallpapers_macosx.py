import os
import webbrowser
from shutil import copyfile
from threading import Timer
from traceback import format_exc
from appscript import app, mactypes
from rumps import App, MenuItem, separator

from config import (
    resources_folder,
    preferences,
    create_preference_file,
    preferences_file,
)
from reddit import get_random_post

log_file_name = "/usr/local/var/reddit-wallpapers-macosx/errors.log"


def handle_error(e):
    print(format_exc())
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
        copyfile(resources_folder + "/startup.plist", target)
    else:
        try:
            os.remove(target)
        except OSError:
            pass


class RedditWallpaperApp(App):
    def __init__(self):
        super(RedditWallpaperApp, self).__init__("Wallpapers from Reddit")
        self.icon = resources_folder + "/icon.png"
        self.current_menu = MenuItem("", callback=self.open_post)
        self.quit_button = "Quite Reddit Wallpapers"
        self.menu = [
            self.current_menu,
            MenuItem("Change wallpaper", callback=self.set_image),
            separator,
            MenuItem("Open preferences file",
                     callback=self.change_preferences),
            MenuItem("Reload Preferences", callback=self.update_preferences),
            separator,
        ]
        self.set_image(None)

    def update_preferences(self, _):
        preferences.load()
        if hasattr(self, 'timer'):
            self.timer.cancel()
        self.set_timer()

    def set_timer(self):
        auto_reload = preferences.auto_reload
        if auto_reload:
            self.timer = Timer(auto_reload, self.set_image, [None])
            self.timer.start()

    def set_image(self, _):
        self.set_timer()

        try:
            post = get_random_post()
            self.current_post = post

            # Set desktop wallpaper
            app("Finder").desktop_picture.set(mactypes.File(post.local_path))

            # Update menu
            title = post.title
            menu_max_length = preferences.max_length
            if menu_max_length > 0 and len(title) > menu_max_length:
                title = title[:menu_max_length] + "..."
            title = title + " [/r/" + post.subreddit + "]"
            self.current_menu.title = title

        except Exception as e:
            handle_error(e)

    def change_preferences(self, _):
        try:
            create_preference_file()
            os.system("open " + preferences_file)
        except Exception as e:
            handle_error(e)

    def open_post(self, post):
        try:
            uri = self.current_post.permalink
            webbrowser.open("https://www.reddit.com" + self.current_post)
        except Exception as e:
            handle_error(e)


if __name__ == "__main__":
    RedditWallpaperApp().run()
