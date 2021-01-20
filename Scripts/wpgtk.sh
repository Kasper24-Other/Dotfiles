#!/bin/bash
nitrogen --set-auto ~/.config/wpg/.current
wal_steam -w

if pgrep -x "spotify" > /dev/null
then
    spicetify apply
else
    spicetify update
fi