#!/usr/bin/env bash
# F1 2017

steam -applaunch 515220
#steam steam://rungameid/515220
sleep 5
for pid in `pgrep F12017`; do
	tail --pid=$pid -f /dev/null
done

# Extract average frame time in ms
cd "/home/sebi/.local/share/feral-interactive/F1 2017/SaveData/feral_bench/"
echo Average frame time
cat $( ls -t *.xml | head -1 ) | grep results | cut -d\" -f16
