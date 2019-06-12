#!/usr/bin/env bash
# Possible arguments:
# +timedemoquit midemo2
# +timedemoquit dota2-pts-1971360796 +timedemo_start 50000 +timedemo_end 51000
set -e

PGO_FOLDER=/home/sebi/Downloads/pgo/ashes-auto
rm -rf "$PGO_FOLDER"
mkdir "$PGO_FOLDER"

# Run without PGO
for i in `seq 3`; do
	echo
	echo Run $i without PGO
	env VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json /home/sebi/Masterarbeit/repo/scripts/ashes_start.sh
done

# Run with instrumentation
echo
echo Run with PGO instrumentation
env AMDVLK_PROFILE_INSTR_GEN="$PGO_FOLDER/Pipeline_%i_%m.profraw" VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json /home/sebi/Masterarbeit/repo/scripts/ashes_start.sh

cd "$PGO_FOLDER"
echo
echo Converting PGO data
/home/sebi/Masterarbeit/repo/scripts/convert_pipelines.sh
cd -

# Run with PGO
for i in `seq 3`; do
	echo
	echo Run $i with PGO
	env AMDVLK_PROFILE_INSTR_USE="$PGO_FOLDER/Pipeline_%i.profdata" VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json /home/sebi/Masterarbeit/repo/scripts/ashes_start.sh
done
