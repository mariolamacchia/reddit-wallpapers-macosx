curl -L $(curl -s https://api.github.com/repos/mariolamacchia/reddit-wallpapers-macosx/releases | grep browser_download_url | head -n 1 | cut -d '"' -f 4) > reddit-wallpapers.dmg
sudo hdiutil attach reddit-wallpapers.dmg
cp -R "/Volumes/reddit-wallpapers/Reddit Wallpapers.app" ~/Applications
sudo hdiutil detach /Volumes/reddit-wallpapers
rm reddit-wallpapers.dmg
open "~/Applications/Reddit Wallpapers.app"
