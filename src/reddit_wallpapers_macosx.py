import os
from threading import Timer
from traceback import format_exc
from rumps import App, MenuItem, separator

from config import (
    resources_folder,
    preferences,
    create_preference_file,
    preferences_file,
)
from reddit import get_random_post
from osx import set_run_on_boot, open_webpage, set_wallpaper
from var import log_error


def handle_error(e):
    print(format_exc())
    log_error(e)


class RedditWallpaperApp(App):
    def __init__(self):
        try:
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
                MenuItem("Reload Preferences",
                         callback=self.update_preferences),
                separator,
            ]
            self.set_image(None)
        except Exception as e:
            handle_error(e)

    def update_preferences(self, _):
        try:
            preferences.load()
            if hasattr(self, 'timer'):
                self.timer.cancel()
            self.set_timer()
            set_run_on_boot(preferences.run_on_boot)
        except Exception as e:
            handle_error(e)

    def set_timer(self):
        auto_reload = preferences.auto_reload
        if auto_reload:
            self.timer = Timer(auto_reload, self.set_image, [None])
            self.timer.start()

    def set_image(self, _):
        try:
            self.set_timer()
            post = get_random_post()
            self.current_post = post

            # Set desktop wallpaper
            set_wallpaper(post.local_path)

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
            url = "https://www.reddit.com" + self.current_post.permalink
            open_webpage(url)
        except Exception as e:
            handle_error(e)


if __name__ == "__main__":
    RedditWallpaperApp().run()
