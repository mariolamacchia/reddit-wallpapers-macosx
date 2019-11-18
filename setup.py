from setuptools import setup

setup(
  name="Reddit Wallpapers",
  version="0.1",
  description="Reddit Wallpapers for MacOSX",
  author="Mario Lamacchia",
  author_email="mariolamacchia@gmail.com",
  url="https://github.com/mariolamacchia/reddit-wallpapers-macosx",
  keywords=["wallpapers", "macosx", "reddit"],
  classifiers=[],
  install_requires=[
    "appscript==1.0.1",
    "certifi==2017.4.17",
    "chardet==3.0.4",
    "idna==2.5",
    "pyobjc==3.2.1",
    "pyobjc-core==3.2.1",
    "pyobjc-framework-Accounts==3.2.1",
    "pyobjc-framework-AddressBook==3.2.1",
    "pyobjc-framework-AppleScriptKit==3.2.1",
    "pyobjc-framework-AppleScriptObjC==3.2.1",
    "pyobjc-framework-ApplicationServices==3.2.1",
    "pyobjc-framework-Automator==3.2.1",
    "pyobjc-framework-AVFoundation==3.2.1",
    "pyobjc-framework-AVKit==3.2.1",
    "pyobjc-framework-CalendarStore==3.2.1",
    "pyobjc-framework-CFNetwork==3.2.1",
    "pyobjc-framework-CloudKit==3.2.1",
    "pyobjc-framework-Cocoa==3.2.1",
    "pyobjc-framework-Collaboration==3.2.1",
    "pyobjc-framework-Contacts==3.2.1",
    "pyobjc-framework-ContactsUI==3.2.1",
    "pyobjc-framework-CoreBluetooth==3.2.1",
    "pyobjc-framework-CoreData==3.2.1",
    "pyobjc-framework-CoreLocation==3.2.1",
    "pyobjc-framework-CoreText==3.2.1",
    "pyobjc-framework-CoreWLAN==3.2.1",
    "pyobjc-framework-CryptoTokenKit==3.2.1",
    "pyobjc-framework-DictionaryServices==3.2.1",
    "pyobjc-framework-DiskArbitration==3.2.1",
    "pyobjc-framework-EventKit==3.2.1",
    "pyobjc-framework-ExceptionHandling==3.2.1",
    "pyobjc-framework-FinderSync==3.2.1",
    "pyobjc-framework-FSEvents==3.2.1",
    "pyobjc-framework-GameCenter==3.2.1",
    "pyobjc-framework-GameController==3.2.1",
    "pyobjc-framework-ImageCaptureCore==3.2.1",
    "pyobjc-framework-IMServicePlugIn==3.2.1",
    "pyobjc-framework-InputMethodKit==3.2.1",
    "pyobjc-framework-InstallerPlugins==3.2.1",
    "pyobjc-framework-InstantMessage==3.2.1",
    "pyobjc-framework-Intents==3.2.1",
    "pyobjc-framework-IOSurface==3.2.1",
    "pyobjc-framework-LatentSemanticMapping==3.2.1",
    "pyobjc-framework-LaunchServices==3.2.1",
    "pyobjc-framework-LocalAuthentication==3.2.1",
    "pyobjc-framework-MapKit==3.2.1",
    "pyobjc-framework-MediaAccessibility==3.2.1",
    "pyobjc-framework-MediaLibrary==3.2.1",
    "pyobjc-framework-MediaPlayer==3.2.1",
    "pyobjc-framework-ModelIO==3.2.1",
    "pyobjc-framework-MultipeerConnectivity==3.2.1",
    "pyobjc-framework-NetFS==3.2.1",
    "pyobjc-framework-NetworkExtension==3.2.1",
    "pyobjc-framework-NotificationCenter==3.2.1",
    "pyobjc-framework-OpenDirectory==3.2.1",
    "pyobjc-framework-Photos==3.2.1",
    "pyobjc-framework-PhotosUI==3.2.1",
    "pyobjc-framework-PreferencePanes==3.2.1",
    "pyobjc-framework-PubSub==3.2.1",
    "pyobjc-framework-QTKit==3.2.1",
    "pyobjc-framework-Quartz==3.2.1",
    "pyobjc-framework-SafariServices==3.2.1",
    "pyobjc-framework-SceneKit==3.2.1",
    "pyobjc-framework-ScreenSaver==3.2.1",
    "pyobjc-framework-ScriptingBridge==3.2.1",
    "pyobjc-framework-SearchKit==3.2.1",
    "pyobjc-framework-ServiceManagement==3.2.1",
    "pyobjc-framework-Social==3.2.1",
    "pyobjc-framework-SpriteKit==3.2.1",
    "pyobjc-framework-StoreKit==3.2.1",
    "pyobjc-framework-SyncServices==3.2.1",
    "pyobjc-framework-SystemConfiguration==3.2.1",
    "pyobjc-framework-WebKit==3.2.1",
    "requests==2.20.0",
    "rumps==0.2.2",
    "urllib3==1.25.7",
  ],
  options={
    "py2app": {
      "argv_emulation": True,
      "plist": {
        "LSUIElement": True,
      },
      "iconfile": "icon.icns",
      "packages": ["rumps", "requests", "certifi"],
      "resources": ["src/resources"]
    },
  },
  setup_requires=["py2app"],
  app=["src/reddit_wallpapers_macosx.py"],
)
