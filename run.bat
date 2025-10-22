@echo off
for /f "delims=" %%i in ('
    python -c "import json; c=json.load(open('config.json')); [print(f'set {k}={v}') for k,v in c.items()]"
') do %%i


start /min %Source_2_Viewer_directory%\Source2Viewer-CLI.exe -i "%Deadlock_directory%/game/citadel/pak01_dir.vpk" --output "%CD%" --vpk_filepath "scripts/" -d
timeout /t 5
taskkill /im Source2Viewer-CLI.exe /f
copy scripts\heroes.vdata .\DeadlockRandomizer\heroes.vdata
copy scripts\abilities.vdata .\DeadlockRandomizer\abilities.vdata

timeout /t 5
echo "Parsing Hero Data"
py "parser/parser.py" "%CSDK_directory%"
echo "parsing Complete!"

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
echo [[step]] > "%dead_packer_directory%/Truerandom.toml"
echo [step.compile] >> "%dead_packer_directory%/Truerandom.toml"
echo resource_compiler_path = '%CSDK_directory%/game/bin/win64/resourcecompiler.exe' >> "%dead_packer_directory%/Truerandom.toml"
echo addon_content_directory = '%CSDK_directory%/content/citadel_addons/TrueRandom' >> "%dead_packer_directory%/Truerandom.toml"

echo [[step]] >> "%dead_packer_directory%/Truerandom.toml"
echo [step.pack] >> "%dead_packer_directory%/Truerandom.toml"
echo input_directory = '%CSDK_directory%/game/citadel_addons/TrueRandom' >> "%dead_packer_directory%/Truerandom.toml"
echo output_path = '%deadlockAddondir%/pak01_dir.vpk' >> "%dead_packer_directory%/Truerandom.toml"
echo exclude = ['cache_*.soc', 'tools_thumbnail_cache.bin'] >> "%dead_packer_directory%/Truerandom.toml"

start /min %dead_packer_directory%\Deadpacker.exe %dead_packer_directory%\TrueRandom.toml /s
timeout /t 5
taskkill /im Deadpacker.exe /f
echo "Randomizer complete!"
%deadlockdir%\deadlock.exe 