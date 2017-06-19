from os import remove
from shutil import copyfile
import webbrowser
from appscript import app, mactypes


def set_run_on_boot(should_run):
    # Run on startup
    filenam = os.path.expanduser(
        "~/Library/LaunchAgents/" +
        "io.github.mariolamacchia.reddit-wallpapers-macosx.plist"
        )
    if should_run:
        copyfile(resources_folder + "/startup.plist", filename)
    else:
        try:
            remove(filename)
        except OSError:
            pass


def set_wallpaper(filename):
    app("Finder").desktop_picture.set(mactypes.File(filename))


def open_webpage(url):
    webbrowser.open(url)
