from os import path, makedirs
import requests
from shutil import copyfileobj

var_folder = "/usr/local/var/reddit-wallpapers-macosx"


def create_var_folder():
    if not path.exists(var_folder):
        try:
            makedirs(var_folder)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def store_image(post):
    create_var_folder()
    filename = var_folder + post.filename

    r = requests.get(post.image_url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            r.raw.decode_content = True
            copyfileobj(r.raw, f)

    return filename
