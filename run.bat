@echo off
echo "Initializing"
for /f "delims=" %%i in ('
    python -c "import json; c=json.load(open('config.json')); [print(f'set {k}={v}') for k,v in c.items()]"
') do %%i
mkdir "%CSDK_directory%\content\citadel_addons\Randomizer" > nul 2> nul
mkdir "%CSDK_directory%\content\citadel_addons\Randomizer\scripts" > nul 2> nul
type nul> "%CSDK_directory%\content\citadel_addons\Randomizer\scripts\heroes.vdata"
type nul> "%CSDK_directory%\content\citadel_addons\Randomizer\scripts\abilities.vdata"  

start /min %Source_2_Viewer_directory%\Source2Viewer-CLI.exe -i "%Deadlock_directory%/game/citadel/pak01_dir.vpk" --output "%CD%" --vpk_filepath "scripts/" -d > nul 2> nul
timeout /t 5 > nul 2> nul
taskkill /im Source2Viewer-CLI.exe /f > nul 2> nul
copy scripts\heroes.vdata .\DeadlockRandomizer\heroes.vdata > nul 2> nul
copy scripts\abilities.vdata .\DeadlockRandomizer\abilities.vdata > nul 2> nul
echo "Initialization Complete!"

timeout /t 5 > nul 2> nul
echo "Parsing Hero Data"
py "parser/parser.py" "%CSDK_directory%"
echo "Parsing Complete!"

set deadlockdir=%Deadlock_directory%/game/bin/win64
set deadlockAddondir=%Deadlock_directory%/game/citadel/addons

echo "Copying gameinfo"
copy "%CD%\gameinfo.gi" "%Deadlock_directory%\game\citadel\gameinfo.gi" /Y > nul 2> nul 
echo "Copying Complete!"

echo "Running Randomizer"
mkdir "%deadlockAddondir%" > nul 2> nul 
py "./DeadlockRandomizer/main.py" "%CSDK_directory%"
echo "Randomizer Complete!"

echo "Compiling"
echo [[step]] > "%dead_packer_directory%/Randomizer.toml"
echo [step.compile] >> "%dead_packer_directory%/Randomizer.toml"
echo resource_compiler_path = '%CSDK_directory%/game/bin/win64/resourcecompiler.exe' >> "%dead_packer_directory%/Randomizer.toml"
echo addon_content_directory = '%CSDK_directory%/content/citadel_addons/TrueRandom' >> "%dead_packer_directory%/Randomizer.toml"

echo [[step]] >> "%dead_packer_directory%/Randomizer.toml"
echo [step.pack] >> "%dead_packer_directory%/Randomizer.toml"
echo input_directory = '%CSDK_directory%/game/citadel_addons/TrueRandom' >> "%dead_packer_directory%/Truerandom.toml"
echo output_path = '%deadlockAddondir%/pak01_dir.vpk' >> "%dead_packer_directory%/Randomizer.toml"
echo exclude = ['cache_*.soc', 'tools_thumbnail_cache.bin'] >> "%dead_packer_directory%/Randomizer.toml"

start /min %dead_packer_directory%\Deadpacker.exe %dead_packer_directory%\Randomizer.toml /s
timeout /t 5 > nul 
taskkill /im Deadpacker.exe /f > nul 
echo "Compiling complete!"
echo "Starting Deadlock!"
%deadlockdir%\deadlock.exe 