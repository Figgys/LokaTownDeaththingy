import requests
import json
'''
This is horrible code mostlikely just like everything else in this project but its here cause i think its cool to see the difference between how much faster it is when you cache vs dont
'''

responseTowns = requests.get('https://api.lokamc.com/towns/search/findDeleted')

deletedTowns = {"seenTowns": []}
currentNum = 0


returnedWorldSearchWest = {}
returnedWorldSearchSouth = {}
returnedWorldSearchNorth = {}

def getBiome(tileNum, world) :

    responseWorldSearch = requests.get(f'https://api.lokamc.com/territories/search/findByWorld?world={world}')

    if world == "west":
        cache = returnedWorldSearchWest
    if world == "north":
        cache = returnedWorldSearchNorth
    if world == "south":
        cache = returnedWorldSearchSouth


    if not cache:
        cache = responseWorldSearch.json()


    for tile in cache['_embedded']['territories'] :
       if str(tile.get('num')) == str(tileNum):
           return str(tile.get('areaName'))



def appendToList() : 
    for town in responseTowns.json()['_embedded']['towns'] :

        name = town['name']
        world = town["world"]
        tileNum = town["territoryNum"]
        biomeName = getBiome(tileNum, world)

        global currentNum
        currentNum += 1
        print(name, world, tileNum, biomeName, currentNum)

        newTownJsonFormat = {
            'name': name, 
            "location": {
                "world" : world,
                "tileNumber": tileNum,
                "biome": biomeName
                }
            }
    
        deletedTowns['seenTowns'].append(newTownJsonFormat)

appendToList()

with open('seenTowns.json', 'w') as file:
    json.dump(deletedTowns, file, indent=4)
    print("Now in file")
