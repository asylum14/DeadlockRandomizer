
function Cmd(command) {
    $.DispatchEvent("CitadelConCommand", command);
}

const heros = ["hero_inferno", "hero_gigawatt", "hero_hornet", "hero_ghost", "hero_atlas", "hero_wraith", "hero_forge", "hero_chrono", "hero_dynamo", "hero_kelvin", "hero_haze", "hero_astro", "hero_bebop", "hero_nano", "hero_orion", "hero_krill", "hero_shiv", "hero_tengu", "hero_warden", "hero_yamato", "hero_lash", "hero_viscous", "hero_synth", "hero_mirage", "hero_viper", "hero_magician", "hero_vampirebat", "hero_drifter", "hero_frank", "hero_bookworm", "hero_doorman", "hero_punkgoat"]

function RandomizeHero() {
    Cmd(`selecthero hero_${Math.floor(Math.random() * 31)}`);
}

function RandomizeHeroVanilla() {
    Cmd(`selecthero ${heros[Math.floor(Math.random()*heros.length)]}`);
}

function EnableXmasSkins() {
    Cmd(`ent_create logic_timer {"targetname" "xmastimer" "refiretime" "0.1" "startdisabled" "0"}`);
    Cmd(`ent_create point_servercommand {"targetname" "xmascmd"}`);
    $.Schedule(0.25, () => {
        Cmd(
            `ent_fire xmastimer addoutput "ontimer>xmascmd>command>ent_fire player setbodygroup hat,1;ent_fire player setbodygroup xmas,1>0>-1"`
        );
    });
}

function DisableXmasSkins() {
    Cmd(
        `ent_fire xmastimer Kill;ent_fire xmascmd Kill;ent_fire player setbodygroup hat,0;ent_fire player setbodygroup xmas,0`
    );
}
