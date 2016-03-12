# Las llamadas al Static data
from APIKeyFile import APIKey
import requests

def requestStaticChampion(userData):#Usamos True en dataById para listar por ID
    region =  str(userData[4])
    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion?dataById=true&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestStaticItem(userData):
    region =  str(userData[4])
    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/item?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestStaticSpells(userData):#Usamos True en dataById para listar por ID
    region =  str(userData[4])
    URL = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/summoner-spell?dataById=True&api_key=" + APIKey
    response = requests.get(URL)
    return response.json()
