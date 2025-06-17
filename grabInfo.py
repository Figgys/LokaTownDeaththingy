import requests
import json
from cacheTileInfo import pullFromCache


responseTowns = requests.get('https://api.lokamc.com/towns/search/findDeleted')

deletedTowns = {"seenTowns": []}
currentNum = 0

def appendToList() : 
    for town in responseTowns.json()['_embedded']['towns'] :

        name = town['name']
        world = town["world"]
        tileNum = town["territoryNum"]
        list = pullFromCache(world, tileNum)
        biome,x,y,z = list.split(",")

        global currentNum
        currentNum += 1
        print(name, world, tileNum, biome, x, y, z, currentNum)

        newTownJsonFormat = {
            'name': name, 
            "location": {
                "world" : world,
                "tileNumber": tileNum,
                "biome": biome,
                "x": x,
                "y": y,
                "z": z
                }
            }
    
        deletedTowns['seenTowns'].append(newTownJsonFormat)

appendToList()

with open('seenTowns.json', 'w') as file:
    json.dump(deletedTowns, file, indent=4)
    print("Now in file")
