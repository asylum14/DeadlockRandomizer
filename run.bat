@echo off

for /f "delims=" %%i in ('
    python -c "import json; c=json.load(open('config.json')); [print(f'set {k}={v}') for k,v in c.items()]"
') do %%i


mkdir "%CSDK_directory%\content\citadel_addons\Randomizer\"
mkdir "%CSDK_directory%\content\citadel_addons\Randomizer\scripts"
echo "" >> "%CSDK_directory%\content\citadel_addons\Randomizer\scripts\abilities.vdata"
echo "" >> "%CSDK_directory%\content\citadel_addons\Randomizer\scripts\heroes.vdata"

echo %Source_2_Viewer_directory%
echo %Deadlock_directory%
start /min %Source_2_Viewer_directory%\Source2Viewer-CLI.exe -i "%Deadlock_directory%/game/citadel/pak01_dir.vpk" --output "%CD%" --vpk_filepath "scripts/" -d
timeout /t 5
taskkill /im Source2Viewer-CLI.exe /f
copy scripts\heroes.vdata .\DeadlockRandomizer\heroes.vdata
copy scripts\abilities.vdata .\DeadlockRandomizer\abilities.vdata

timeout /t 5
echo %CSDK_directory%
py parser/parser.py "%CSDK_directory%"
rmdir /s /Q scripts

set deadlockdir=%Deadlock_directory%/game/bin/win64
set deadlockAddondir=%Deadlock_directory%/game/citadel/addons

echo "Copying gameinfo"
copy "%CD%\gameinfo.gi" "%Deadlock_directory%\game\citadel\gameinfo.gi" /Y
if not exist "%deadlockAddondir%\" (
    mkdir "%deadlockAddondir%"
    echo Directory "%deadlockAddondir%" was created.
)else (
    echo Directory "%deadlockAddondir%" already exists.
)
py "./DeadlockRandomizer/main.py" "%CSDK_directory%"
echo [[step]] > "%DeadPacker_directory%/Randomizer.toml"
echo [step.compile] >> "%DeadPacker_directory%/Randomizer.toml"
echo resource_compiler_path = '%CSDK_directory%/game/bin/win64/resourcecompiler.exe' >> "%DeadPacker_directory%/Randomizer.toml"
echo addon_content_directory = '%CSDK_directory%/content/citadel_addons/Randomizer' >> "%DeadPacker_directory%/Randomizer.toml"

echo [[step]] >> "%DeadPacker_directory%/Randomizer.toml"
echo [step.pack] >> "%DeadPacker_directory%/Randomizer.toml"
echo input_directory = '%CSDK_directory%/game/citadel_addons/Randomizer' >> "%DeadPacker_directory%/Randomizer.toml"
echo output_path = '%deadlockAddondir%/pak01_dir.vpk' >> "%DeadPacker_directory%/Randomizer.toml"
echo exclude = ['cache_*.soc', 'tools_thumbnail_cache.bin'] >> "%DeadPacker_directory%/Randomizer.toml"

echo %DeadPacker_directory%
start %DeadPacker_directory%\Deadpacker.exe %DeadPacker_directory%\Randomizer.toml /s
timeout /t 5
taskkill /im Deadpacker.exe /f
echo "Randomizer complete!"
"%deadlockdir%\deadlock.exe"
