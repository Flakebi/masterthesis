#!/usr/bin/env bash
# E.g. start with `+timedemoquit midemo2`
set -e

PGO_FOLDER=/home/sebi/Downloads/pgo/dota-auto
rm -rf "$PGO_FOLDER"
mkdir "$PGO_FOLDER"

rm -r /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/dota/shadercache
# Run 2 times without PGO
echo Run 1 without PGO
env SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' -sdl_displayindex 1 +demo_quitafterplayback 1 +cl_showfps 2 $@
echo
echo Run 2 without PGO
env SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' -sdl_displayindex 1 +demo_quitafterplayback 1 +cl_showfps 2 $@

rm -r /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/dota/shadercache
# Run with instrumentation
echo
echo Run with PGO instrumentation
env AMDVLK_PROFILE_INSTR_GEN="$PGO_FOLDER/Pipeline_%i_%m.profraw" SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' -sdl_displayindex 1 +demo_quitafterplayback 1 +cl_showfps 2 $@

cd "$PGO_FOLDER"
echo
echo Converting PGO data
/home/sebi/Masterarbeit/repo/pgo-example/convert_pipelines.sh
cd -

rm -r /mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota\ 2\ beta/game/dota/shadercache
# Run 2 times with PGO
echo
echo Run 1 with PGO
env AMDVLK_PROFILE_INSTR_USE="$PGO_FOLDER/Pipeline_%i.profdata" SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' -sdl_displayindex 1 +demo_quitafterplayback 1 +cl_showfps 2 $@
echo
echo Run 2 with PGO
env AMDVLK_PROFILE_INSTR_USE="$PGO_FOLDER/Pipeline_%i.profdata" SDL_VIDEODRIVER=x11 VK_ICD_FILENAMES=/mnt/newvms/Masterarbeit/vulkandriver/drivers/amd_icd64.json '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/dota 2 beta/game/dota.sh' -sdl_displayindex 1 +demo_quitafterplayback 1 +cl_showfps 2 $@
