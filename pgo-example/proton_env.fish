#!/usr/bin/env fish
set W '/home/sebi/.steam/steam/steamapps/common/Proton 4.2/dist'
#set -x WINEVERPATH "$W"
#set -x PATH "$W/bin" "$PATH"
#set -x WINESERVER "$W/bin/wineserver"
#set -x WINELOADER "$W/bin/wine"
#set -x WINEDLLPATH "$W/lib/wine/fakedlls"
#set -x LD_LIBRARY_PATH "$W/lib" "$LD_LIBRARY_PATH"
# Ashes of the Singularity
set APPID 507490
set -x STEAM_COMPAT_DATA_PATH "/mnt/bigdata/Dateien/Programme/Steam/steamapps/compatdata/$APPID"
#set -x WINEPREFIX "$STEAM_COMPAT_PATH/pfx"
#set -x STEAM_RUNTIME_LIBRARY_PATH /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_32 /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_64 /usr/lib32 /usr/lib32/libva1 /usr/lib /usr/lib/libva1 /usr/lib/dovecot /usr/lib/libfakeroot /usr/lib/opencollada /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/lib/i386-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/lib /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/usr/lib/i386-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/usr/lib /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/lib/x86_64-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/lib /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/usr/lib/x86_64-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/usr/lib

#set -x TEXTDOMAIN steam
#set -x SteamUser sirfrancisflake
#set -x STEAMSCRIPT /usr/lib/steam/steam
#set -x LD_LIBRARY_PATH /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_32 /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_64 /usr/lib32 /usr/lib32/libva1 /usr/lib /usr/lib/libva1 /usr/lib/dovecot /usr/lib/libfakeroot /usr/lib/opencollada /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/lib/i386-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/lib /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/usr/lib/i386-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/i386/usr/lib /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/lib/x86_64-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/lib /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/usr/lib/x86_64-linux-gnu /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/usr/lib
#set -x SteamClientLaunch 1
set -x EnableConfiguratorSupport 0
set -x SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD 1
set -x LD_PRELOAD /home/sebi/.local/share/Steam/ubuntu12_32/gameoverlayrenderer.so /home/sebi/.local/share/Steam/ubuntu12_64/gameoverlayrenderer.so
set -x SteamGameId $APPID
set -x STEAMSCRIPT_VERSION $APPID
set -x STEAM_CLIENT_CONFIG_FILE /home/sebi/.local/share/Steam/steam.cfg
set -x STEAM_RUNTIME /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime
set -x STEAM_COMPAT_CLIENT_INSTALL_PATH /home/sebi/.local/share/Steam
#set -x ENABLE_VK_LAYER_VALVE_steam_overlay_1 1
set -x SteamAppId $APPID
#set -x Steam3Master 127.0.0.1:57343
set -x PATH /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/bin /home/sebi/.local/share/Steam/ubuntu12_32/steam-runtime/amd64/usr/bin /home/sebi/Dokumente/Freizeit/Programmieren/Shell /home/sebi/Dokumente/Freizeit/Programmieren/Rust/Scripts /usr/local/sbin /usr/local/bin /usr/bin /bin /opt/bin /mnt/bigdata/Dateien/Programme/Tools/android-sdk/tools /mnt/bigdata/Dateien/Programme/Tools/android-sdk/platform-tools /usr/lib/jvm/default/bin /usr/bin/site_perl /usr/bin/vendor_perl /usr/bin/core_perl /home/sebi/.cargo/bin /home/sebi/.yarn/bin /home/sebi/.config/yarn/global/node_modules/.bin /home/sebi/.npm-global/bin /home/sebi/.dotnet/tools

#'/home/sebi/.steam/steam/steamapps/common/Proton 4.2/proton' waitforexitandrun ./game.exe
'/home/sebi/.steam/steam/steamapps/common/Proton 4.2/proton' waitforexitandrun ./AshesEscalation_DX11.exe -benchmark BenchFinal
