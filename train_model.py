import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_training = pd.read_csv('combat_ready.csv')

X= data_training.drop(['winner'],axis = 1)
y= data_training.winner

from sklearn.ensemble import RandomForestClassifier
rand_forest=RandomForestClassifier()
rand_forest.fit(np.matrix(X),y)


import joblib as jb
jb.dump(rand_forest,'pokemon_battle.pickle')

first_pokemon='Groudon'
second_pokemon='Kyogre'

pokemon = pd.read_csv('pokemon.csv')

from sklearn import preprocessing
le_type = preprocessing.LabelEncoder()
pokemon['Type 2']= pokemon['Type 2'].fillna('ZNOTYPE')
le_type.fit(pokemon['Type 2'])
pokemon['Type 1']= le_type.fit_transform(pokemon['Type 1'])
pokemon['Type 2']= le_type.fit_transform(pokemon['Type 2'])


first_pokedex = pokemon[pokemon['Name']==first_pokemon]
second_pokedex = pokemon[pokemon['Name']==second_pokemon]




first_stat =[first_pokedex['#'].values[0],first_pokedex['Type 1'].values[0],first_pokedex['Type 2'].values[0],first_pokedex['HP'].values[0],first_pokedex['Attack'].values[0],first_pokedex['Defense'].values[0],first_pokedex['Sp. Atk'].values[0],first_pokedex['Sp. Def'].values[0],first_pokedex['Speed'].values[0],first_pokedex['Legendary'].values[0]]
second_stat =[second_pokedex['#'].values[0],second_pokedex['Type 1'].values[0],second_pokedex['Type 2'].values[0],second_pokedex['HP'].values[0],second_pokedex['Attack'].values[0],second_pokedex['Defense'].values[0],second_pokedex['Sp. Atk'].values[0],second_pokedex['Sp. Def'].values[0],second_pokedex['Speed'].values[0],second_pokedex['Legendary'].values[0]]

battle_stat=[]
battle_stat = first_stat + second_stat

# print(rand_forest.predict_proba(np.matrix(battle_stat)))
# print(rand_forest.predict(np.matrix(battle_stat)))