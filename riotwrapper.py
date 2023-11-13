import os
import requests
import json
Rapi_key = "null"

class RiotWrapper:
    def checkAPI(self):
        if Rapi_key == "null":
            raise Exception("Riot API key is not defined")

    #Used for throwing an exception when the API key is missing

    def getSummonerData(self, name, region):
        self.checkAPI()
        request_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        constructed_url = request_url + name + '?api_key=' + Rapi_key
        response = requests.get(constructed_url)
        rawdata = response.json()
        playerdata = {
            "name": rawdata["name"],
            "id": rawdata["id"],
            "accountid": rawdata["accountid"],
            "summonerLevel": rawdata["summonerlevel"],
            "iconid": rawdata["profileIconId"],
            "puuid": rawdata["puuid"],
            "revisionDate": rawdata["revisionDate"]
        }
        return playerdata

    def getRmatches(self, region, puuid, count):
        self.checkAPI()
        constructed_url = "https://" + str(region) + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) + "/ids?start=0&count=" + str(count) + "&api_key=" + str(Rapi_key)
        response = requests.get(constructed_url)
        rawdata = response.json()
        return rawdata

    def getMatchStats(self, matchid, region):
        self.checkAPI()
        constructed_url = "https://" + str(region.upper()) + ".api.riotgames.com/lol/match/v5/matches/" + str(matchid) + "?api_key=" + Rapi_key
        response = requests.get(constructed_url)
        responsebody = response.json()
        #print(responsebody)  #for debugging purposes lol
        rawMetadata = responsebody["metadata"]
        rawInfo = responsebody["info"]
        participants_id = {}

        #Participants in metadata
        for i, v in enumerate(rawMetadata["participants"]):
            participants_id[f"player_{i + 1}"] = v
        #print(participants) //debug print for printing the participants list seperatley

        #Participants in metadata
        playerstats = {
            "player_1": rawInfo["participants"][0],
            "player_2": rawInfo["participants"][1],
            "player_3": rawInfo["participants"][2],
            "player_4": rawInfo["participants"][3],
            "player_5": rawInfo["participants"][4],
            "player_6": rawInfo["participants"][5],
            "player_7": rawInfo["participants"][6],
            "player_8": rawInfo["participants"][7],
            "player_9": rawInfo["participants"][8],
            "player_10": rawInfo["participants"][9],
        }

        #Final dictionary
        matchStats = {
            "gameDuration": rawInfo["gameDuration"],
            "gameEndTimestamp": rawInfo["gameEndTimestamp"],
            "gameId": rawInfo["gameId"],
            "gameMode": rawInfo["gameMode"],
            "gameName": rawInfo["gameName"],
            "gameStartTimestamp": rawInfo["gameStartTimestamp"],
            "gameType": rawInfo["gameType"],
            "gameVersion": rawInfo["gameVersion"],
            "mapId": rawInfo["mapId"],
            "participants_sid": participants_id,
            "platformId": rawInfo["platformId"],
            "queueId": rawInfo["queueId"],
            "teams": rawInfo["teams"],
            "tournamentCode": rawInfo["tournamentCode"],
            "playerstats": playerstats
        }
        return matchStats



