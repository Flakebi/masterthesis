#!/usr/bin/env bash
# Ashes of the Singularity
export SteamAppId=507490
export STEAM_COMPAT_DATA_PATH="/mnt/bigdata/Dateien/Programme/Steam/steamapps/compatdata/$SteamAppId"
export EnableConfiguratorSupport=0
export SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD=1
export SteamGameId=$SteamAppId
export STEAMSCRIPT_VERSION=$SteamAppId
export STEAM_CLIENT_CONFIG_FILE=/home/sebi/.local/share/Steam/steam.cfg
export STEAM_RUNTIME=/home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime
export STEAM_COMPAT_CLIENT_INSTALL_PATH=/home/sebi/.local/share/Steam
export 'PATH=/home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/bin:/home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/usr/bin:/home/sebi/Dokumente/Freizeit/Programmieren/Shell:/home/sebi/Dokumente/Freizeit/Programmieren/Rust/Scripts:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/opt/bin:/mnt/bigdata/Dateien/Programme/Tools/android-sdk/tools:/mnt/bigdata/Dateien/Programme/Tools/android-sdk/platform-tools:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/home/sebi/.cargo/bin:/home/sebi/.yarn/bin:/home/sebi/.config/yarn/global/node_modules/.bin:/home/sebi/.npm-global/bin:/home/sebi/.dotnet/tools'

cd '/mnt/bigdata/Dateien/Programme/Steam/steamapps/common/Ashes of the Singularity Escalation'
'/home/sebi/.steam/steam/steamapps/common/Proton 4.2/proton' waitforexitandrun ./AshesEscalation_DX11.exe -benchmark BenchFinal
