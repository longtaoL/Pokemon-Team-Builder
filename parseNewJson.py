import json, os

path = 'C:/Users/User/Desktop/csgy6943/project/newData/'
dirs = os.listdir(path)

teams = []
skills = set()

def processPokemon(file):

    with open(path + file, 'r', encoding='UTF-8') as f:
        data = json.load(f)

        for team in data['teams']:
            tmp = []
            for pokemon in team:
                tmp.append(pokemon['species'])
            tmp.sort()
            teams.append(tmp)


def writeJson(suffix):
    result = {}
    result['teams'] = teams

    with open('pokemonTeams' + str(suffix) + '.json', 'w') as out:
        json.dump(result, out)

i = 1
for file in dirs:
    processPokemon(file)
    print('finish ' + str(i))
    i += 1

writeJson('All')

print('done')
