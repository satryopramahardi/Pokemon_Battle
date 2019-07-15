import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

stats = pd.read_csv('pokemon.csv')
battle = pd.read_csv('combats.csv')
# stats = stats.set_index('#')

from sklearn import preprocessing

le_type = preprocessing.LabelEncoder()
stats['Type 2']= stats['Type 2'].fillna('ZNOTYPE')
le_type.fit(stats['Type 2'])
stats['Type 1']= le_type.fit_transform(stats['Type 1'])
stats['Type 2']= le_type.fit_transform(stats['Type 2'])

# print(stats.head())
# print(le_type.classes_)

arena = pd.DataFrame(columns=['1#','1type1','1type2','1HP','1Attack','1Defense','1SpAtk','1SpDef','1Speed','1Legendary',
                            '2#','02type1','2type2','2HP','2Attack','2Defense','2SpAtk','2SpDef','2Speed','2Legendary'])

# arena['1#'] = battle['First_pokemon']
# arena['2#'] = battle['Second_pokemon']

fights = []
for i in range(0,len(battle)):
    first_pokemon = battle['First_pokemon'].iloc[i]
    second_pokemon = battle['Second_pokemon'].iloc[i]
    print(f"1st pokemon {first_pokemon}")
    print(f"2nd pokemon {second_pokemon}")
    if battle['Winner'].iloc[i] == first_pokemon:
        winner = True
    else:
        winner = False

    duel = {
        '1#': first_pokemon,
        '1type1': stats[stats['#'] == first_pokemon]['Type 1'].values[0],
        '1type2': stats[stats['#'] == first_pokemon]['Type 2'].values[0],
        '1HP' : stats[stats['#'] == first_pokemon]['HP'].values[0],
        '1Attack': stats[stats['#'] == first_pokemon]['Attack'].values[0],
        '1Defense': stats[stats['#'] == first_pokemon]['Defense'].values[0],
        '1SpAtk': stats[stats['#'] == first_pokemon]['Sp. Atk'].values[0],
        '1SpDef': stats[stats['#'] == first_pokemon]['Sp. Def'].values[0],
        '1Speed': stats[stats['#'] == first_pokemon]['Speed'].values[0],
        '1Legendary': stats[stats['#'] == first_pokemon]['Legendary'].values[0],
        '2#': second_pokemon,
        '2type1': stats[stats['#'] == second_pokemon]['Type 1'].values[0],
        '2type2': stats[stats['#'] == second_pokemon]['Type 2'].values[0],
        '2HP' : stats[stats['#'] == second_pokemon]['HP'].values[0],
        '2Attack': stats[stats['#'] == second_pokemon]['Attack'].values[0],
        '2Defense': stats[stats['#'] == second_pokemon]['Defense'].values[0],
        '2SpAtk': stats[stats['#'] == second_pokemon]['Sp. Atk'].values[0],
        '2SpDef': stats[stats['#'] == second_pokemon]['Sp. Def'].values[0],
        '2Speed': stats[stats['#'] == second_pokemon]['Speed'].values[0],
        '2Legendary': stats[stats['#'] == second_pokemon]['Legendary'].values[0],
        'winner': winner
    }
    fights.append(duel)
    print(duel)

arena = pd.DataFrame(fights)
print(arena.head(20))
print(len(arena))
arena.to_csv("combat_ready.csv",index=False)
