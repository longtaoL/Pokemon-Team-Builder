import json, os

path = os.path.join(os.path.expanduser('~'), 'Documents', 'dataComplete')
dirs = os.listdir(path)

setsOrdered = {}
setsLookup = {}
movesLookup = {}
teamsList = []

moves = open("skills.txt", "r")
for line in moves:
    sLine = line.split(" ", 1)
    movesLookup[sLine[1][:-1]] = int(sLine[0])

def writeJson():
    print("\nWriting Json output...")
    result = {}
    result['teams'] = teamsList

    jsonPath = os.path.join(os.path.expanduser('~'), 'Documents', 'processedDataHere', 'pokemonTeamProcessed.json')
    with open(jsonPath, 'w') as out:
        json.dump(result, out)
    print("Json output complete!")

def writePokemonFile():
    length = len(setsOrdered)
    print("\nCreating " + str(length) + " Pokemon Entries...")
    for k, v in setsOrdered.items():
        i += 1
        textPath = os.path.join(os.path.expanduser('~'), 'Documents', 'processedDataHere', 'pokemonSets', k + '.txt')
        textFile = open(textPath, 'w')
        for i in range(len(v)):
            textFile.write(str(i) + " " + str(v[i]) + "\n")
        textFile.close()
    print("Pokemon entries complete!")

def sortMoves(moveList):
    newList = []
    for move in moveList:
        newList.append([movesLookup[move], move])
    for i in range(1, len(newList)):
        key_item = newList[i]
        j = i-1
        while j >= 0 and newList[j][0] > key_item[0]:
            newList[j+1] = newList[j]
            j -= 1
        newList[j+1] = key_item
    for i in range(0, len(newList)):
        newList[i] = newList[i][1]
    return newList

n = 0
for dir in dirs:
    print("Processing file " + dir + "...")
    with open(path + "/" + dir, 'r', encoding='UTF-8') as f:
        data = json.load(f)
        for k, v in data.items():
            for team in v:
                newTeam = []
                for poke in team:
                    pokeList = [poke['species'], poke['item'], poke['ability']]
                    for move in poke['moves']:
                        pokeList.append(move)
                    pokeList = pokeList[0:3] + sortMoves(pokeList[3:])
                    pokeTuple = tuple(pokeList)
                    if pokeTuple[0] not in setsOrdered:
                        setsOrdered[pokeTuple[0]] = [pokeList[1:]]
                        setsLookup[pokeTuple] = 0
                        newTeam.append(pokeTuple[0] + "_0")
                    elif pokeTuple not in setsLookup:
                        length = len(setsOrdered[pokeTuple[0]])
                        setsOrdered[pokeTuple[0]].append(pokeList[1:])
                        setsLookup[pokeTuple] = length
                        newTeam.append(pokeTuple[0] + "_" + str(length))
                    else:
                        newTeam.append(pokeTuple[0] + "_" + str(setsLookup[pokeTuple]))
                teamsList.append(newTeam)

print("Processing files complete!")
writeJson()
writePokemonFile()