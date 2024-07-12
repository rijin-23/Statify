import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import pandas as pd
import datetime as dt

import Artists_names as artistsNames
import secret_keys as clientKeys

#The following function will return authentication token if the response is 200 else it throws an error.
def get_spotify_auth_code(clientId, clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type":"client_credentials",
        "client_id": clientId,
        "client_secret": clientSecret
    }

    response = requests.post(url, headers = headers, data = data)

    if response.status_code == 200:
        req_data = response.json()
        return req_data
    else:
        raise Exception(f"Failed to get the Token {response.status_code}, {response.reason}")
    
secretKeys = clientKeys.Secret_keys()
client_id = secretKeys.client_id
client_secret = secretKeys.client_secret

#The token is fetched which is a JSON
token_json = get_spotify_auth_code(clientId=client_id, clientSecret=client_secret)


#Token and token type is stored which is essential for API calls
access_token = token_json["access_token"]
token_type = token_json["token_type"]

def apiRequest(artistName, token_type, access_token):
    url = f"https://api.spotify.com/v1/search?q={artistName}&type=artist"
    headers = {
        "Authorization" : f"{token_type}  {access_token}"
    }
    artistResponse = requests.get(url, headers = headers)

    if artistResponse.status_code == 200:
        artist_data = artistResponse.json()
        return artist_data
    else:
        raise Exception (f"An error occurred, {artistResponse.status_code}, {artistResponse.reason}")

artist_data = {
    "SpotifyID" : [],
    "ArtistName": [],
    "Followers" : [],
    "Popularity" : [],
    "ImageURL" : [],
    "Genres": [],
    "DateTime": []
    }

def artistDataProcessing(artist_details):
    artist_data['SpotifyID'].append(artist_details['artists']['items'][0]['id'])
    artist_data['ArtistName'].append(artist_details['artists']['items'][0]['name'])
    artist_data['Followers'].append(artist_details['artists']['items'][0]['followers']['total'])
    artist_data['Popularity'].append(artist_details['artists']['items'][0]['popularity'])
    artist_data['ImageURL'].append(artist_details['artists']['items'][0]['images'][0]['url'])
    artist_data['Genres'].append(artist_details['artists']['items'][0]['genres'])
    artist_data['DateTime'].append(dt.datetime.now())

ArtistNamesObj = artistsNames.Artist_Names()
namesData = ArtistNamesObj.names

for name in namesData:
    artistDetails = apiRequest(name.replace(" ","+"), token_type, access_token)
    artistDataProcessing(artist_details=artistDetails)

artistDf = pd.DataFrame(artist_data)

artistDf.to_csv('Artists_Data.csv')