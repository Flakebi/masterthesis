#!/usr/bin/env bash
# Warhammer 40,000: Dawn of War III

steam -applaunch 285190
sleep 5
for pid in `pgrep DawnOfWar3`; do
	tail --pid=$pid -f /dev/null
done

# Extract average frame time in ms
cd "/home/sebi/.local/share/feral-interactive/Dawn of War III/VFS/User/AppData/Roaming/My Games/Dawn of War III/LogFiles"
echo Average frame time
#cat $( ls -t *.xml | head -1 ) | grep results | cut -d\" -f16
echo 1
