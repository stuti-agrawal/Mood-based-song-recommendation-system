from flask import Flask, render_template, request
import spotipy
import numpy as np
import pandas as pd
import tekore as tk
from tqdm import tqdm
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyClientCredentials
import os
import spotipy.util as util
import ast

# ===============================================
# app.py
# ------------
# reads json data to send to viewer
# ===============================================

# creating a Flask app
app = Flask(__name__, static_folder='./static', template_folder='./static')

@app.route('/', methods = ['POST'])
@cross_origin("http://localhost:3000") # CORS access

def mood_values():
    # moods dict stores the values of different moods that the user inputs
    moods_dict = {}
    mood_values_ = request.get_json()
    moods_dict["happy_value"] = mood_values_["happy_value"]
    moods_dict["sad_value"] = mood_values_["sad_value"]
    moods_dict["angry_value"] = mood_values_["angry_value"]
    moods_dict["romantic_value"] = mood_values_["romantic_value"]
    moods_dict["anxious_value"] = mood_values_["anxious_value"]
    
    spotify = auth()
    genres = spotify.recommendation_genre_seeds()
    data_dict = {
    "id":[], 
    "track_name":[], 
    "artist_name":[],
    "valence":[],     
    "energy":[],      
    "danceability": []
    }
    
    # choose only genres for pop, hiphop, chill, indiepop, indie, rock, and sad, respectively
    genrez = [genres[86], genres[52], genres[16], genres[58], genres[59], genres[99], genres[103]]
    
    # Get recommendation for each genre
    for gender in tqdm(genrez):
        
        recs = spotify.recommendations(genres = [gender], limit = 7)
        #changed from eval for security issues
        recs = ast.literal_eval(recs.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]
    
    for track in recs:
        data_dict["id"].append(track["id"])
        track_meta = spotify.track(track["id"])
        data_dict["track_name"].append(track_meta.name)
        data_dict["artist_name"].append(track_meta.album.artists[0].name)
        track_features = sp.audio_features(track["id"])
        data_dict["valence"].append(track_features[0]['valence'])
        data_dict["energy"].append(track_features[0]['energy'])
        data_dict["danceability"].append(track_features[0]['danceability'])

    # Store data in pandas dataframe
    df = pd.DataFrame(data_dict)

    # Drop duplicates
    df.drop_duplicates(subset = "id", keep = "first", inplace = True)
    df.to_csv("arousal_dataset.csv", index = False)

    #mood 1 = happy, mood 2 = sad, mood 3 = angry, mood 4 = romantic, mood 5 = anxious

    #Obtain values from website
    moods = [ mood_values_["happy_value"], mood_values_["sad_value"], mood_values_["angry_value"], mood_values_["romantic_value"], mood_values_["anxious_value"]]
    #Scale down to 50 (originally slider only went to 50, new slider goes to 100)
    for i in moods:
      i = (i / (float)(100)) * 50
      
    moodvals = np.array(moods)

    # valence = 1.0 correlates with happiness and positve emotions, 0.0 correlates with negative emotions
    # start with neutral score of 0.5
    # happiness and sadness have most impact, other emotions have half as much impact
    valenceval = 0.5
    
    # if happiness is 50, can get max of 1.0
    valenceval = valenceval + (moodvals[0] * 0.01)  - (moodvals[1] * 0.01) - (moodvals[2] * 0.005) + (moodvals[3] * 0.005) - (moodvals[4] * 0.005)
    
    # max val is 50 happiness, 50 romantic, so divide by 75 as max value
    if valenceval < 0:
        valenceval = 0.0

    # energy = 1.0 correlates with intensity, like death metal, 0.0 correlates with mellowness
    # here, we base energy value on happiness and anger only
    # start with base value 0.5
    # if happiness and anger maxed, get 1.0
    energyval = 0.5
    energyval = energyval + (moodvals[0] * 0.005) + (moodvals[1] * 0.005) 

    # danceability = 1.0 correlates with most danceable, 0.0 correlates with least danceable
    # start w/ neutral val 0.5, subtract based on sadness, anxious, anger, romantic
    # here, we base danceability on happiness, but want less danceable songs based on if you are sad, angry, or anxious
    danceabilityval = 0.5
    danceabilityval = danceabilityval - (moodvals[1] * 0.0025) - (moodvals[2] * 0.005) - (moodvals[4] * 0.0025)
    if danceabilityval < 0:
        danceabilityval = 0.0
    return get_song(df, valenceval, energyval, danceabilityval)


def auth():
  client_id  = "983bdba20e524ca997c58d8250b088d9"
  secret_key = "d787de6d91b2409b9a68467558c5f7fb"
  token = tk.request_client_token(client_id, secret_key)
  return tk.Spotify(token)

client_id  = "983bdba20e524ca997c58d8250b088d9"
client_secret = "d787de6d91b2409b9a68467558c5f7fb"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

def get_song(df, valenceval, energyval, danceabilityval):
    foundSong = False
    for i in range(6):
        optimalValence = (df.loc[i].at["valence"] > valenceval - 0.1 and df.loc[i].at["valence"] <= valenceval + 0.1)
        optimalEnergy = (df.loc[i].at["energy"] > energyval - 0.1 and df.loc[i].at["energy"] <= energyval + 0.1)
        optimalDance = (df.loc[i].at["danceability"] > danceabilityval - 0.1 and df.loc[i].at["danceability"] <= danceabilityval + 0.1)
        if (optimalValence and optimalEnergy and optimalDance):
            foundSong = True
            print(df.loc[i].at["artist_name"], end = "  - ")
            print(df.loc[i].at["track_name"], end = " ")
            print ("https://open.spotify.com/track/", end="")
            print (df.loc[i].at["id"])
            return "https://open.spotify.com/track/"+ df.loc[i].at["id"]
    if not foundSong: 
      # try again with larger margins
        for i in range(6):
            optimalValence = (df.loc[i].at["valence"] > valenceval - 0.3 and df.loc[i].at["valence"] <= valenceval + 0.3)
            optimalEnergy = (df.loc[i].at["energy"] > energyval - 0.3 and df.loc[i].at["energy"] <= energyval + 0.3)
            optimalDance = (df.loc[i].at["danceability"] > danceabilityval - 0.3 and df.loc[i].at["danceability"] <= danceabilityval + 0.3)
            if (optimalValence and optimalEnergy and optimalDance):
                foundSong = True
                print(df.loc[i].at["artist_name"], end = " - ")
                print(df.loc[i].at["track_name"], end = " ")
                print ("https://open.spotify.com/track/", end="")
                print(df.loc[i].at["id"])
                return "https://open.spotify.com/track/"+ df.loc[i].at["id"]
    if not foundSong:
        print("Rick Astley", end = " - ")
        print("Never Gonna Give You Up", end = " ")
        return "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"

def get_data_dict() :
    spotify = auth()
    genres = spotify.recommendation_genre_seeds()
    data_dict = {
    "id":[], 
    "track_name":[], 
    "artist_name":[],
    "valence":[],     
    "energy":[],      
    "danceability": []
    }
    
    # choose only genres for pop, hiphop, chill, indiepop, indie, rock, and sad, respectively
    genrez = [genres[86], genres[52], genres[16], genres[58], genres[59], genres[99], genres[103]]
    
    # Get recommendation for each genre
    for gender in tqdm(genrez):
        
        recs = spotify.recommendations(genres = [gender], limit = 7)
        recs = eval(recs.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]
    
    for track in recs:
        data_dict["id"].append(track["id"])
        track_meta = spotify.track(track["id"])
        data_dict["track_name"].append(track_meta.name)
        data_dict["artist_name"].append(track_meta.album.artists[0].name)
        track_features = sp.audio_features(track["id"])
        data_dict["valence"].append(track_features[0]['valence'])
        data_dict["energy"].append(track_features[0]['energy'])
        data_dict["danceability"].append(track_features[0]['danceability'])

    return data_dict

app.run(debug=True)