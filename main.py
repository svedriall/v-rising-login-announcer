import time
from datetime import datetime as dt
from rcon.source import Client
import requests
from discord import Webhook, RequestsWebhookAdapter
import re

userlist = {}
discordToggle = True # Should it send discord messages?
loginServerAnnounceToggle = True # Should it send server messages for login?
logoutServerAnnounceToggle = True #Should it send server messages for logout?

debugFollow = False # Should it debug & log every line?

now = dt.now()
current_time = now.strftime("%H:%M - %d.%m.%Y")  

def sendDiscordMessage(message):
    webhook = Webhook.from_url("your-url", adapter=RequestsWebhookAdapter())
    webhook.send(message)

def sendServerCommand(message):
    with Client('127.0.0.1', YourRconPort, passwd="YourRconPassword") as client:
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
        if debugFollow:
            print(current_time + "-" + line)
        try:
            if "connected as" in line:
                userLine = line.split(",")
                characterNameString = userLine[2].split("'")
                characterName = characterNameString[1]

                steamIDString = userLine[0]
                userSteamIDString = steamIDString.split("'")
                userSteamID = userSteamIDString[3]

                if userSteamID not in userlist :
                    userlist[userSteamID] = characterName

                # print(userLine)
                announcement = "["+ current_time + "] " + characterName + " oyuna baglandi."
                print(announcement)
                if discordToggle:
                    sendDiscordMessage(announcement)
                if loginServerAnnounceToggle:
                    sendServerCommand(announcement)
            if "SteamPlatformSystem - EndAuthSession" in line:
                logoutUserLine = line.split(":")
                logoutUserSteamID = re.sub("\D","",logoutUserLine[1].replace(" ",""))
                announcement = "["+ current_time + "] " + userlist[userSteamID] + " disconnected."
                print(announcement)
                if discordToggle:
                    sendDiscordMessage(announcement)
                if logoutServerAnnounceToggle:
                    sendServerCommand(announcement)
        except:
            print("an exception occured on line: " + line)
