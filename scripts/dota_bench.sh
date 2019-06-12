#!/usr/bin/env bash
# Possible arguments:
# +timedemoquit midemo2
# +timedemoquit dota2-pts-1971360796 +timedemo_start 50000 +timedemo_end 51000
set -e

PGO_FOLDER=/home/sebi/Downloads/pgo/dota-auto
rm -rf "$PGO_FOLDER"
mkdir "$PGO_FOLDER"

DOTA_ARGS='-sdl_displayindex 1 +demo_quitafterplayback 1 +cl_showfps 2 +fps_max 0 -nosound -noassert -novconsole'

rm -r /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/dota/shadercache
# Run without PGO
for i in `seq 5`; do
	echo
	echo Run $i without PGO
	env SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' $DOTA_ARGS $@
done

rm -r /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/dota/shadercache
# Run with instrumentation
echo
echo Run with PGO instrumentation
env AMDVLK_PROFILE_INSTR_GEN="$PGO_FOLDER/Pipeline_%i_%m.profraw" SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' $DOTA_ARGS $@

cd "$PGO_FOLDER"
echo
echo Converting PGO data
/home/sebi/Masterarbeit/repo/scripts/convert_pipelines.sh
cd -

rm -r /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/dota/shadercache
# Run with PGO
for i in `seq 5`; do
	echo
	echo Run $i with PGO
	env AMDVLK_PROFILE_INSTR_USE="$PGO_FOLDER/Pipeline_%i.profdata" SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' $DOTA_ARGS $@
done
