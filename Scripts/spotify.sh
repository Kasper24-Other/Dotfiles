if pgrep -x "spotify" > /dev/null
then
    spicetify apply
else
    spicetify update
fi