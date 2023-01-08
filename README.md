# course-project-group-26
course-project-group-26 created by GitHub Classroom
# Moodify - Mood Based Song Recommendation System

People experience all sorts of emotions throughout the day, and the Mood-Based Song Recommendation Web application "Moodify" strives to uplift or complement these feelings by recommending a song. Users are able to use sliders to increase or decrease the levels of happiness, sadness, anger, romance, and anxiety they feel that day. In return, they will receive a song, artist, and link/URL from our music library that was calculated from the average of the emotional values, with the heaviest emphasis on happiness and sadness. "Moodify" allows people to be more in touch with their emotions and how they feel on a day-to-day basis by offering a new song to listen to that reflects their mood.

Developers:

Stuti Agrawal: stutia3@illinois.edu

Lisa Leung: ljleung2@illinois.edu

Haley Shah: hmshah2@illinois.edu

Libby Codamon: ecoda2@illinois.edu

Mentor: Ryan Ziegler

Front-end: React Framework

Back-end: Python

# Technical Architecture

Backend (Haley, Lisa, Libby):
The backend was done completely in python using the spotipy library which is a lightweight version of the spotify api.

We took a secret id and client id credentials from the spotify developers page. These credentials were used to authorize and create a spotify object. From this, we took a recommendation of genres, selected a select few genres- the ones that are most popular nowadays. Then we find recommendations for each of the genres, add the data for each into a dictionary which we converted into a pandas dataframe then into a csv for easy accessibility throughout our code.

We take in an array of mood values (this is based on the slider data from the frontend). From there, we calculate the valence, energy, and danceability values (the main components of song that differentiates it from others)- each on a scale from 0 to 1.

valence = 1.0 correlates with happiness and positive emotions, 0.0 correlates with negative emotions
energy = 1.0 correlates with intensity, like death metal, 0.0 correlates with mellowness- like chill songs of a lower tempo
danceability = 1.0 correlates with most danceable, 0.0 correlates with least danceable

Then, we search through the data csv for a song that has these values and it will return one of three things. Using our getSong function with inputs: dataframe, valenceval, energyval, and danceabilityval, we are able to calculate a song from our data library that best correlates with the values. 

1. If a song is found with optimal valence, energy, and dance values, then a song from our library and genre selection will be outputted with the song title, artist, and a link/URL to the song. 

2. If a song is not easily found with the given values, our getSong function will then use larger margins for the optimal valence, energy, and dance values to calculate and return a song title, artist, and link/URL. 

3. Finally, if the values combined are inconclusive and a song cannot be found in our library, then the song “Never Gonna Give You Up” by Rick Astley will be outputted with a link/URL.


Frontend (Stuti):
Users are able to use sliders to increase/decrease on 5 emotions (happy, sad, angry, romantic, anxious) to display what levels of each they are feeling that day. The data that is submitted by the user is then sent to the backend which finds a song and sends it back to the frontend which displays a song, artist, and link/URL. We have also included a video on the final screen about the correlation between music and moods/feelings as the inspiration for our course project. 


## Virtual environment 
We are using a virtual environment for developing this project and to manage dependencies. To start the virtual environment run the following commands from the root directory:

Windows:
```
source venv/Scripts/activate
```

Mac:
```
source venv/bin/activate
```

## To start an instance of the Web App

for the first run:
```
cd static
npm install
```

for subsequent runs:
```
cd static
npm start
```
