# Scripts for ['Games Nebula'](https://github.com/yancharkin/games_nebula) (non-GOG games)

Minimal installation script should download and unpack (or install) game and contain game name on last (commented) line. It's possible to use any utilities, but I wrote few function that I find optimal for the task.

#### Environment variables that already set by 'Games Nebula':
- **$DOWNLOAD_DIR** - absolute path to download directory
- **$INSTALL_DIR** - absolute path to install directory
- **$WINE_PATH** - absolute path to directory containing wine binary or 'wine' if system version used
- **$GAME_NAME** - game id used by gog
- **$START_FILE** - absolute path to 'start.sh'
- **$SETTINGS_FILE** - absolute path to 'settings.sh'
- **$ADDITIONS_FILE** - absolute path to 'additions.sh'
- **$DOSBOX_GAME_CONF** - absolute path to 'dosbox_game.conf'
- **$DOSBOX_SETTINGS_CONF** - absolute path to 'dosbox_settings.conf'
- **$NEBULA_DIR** - path to root directory of 'Games Nebula'
- **$WINEARCH** - value of WINEARCH environment variable
- **$KEEP_INSTALLERS** - indicates if installers should be removed after installation

#### Shell functions
Few simple functions that can be used in bash scripts.

- **proc_timer** - simple timer, its main purpose to indicate that process didn't stalled.
- **get_arch** - return OS architecture.
- **get_common_file** - download file to "$DOWNLOAD_DIR/_distr/" using curl. Usable for downloading files required by more than one game.
- **get_file** - download file to "$DOWNLOAD_DIR/_distr/$GAME_NAME/". Usable for downloading game specific files (like patches or mods).
- **get_mylib_distr** - download file to "$DOWNLOAD_DIR/$GAME_NAME/". Usable for downloading game installers.
- **get_java_i586** - download 32-bit version of JRE to "$DOWNLOAD_DIR/_distr/" and unpack it to "$INSTALL_DIR/$GAME_NAME/jre".
- **get_java_x64** - download 64-bit version of JRE to "$DOWNLOAD_DIR/_distr/" and unpack it to "$INSTALL_DIR/$GAME_NAME/jre".
- **get_from_mega** - download file to "$DOWNLOAD_DIR/_distr/$GAME_NAME/" using megadl (megtools).
- **get_weidu** - download WeiDU and upack it to "$INSTALL_DIR/$GAME_NAME/game".
- **get_upx** - download UPX and upack it to "$INSTALL_DIR/$GAME_NAME/game".
- **setup_lavfilters** - download, unpack and setup LAVFilters (wine).

Before using them you have to add to your script:

    source "$NEBULA_DIR/scripts/shell_functions.sh"

#### autosetup.ini

Can be used to greatly simplify installation scripts.

**Options:**

- **image** - image url. If option exists ‘Games Nebula’ will download this image and use it to represent game in you library.
- **native_exe** - path to main executable (linux) (1)
- **native_settings_exe** - path to configuration utility (linux) (1)
- **win_exe** - path to main executable (windows) (1)
- **win_settings_exe** - path to configuration utility (windows) (1)
- **winedlloverrides** - value of WINEDLLOVERRIDES environment variable can be set here
- **winetricks** - components to install with winetricks
- **dos_iso** - path to disk image (1)
- **dos_exe** - path to main executable (dos) (1)
- **dos_settings_exe** - path to configuration utility (dos) (1)
- **scummvm_name** - name used in ScummVM
- **scummvm_id** - id used in ScummVM
- **special** - additional commands (copy, move, remove files, etc.) (2)
- **win_reg1, win_reg2, etc.** - keys to add to registry (windows) (2). **This option(s) should be at the end!**

*(1) - path relative to 'game' directory*

*(2) - see existing examples*

