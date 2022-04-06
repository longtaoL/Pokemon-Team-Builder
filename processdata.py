f = open("rawdata.txt", "r")
divided_teams = []
newteam = ""
for line in f:
    if (line == "\n"):
        divided_teams.append(newteam)
        newteam = ""
    else:
        newteam += line

final_teams = []

for team in divided_teams:
    pokemonarray = team.split("\n")[1:7]
    for mon in range(6):
        pokemonarray[mon] = pokemonarray[mon].split(":")[0]
    final_teams.append(tuple(pokemonarray))

print(final_teams)