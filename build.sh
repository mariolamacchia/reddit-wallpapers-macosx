source=dist
title="Reddit Wallpapers"
size=15000
backgroundPictureName="background.png"
applicationName="reddit_wallpapers_macosx.app"
finalDMGName="reddit-wallpapers"

cp -R .background dist

hdiutil create -srcfolder "${source}" -volname "${title}" -fs HFS+ \
    -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${size}k pack.temp.dmg

device=$(hdiutil attach -readwrite -noverify -noautoopen "pack.temp.dmg" | \
    egrep '^/dev/' | sed 1q | awk '{print $1}')

echo '
   tell application "Finder"
     tell disk "'${title}'"
           open
           delay 5
           set current view of container window to icon view
           set toolbar visible of container window to false
           set statusbar visible of container window to false
           set the bounds of container window to {400, 100, 1040, 430}
           set theViewOptions to the icon view options of container window
           set arrangement of theViewOptions to not arranged
           set icon size of theViewOptions to 100
           set background picture of theViewOptions to file ".background:'${backgroundPictureName}'"
           make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
           set position of item "'${applicationName}'" of container window to {160, 190}
           set position of item "Applications" of container window to {480, 190}
           update without registering applications
           delay 5
           close
     end tell
   end tell
' | osascript

chmod -Rf go-w /Volumes/"${title}"
sync
sync
hdiutil detach ${device}
hdiutil convert "/pack.temp.dmg" -format UDZO -imagekey zlib-level=9 -o "${finalDMGName}"
rm -f /pack.temp.dmg
