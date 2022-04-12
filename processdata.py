import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori as apr3, association_rules

f = open("rawdata.txt", "rb")
divided_teams = []
newteam = ""
#put all teams(raw data) in an array
for line in f:
    line = line.decode("utf-8")
    if (line == "\n"):
        divided_teams.append(newteam)
        newteam = ""
    else:
        newteam += line 
#put all pokemon teams in an array
final_teams = []
mons = []
for team in divided_teams:
    pokemonarray = team.split("\n")[1:7]
    for mon in range(6):
        pokemonarray[mon] = pokemonarray[mon].split(":")[0]
        #keep track of all pokemons appeared
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

# Building the model
frq_items = apr3(processed_data, min_support=0.0000001, use_colnames=True)

# Collecting the inferred rules in a dataframe
rules = association_rules(frq_items, metric="lift", min_threshold=0.0001)
rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
# print(rules)

#build a pokemon team step by step

input_pokemon = input("Input Pokemon would you like to use, separated by comma: ")
final_choices = input_pokemon.split(",")

#continue running until there are 6 pokemons on the team
while(len(final_choices) < 6):
    #find the match 
    resulting_rules = rules[(rules["antecedents"]==frozenset(final_choices))]
    #resort the rules based on confidence and lift in descending order
    resulting_rules = resulting_rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    #get the suggested pokemon
    suggestion = list(resulting_rules["consequents"].iloc[0])[0]
    #add the suggestion
    final_choices.append(suggestion)

print("\n")
print(final_choices)
print("\n")

Landorus_Therian_rules = rules[(rules["antecedents"]==frozenset(["Landorus-Therian"]))]
print(Landorus_Therian_rules[['antecedents', 'consequents', 'confidence', 'lift']])
#Weavile is the first suggestion with highest confidence and lift

# L_W_rules = rules[(rules["antecedents"]==frozenset(["Landorus-Therian","Weavile"]))]
# L_W_rules = L_W_rules.sort_values(['confidence', 'lift'], ascending=[False, False])
# print(L_W_rules)
# #Ferrothorn does not seem to be the suggestion with highest confidence and lift, but it is ranked 1st even after resorting. 

# L_W_F_rules = rules[(rules["antecedents"]==frozenset(["Landorus-Therian","Weavile","Ferrothorn"]))]
# L_W_F_rules = L_W_F_rules.sort_values(['confidence', 'lift'], ascending=[False, False])
# print(L_W_F_rules)
# #Tapu Fini is not the suggestion with highest confidence and lift, but it is ranked 1st even after resorting

# L_W_F_T_rules = rules[(rules["antecedents"]==frozenset(["Landorus-Therian","Weavile","Ferrothorn","Tapu Fini"]))]
# print(L_W_F_T_rules)
# #Zapdos does not seem to be the suggestion with highest confidence and lift, but it is ranked first, even after resorting