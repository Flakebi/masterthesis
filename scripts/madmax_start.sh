#!/usr/bin/env bash
# Mad Max

steam -applaunch 234140 --feral-benchmark
#steam -applaunch 234140
sleep 5
for pid in `pgrep MadMax`; do
	tail --pid=$pid -f /dev/null
done

# Extract average frame time in ms
cd "/home/sebi/.local/share/feral-interactive/Mad Max/VFS/User/AppData/Roaming/WB Games/Mad Max/FeralBenchmark"
cd $( ls -td * | head -1 )
echo Average frame time
#cat $( ls -t *.xml | head -1 ) | grep results | cut -d\" -f16
echo 1
