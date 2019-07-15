from flask import Flask,jsonify,render_template,request,redirect,send_from_directory
import json, requests
import joblib as jb
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# def declare_winner()

app = Flask(__name__)
app.config['upload_folder']='storage'


pokemon = pd.read_csv('pokemon.csv')


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/fight', methods= ['POST','GET'])
def find():
    first_pokemon = str(request.form['first_pokemon']).capitalize()
    second_pokemon = str(request.form['second_pokemon']).capitalize()
    if first_pokemon == '' or second_pokemon =='':
        return redirect('404.html')
    first_pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{first_pokemon.lower()}'
    second_pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{second_pokemon.lower()}'
    first_data = requests.get(first_pokemon_url)
    second_data = requests.get(second_pokemon_url)

    print(first_data.status_code)
    print(second_data.status_code)



    if first_data.status_code == 200 and second_data.status_code==200:
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
        predict_model=jb.load('pokemon_battle.pickle')

        battle_stat=[]
        battle_stat = first_stat + second_stat

        proba=predict_model.predict_proba(np.matrix(battle_stat))
        # print(proba)
        # print(predict_model.predict(np.matrix(battle_stat)))
        pred = predict_model.predict(np.matrix(battle_stat))
        if pred == True:
            winner = first_pokemon
        else:
            winner = second_pokemon
        if proba[0][0]>=proba[0][1]:
            probs = str(proba[0][0]*100)
        else:
            probs = str(proba[0][0]*100)
            
        names = [first_pokemon,second_pokemon]
        hp = [first_pokedex['HP'].values[0],second_pokedex['HP'].values[0]]
        attack = [first_pokedex['Attack'].values[0],second_pokedex['Attack'].values[0]]
        defense = [first_pokedex['Defense'].values[0],second_pokedex['Defense'].values[0]]
        spatk = [first_pokedex['Sp. Atk'].values[0],second_pokedex['Sp. Atk'].values[0]]
        spdef = [first_pokedex['Sp. Def'].values[0],second_pokedex['Sp. Def'].values[0]]
        speed = [first_pokedex['Speed'].values[0],second_pokedex['Speed'].values[0]]

        plt.figure(figsize=(17,10))
        plt.subplot(161)
        plt.bar(names,hp,color=['blue','red'])
        plt.title('HP')
        i=0
        while i<len(names):
            plt.text(names[i],hp[i]-4,f'''{hp[i]}''',fontsize=17)
            i+=1

        plt.subplot(162)
        plt.bar(names,attack,color=['blue','red'])
        plt.title('Attack')
        i=0
        while i<len(names):
            plt.text(names[i],attack[i]-4,f'''{attack[i]}''',fontsize=17)
            i+=1

        plt.subplot(163)
        plt.bar(names,defense,color=['blue','red'])
        plt.title('Defense')
        i=0
        while i<len(names):
            plt.text(names[i],defense[i]-4,f'''{defense[i]}''',fontsize=17)
            i+=1

        plt.subplot(164)
        plt.bar(names,spatk,color=['blue','red'])
        plt.title('Special Attack')
        i=0
        while i<len(names):
            plt.text(names[i],spatk[i]-4,f'''{spatk[i]}''',fontsize=17)
            i+=1

        plt.subplot(165)
        plt.bar(names,spdef,color=['blue','red'])
        plt.title('Special Defense')
        i=0
        while i<len(names):
            plt.text(names[i],spdef[i]-4,f'''{spdef[i]}''',fontsize=17)
            i+=1

        plt.subplot(166)
        plt.bar(names,speed,color=['blue','red'])
        plt.title('Speed')
        i=0
        while i<len(names):
            plt.text(names[i],speed[i]-4,f'''{speed[i]}''',fontsize=17)
            i+=1
        plot=f"./storage/{names[0]}vs{names[1]}.png"
        plot_url=f"http://localhost:5000/upload/{names[0]}vs{names[1]}.png"
        plt.savefig(plot)

        first_pic = first_data.json()['sprites']['front_default']
        second_pic = second_data.json()['sprites']['front_default']
        
        response_dat = []
        response_dat = [first_pokemon,second_pokemon,first_pic,second_pic,winner,probs,plot_url]
        # print(plot_url)
        print("=================================")
        print(first_pic)
        print("=================================")
        # print(second_pic)
        # return response_dat
        return render_template("result.html",result = response_dat)
    else:
        return redirect('404.html')

@app.route('/upload/<path:x>')
def upload_file(x):
    return send_from_directory('storage',x)

@app.errorhandler(404)
def notFound(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug = True)
