curl -L $(curl -s https://api.github.com/repos/mariolamacchia/reddit-wallpapers-macosx/releases | grep browser_download_url | head -n 1 | cut -d '"' -f 4) > reddit-wallpapers.dmg
sudo hdiutil attach reddit-wallpapers.dmg
cp -R "/Volumes/Reddit Wallpapers/Reddit Wallpapers.app" /Applications
sudo hdiutil detach "/Volumes/Reddit Wallpapers"
rm reddit-wallpapers.dmg
open /Applications/Reddit\ Wallpapers.app
