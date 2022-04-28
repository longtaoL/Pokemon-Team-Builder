import json, os

path = 'C:/Users/User/Downloads/gen8vgc2022/'
dirs = os.listdir(path)

teams = []
skills = set()

def processPokemon(file):

    with open(path + file, 'r', encoding='UTF-8') as f:
        data = json.load(f)

    for k, v in data.items():
        if k == 'p1team' or k == 'p2team':
            team = []
            for pokemon in v:
                info = {}
                info['species'] = pokemon['species']
                info['item'] = pokemon['item']
                info['ability'] = pokemon['ability']
                info['nature'] = pokemon['nature']
                info['moves'] = pokemon['moves']
                for move in pokemon['moves']:
                    skills.add(move)
                info['evs'] = pokemon['evs']
                info['ivs'] = pokemon['ivs']
                team.append(info)
            teams.append(team)


def writeJson(n):
    result = {}
    result['teams'] = teams
    
    with open('pokemonTeams' + str(n) + '.json', 'w') as out:
        json.dump(result, out)


i = 0
num = 0
for file in dirs:
    processPokemon(file)
    if i % 10000 == 0:
        print(i)
    if i % 100000 == 0 and i != 0:
        writeJson(num)
        teams = []
        num += 1
    i += 1

writeJson(num)

print("json merged")

n = 0
f = open('skills.txt', 'w')
for skill in skills:
    f.write(str(n) + ' ' + skill + '\n')
    n += 1
f.close()

print("skill recorded")

print("finished")
