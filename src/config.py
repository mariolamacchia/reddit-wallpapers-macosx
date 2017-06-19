from os import mkdir, path
from shutil import copyfile
from ConfigParser import ConfigParser

app_folder = path.dirname(path.realpath(__file__))
resources_folder = app_folder + "/resources"
user_folder = path.expanduser("~/.wallpapers")
default_preferences_file = resources_folder + "/defaults.cfg"
preferences_file = user_folder + "/preferences.cfg"
preferences = {}


def load_preferences():
    config = ConfigParser()
    config.readfp(open(default_preferences_file))
    config.read([preferences_file])
    preferences["run_on_boot"] = config.getboolean("DEFAULT", "run_on_boot")
    preferences["subreddits"] = config.get("DEFAULT", "subreddits").split(",")
    preferences["auto_reload"] = config.getint("DEFAULT", "auto_reload")
    preferences["max_length"] = config.getint("DEFAULT", "max_length")


def create_preference_file():
    if not path.exists(preferences_file):
        copyfile(default_preferences_file, preferences_file)


if not path.isdir(user_folder):
    mkdir(user_folder)
load_preferences()
