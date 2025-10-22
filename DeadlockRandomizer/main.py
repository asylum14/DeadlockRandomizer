import re
import os
import glob
from datetime import  datetime, timezone
from random import randint, seed
import sys
utc_now = datetime.now(timezone.utc)
dt = utc_now.date()
seed(str(dt))


s_CSDK =sys.argv[1]

count = 76
directory_path = "DeadlockRandomizer\\Characters"

search_pattern = os.path.join(directory_path, "*.txt")
chars = glob.glob(search_pattern)
output=""
ultimates = []
abilities = []
names =[]
for char in chars:
    names.append(char)
    f = open(char)
    data = f.read()
    f.close()
    result = re.findall("^\t\t\t.*ESlot_Signature.*", data, re.MULTILINE)
    ultimate =result[3][24:-1]
    ultimates.append(ultimate)
    result.pop(3)
    for i in range(len(result)):
        abilities.append(result[i][24:-1])
        


for char in chars:
    f = open(char)
    data = f.read()
    f.close()
    result = re.findall("^\t\t\t.*ESlot_Signature.*", data, re.MULTILINE)
    idPattern = re.findall("^\t\tm_HeroID =.*$", data, re.MULTILINE)
    idPattern = idPattern[0][2:]
    namePattern = re.findall("^hero_.*$", data, re.MULTILINE)
    namePattern = namePattern[0][0:-2]
    namePattern = "^"+namePattern
    charSelect = re.findall("^\t\tm_bDisabled = false$", data, re.MULTILINE)
    currHeroId = f"m_HeroID = {count}"
    heroName = f"hero_{count - 76}"
    currData = data
    currData = re.sub(idPattern, currHeroId, currData)
    currData = re.sub(namePattern, heroName, currData)
    currData = re.sub(charSelect[0], "\t\tm_bDisabled = true", currData)

    for i in range(len(result)):
        if i % 4 == 3:
            uIndex =randint(0, len(ultimates)-1)
            currData = re.sub(result[i][24:-1], ultimates[uIndex], currData)
            ultimates.pop(uIndex)
        else:
            aIndex = randint(0,len(abilities)-1)
            currData = re.sub(result[i][19:-1], f"{i+1} = \"{abilities[aIndex]}", currData)
            abilities.pop(aIndex)

    output += currData
    output+="\n"
    count += 1

f = open("DeadlockRandomizer\\heroes.vdata")
data = f.read()
f.close()
data=data[:-1]
data = f"{data}\n{output}"
data+="}"
with open(f"{s_CSDK}\\content\\citadel_addons\\TrueRandom\\scripts\\heroes.vdata", "w") as f:
    f.write(data)
    f.close()
    