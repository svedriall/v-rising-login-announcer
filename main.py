from collections import UserList
import time
from datetime import datetime as dt
from rcon.source import Client
import requests
from discord import Webhook, RequestsWebhookAdapter
import re

userlist = {}

def sendDiscordMessage(message):
    webhook = Webhook.from_url("your-url", adapter=RequestsWebhookAdapter())
    webhook.send(message)

def sendServerCommand(message):
    with Client('127.0.0.1', YourRconPort, passwd="yourRconPassword") as client:
        time.sleep(10)
        response = client.run('announce '+ message)
    print(response)

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open("..\VRisingServer.log","r")
    loglines = follow(logfile)
    for line in loglines:
        # print(line)
        if "User " in line and "Character:" in line:
            userLine = line.split(",")
            print(userLine)
            characterNameString = userLine[2].split("'")
            characterName = characterNameString[1]

            steamIDString = userLine[0]
            userSteamIDString = steamIDString.split("'")
            userSteamID = userSteamIDString[3]

            #print(userSteamID)
            #print("SteamID: " + userSteamID)
            userInfo = (userSteamID, characterName)

            if userSteamID not in userlist :
                userlist[userSteamID] = characterName

            now = dt.now()
            current_time = now.strftime("%H:%M - %d.%m.%Y")           
            # print(userLine)
            announcement = "["+ current_time + "] " + characterName + " logged in."
            print(announcement)
            sendDiscordMessage(announcement)
            #sendServerCommand(announcement)
        if "EndAuthSession " in line:
            logoutUserLine = line.split(":")
            logoutUserSteamID = re.sub("\D","",logoutUserLine[1].replace(" ",""))
            print("["+ current_time + "] " + userlist[userSteamID] + " oyundan cikis yapti.")
            announcement = "["+ current_time + "] " + userlist[userSteamID] + " logged out."
            sendDiscordMessage(announcement)

