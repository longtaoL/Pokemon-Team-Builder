from efficient_apriori import apriori as apr1
from apyori import apriori as apr2
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori as apr3, association_rules


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
mons = []
for team in divided_teams:
    pokemonarray = team.split("\n")[1:7]
    for mon in range(6):
        pokemonarray[mon] = pokemonarray[mon].split(":")[0]
        if pokemonarray[mon] not in mons:
            mons.append(pokemonarray[mon])
    final_teams.append(tuple(pokemonarray))

nums_of_mons = []

for team in final_teams:
    mons_there = []
    for mon in mons:
        if mon in team:
            mons_there.append(True)
        else:
            mons_there.append(False)
    nums_of_mons.append(mons_there)


data = np.array(nums_of_mons)

processed_data = pd.DataFrame(nums_of_mons, columns=mons)

print(processed_data)

# Building the model
frq_items = apr3(processed_data, min_support=0.0000001, use_colnames=True)

# Collecting the inferred rules in a dataframe
rules = association_rules(frq_items, metric="lift", min_threshold=0.0001)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
print(rules)








#for x in final_teams:
#    print(x, end='')
#    print(',')

#itemsets, rules = apr1(final_teams, min_support=0.1, min_confidence=0.1)
#results = list(apr2(final_teams))

"""
ranked_rules = []
for i in range(100):
    itemsets, rules = apr1(final_teams, min_support=0.1 - (i * 0.001), min_confidence=0.1 - (i * 0.001))
    for rule in rules:
        if rule not in ranked_rules:
            ranked_rules.append(rule)
"""

#print(ranked_rules)
#print(results)