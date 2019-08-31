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
echo FPS list
grep avg_fps *.xml | cut -d'>' -f2 | cut -d'<' -f1 | paste -sd,
