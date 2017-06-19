from os import mkdir, path
from shutil import copyfile
from ConfigParser import ConfigParser
from yaml import load

app_folder = path.dirname(path.realpath(__file__))
resources_folder = app_folder + "/resources"
user_folder = path.expanduser("~/.wallpapers")
default_preferences_file = resources_folder + "/defaults.yml"
preferences_file = user_folder + "/preferences.yml"


class Preferences:
    def __init__(self):
        self.load()

    def reset(self):
        self.from_yaml(default_preferences_file)

    def load(self):
        self.reset()
        if (path.isfile(preferences_file)):
            self.from_yaml(preferences_file)

    def from_yaml(self, file):
        f = open(file)
        self.from_dict(load(f.read()))
        f.close()

    def from_dict(self, d):
        keys = ["run_on_boot", "subreddits", "auto_reload", "max_length"]
        for key in keys:
            if key in d:
                setattr(self, key, d[key])


def create_preference_file():
    if not path.exists(preferences_file):
        copyfile(default_preferences_file, preferences_file)


if not path.isdir(user_folder):
    mkdir(user_folder)

preferences = Preferences()
