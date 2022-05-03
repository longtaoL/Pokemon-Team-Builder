import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori as apr3, association_rules
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

spark = SparkSession.builder.getOrCreate()

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

rules["antecedents"] = rules["antecedents"].apply(list)
rules["consequents"] = rules["consequents"].apply(list)
# print(rules)

# from pyspark.sql.types import *
# schema = StructType([
#           StructField("antecedents",ArrayType(StringType(),True),True),
#           StructField("consequents",ArrayType(StringType(),True),True),
#           StructField("antecedent support",FloatType(),True),
#           StructField("consequent support",FloatType(),True),
#           StructField("support",FloatType(),True),
#           StructField("confidence",FloatType(),True),
#           StructField("lift",FloatType(),True),
#           StructField("leverage",FloatType(),True),
#           StructField("conviction",FloatType(),True)])
df = spark.createDataFrame(rules)

df.createOrReplaceTempView("association_rules")
ordered_rules = spark.sql("select * from association_rules ORDER BY (confidence,lift) DESC").createOrReplaceTempView("ordered_view")

step_one = """
          SELECT consequents 
          FROM ordered_view 
          WHERE array_contains(antecedents,{pokemon1})
              AND cardinality(antecedents) = {arr_size}
          ORDER BY ("confidence","lift")
         """
step_two = """
          SELECT consequents 
          FROM ordered_view 
          WHERE array_contains(antecedents,{pokemon1})
              AND array_contains(antecedents,{pokemon2})
              AND cardinality(antecedents) = {arr_size}
          ORDER BY ("confidence","lift")
         """
step_three = """
          SELECT consequents 
          FROM ordered_view 
          WHERE array_contains(antecedents,{pokemon1})
              AND array_contains(antecedents,{pokemon2})
              AND array_contains(antecedents,{pokemon3})
              AND cardinality(antecedents) = {arr_size}
          ORDER BY ("confidence","lift")
         """
step_four = """
          SELECT consequents 
          FROM ordered_view 
          WHERE array_contains(antecedents,{pokemon1})
              AND array_contains(antecedents,{pokemon2})
              AND array_contains(antecedents,{pokemon3})
              AND array_contains(antecedents,{pokemon4})
              AND cardinality(antecedents) = {arr_size}
          ORDER BY ("confidence","lift")
         """
step_five = """
          SELECT consequents 
          FROM ordered_view 
          WHERE array_contains(antecedents,{pokemon1})
              AND array_contains(antecedents,{pokemon2})
              AND array_contains(antecedents,{pokemon3})
              AND array_contains(antecedents,{pokemon4})
              AND array_contains(antecedents,{pokemon5})
              AND cardinality(antecedents) = {arr_size}
          ORDER BY ("confidence","lift")
         """

#build a pokemon team step by step

input_pokemon = input("What are your initial Pokemon? Please separate by comma: ")
final_choices = input_pokemon.split(",")

#continue running until there are 6 pokemons on the team
while(len(final_choices) < 6):
  #run the SQL queries in different scenarios
  if len(final_choices) == 1:
    suggestions = spark.sql(step_one.format(pokemon1='"%s"'%final_choices[0],arr_size=len(final_choices))).collect()
  elif len(final_choices) == 2:
    suggestions = spark.sql(step_two.format(pokemon1='"%s"'%final_choices[0],pokemon2='"%s"'%final_choices[1],arr_size=len(final_choices))).collect()
  elif len(final_choices) == 3:
    suggestions = spark.sql(step_three.format(pokemon1='"%s"'%final_choices[0],pokemon2='"%s"'%final_choices[1],pokemon3='"%s"'%final_choices[2],arr_size=len(final_choices))).collect()
  elif len(final_choices) == 4:
    suggestions = spark.sql(step_four.format(pokemon1='"%s"'%final_choices[0],pokemon2='"%s"'%final_choices[1],pokemon3='"%s"'%final_choices[2],pokemon4='"%s"'%final_choices[3],arr_size=len(final_choices))).collect()
  elif len(final_choices) == 5:
    suggestions = spark.sql(step_five.format(pokemon1='"%s"'%final_choices[0],pokemon2='"%s"'%final_choices[1],pokemon3='"%s"'%final_choices[2],pokemon4='"%s"'%final_choices[3],pokemon5='"%s"'%final_choices[4],arr_size=len(final_choices))).collect()
  cur_index = 0
  pick = suggestions[cur_index][0]

  #added the accept/reject functionality
  print("Based your current team draft, our suggestion is ")
  print(pick)
  decision = input("Do your want to accept it or try a new suggestion? (accept/reject): ")
  while(decision != "accept"):
    cur_index += 1
    pick = suggestions[cur_index][0]
    print("Here is another recommendation ")
    print(pick)
    decision = input("Do your want to accept it or try a new suggestion? (accept/reject): ")
  #add the recommended pokemon to the team
  if len(pick)==1:
    final_choices.append(pick[0])
  else:
    for item in pick:
      final_choices.append(item)
  print("Your current draft is: ")
  print(final_choices)

# temp1 = spark.sql("""
#           SELECT * 
#           FROM ordered_view 
#           WHERE array_contains(antecedents,"Landorus-Therian")
#               AND array_contains(antecedents,"Heatran")
#               AND array_contains(antecedents,"Kartana")
#               AND cardinality(antecedents) = 3
#           ORDER BY ("confidence","lift")
#          """).show()