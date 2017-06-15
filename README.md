# Reddit Wallpapers for MacOSX

## Work in progress!

To make it work now:
- Setup virtualenv:

    ```sh
    $ virtualenv venv
    $ source venv/bin/activate
    ```

- Install dependencies:

    ```sh
    $ pip install -r requirements.txt
    ```

- Build application:

    ```sh
    $ python setup.py py2app
    ```

You will find the `reddit_wallpapers_macosx.app` inside the `dist` folder.
