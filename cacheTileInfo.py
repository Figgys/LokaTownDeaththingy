import requests
import json

def doesCacheExist(cacheName : str) :
    if cacheName not in ("west", "north", "south") :
        print(f"Cache name of {cacheName}, Invalid param should be; west, south or north")
        return True
    
    try:
        with open(f"{cacheName}.json") as file:
            cache = file.read()
        return True
    except FileNotFoundError:
        print(f"File of {cacheName}.json does not exist.")
        print("Attempting to generate new one rerun program once its complete")
        with open(f"{cacheName}.json", "w") as file:
            file.write(json.dumps({f"{cacheName}Cache": {}}, indent=5))
        return False
    

def generateData(world: str) :
        seenTiles = {"cache": []}
        if doesCacheExist(world) == False :
            responseWorldSearch = requests.get(f'https://api.lokamc.com/territories/search/findByWorld?world={world}')
            for tile in responseWorldSearch.json()["_embedded"]["territories"]:
                    
                    biomeLoc = tile['areaName']
                    tileNum = tile['num']
                    if tile["tg"] is not None and 'beacon' in tile["tg"] :
                        tgenList = tile['tg']['beacon']
                        loc,x,y,z = tgenList.split(",")
                    else :
                        x,y,z = None, None, None


                    newJsonFormat = {
                                "tileNumber": tileNum,
                                "location": {
                                    "biome": biomeLoc,
                                        "tgen": {
                                            "x": x,
                                            "y": y,
                                            "z": z
                                        }
                                    }
                                }
                    
                    seenTiles["cache"].append(newJsonFormat)

            with open(f'{world}.json', 'w') as file:
                json.dump(seenTiles, file, indent=4)
                print("Now in file")

def pullFromCache(world: str, tileNum: str) :
    if doesCacheExist(world) == True :
            with open(f"{world}.json", "r") as file:
                cacheRead = json.load(file)
            for tile in cacheRead['cache'] :
                 if str(tile['tileNumber']) == str(tileNum) :
                      list = f"{tile['location']['biome']},{tile['location']['tgen']['x']},{tile['location']['tgen']['y']},{tile['location']['tgen']['z']}"
                      return list
                 
generateData("west")
generateData("north")
generateData("south")
