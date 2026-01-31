import re
import json

with open("config.json", 'r') as file:
    configData = json.load(file)
s_CSDK = configData["CSDK_directory"]

# fix the lash viper bug
f = open("DeadlockRandomizer\\abilities.vdata", "r")
data = f.read()
f.close()
i1 = data.index("_include ")
ic = i1
while data[ic] != ']':
    ic += 1
test = data[i1:ic+1]
data = data.replace(test, '')

weaponSets = re.findall("^\tcitadel_weapon_.*_set =", data, re.MULTILINE)


for i in range(len(weaponSets)):
    weaponSets[i] = weaponSets[i][1:-2]

for i, wset in enumerate(weaponSets):
    if wset != "citadel_weapon_lash_set":
        continue
    s1Index = data.index(weaponSets[i])
    s2Index = data.index(weaponSets[i+1])

    setInfo = data[s1Index:s2Index]
    oLash = setInfo

    lAbilities = re.findall("citadel_ability_lash.* =", setInfo, re.MULTILINE)

    for j, ability in enumerate(lAbilities):
        if j == len(lAbilities)-1:
            a1Index = data.index(lAbilities[j])
            a2Index = data.index("ability_lash_flog =")
        else:
            a1Index = data.index(lAbilities[j])
            a2Index = data.index(lAbilities[j+1])
        abilityInfo = data[a1Index:a2Index]
        oldability = abilityInfo
        newability = abilityInfo
        if ability == "citadel_ability_lash =":
            newability = newability.replace(
                "citadel_ability_lash =",
                "citadel_ability_sky_grapple ="
            )
        if ability == "citadel_ability_lash_ultimate =":
            newability = newability.replace(
                "citadel_ability_lash_ultimate =",
                "citadel_ability_cloud_pull ="
            )
        if ability == "citadel_ability_lash_down_strike =":
            newability = newability.replace(
                "citadel_ability_lash_down_strike =",
                "citadel_ability_high_slam ="
            )
        newability = oldability + '\n' + newability
        setInfo = setInfo.replace(oldability, newability)

    data = data.replace(oLash, setInfo)

output_path = (
    f"{s_CSDK}\\content\\citadel_addons\\TrueRandom\\scripts\\abilities.vdata"
)
with open(output_path, "w") as f:
    f.write(data)
    f.close()

# do normal parsing stuff
search_pattern = ""
f = open("parser\\heros.txt", "r")
heros = f.read().splitlines()
f.close()
herodict = {}
for hero in heros:
    h = hero.split(",")
    herodict[h[0]] = h[1]

f = open("DeadlockRandomizer\\heroes.vdata", "r")

data = f.read()
f.close()
chars = re.findall("^\thero_.*", data, re.MULTILINE)

f = open("parser\\blacklist.txt", "r")
blacklist = f.read().splitlines()
f.close()

for i in range(len(blacklist)):
    blacklist[i] = blacklist[i][2:]

for i in range(len(chars)):
    chars[i] = chars[i][1:-3]
for i, char in enumerate(chars):
    if char in blacklist:
        continue

    c1Index = data.index(chars[i])
    c2Index = data.index(chars[i+1])
    output = data[c1Index:c2Index]
    if char == "hero_lash":
        output = output.replace(
            "citadel_ability_lash_down_strike", "citadel_ability_high_slam"
        )
        output = output.replace(
            "citadel_ability_lash_ultimate", "citadel_ability_cloud_pull"
        )
        output = output.replace(
            "citadel_ability_lash", "citadel_ability_sky_grapple"
        )
    if i == len(chars)-1:
        break

    char_file_path = (
        fr"DeadlockRandomizer\Characters\{herodict[char]}.txt"
    )
    with open(char_file_path, "w") as f:
        f.write(output)
        f.close()
