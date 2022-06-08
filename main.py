import time
from datetime import datetime as dt
from rcon.source import Client
from discord import Webhook, RequestsWebhookAdapter
import re
import json
import os

discordToggle = True  # Shousld it send discord messages?
loginServerAnnounceToggle = True  # Should it send server messages for login?
logoutServerAnnounceToggle = True  # Should it send server messages for logout?

debugFollow = False  # Should it debug & log every line?
filename = "users.json"

RCONIP = "127.0.0.1"
RCONPort = 25575
RCONPassword = "YourPasswordHere"

DiscordWebHookURL = "YourURLHere"
connectedMessageAffix = " connected."
disconnectedMessageAffix = " disconnected."

logfileDir = "..\VRisingServer.log"

def getCurrentTime():
    now = dt.now()
    current_time = now.strftime("%H:%M:%S - %d.%m.%Y")
    return current_time


def firstTimeCheck():
    def where_json(file_name):
        return os.path.exists(file_name)

    if where_json("users.json"):
        pass
    else:
        data = {"DummyUserID": "DummyName"}

        with open("users.json", "w") as outfile:
            json.dump(data, outfile)


def checkUser(checkedUserSteamID, checkEedUserCharacterName):
    with open(filename, "r") as f:
        userlist = json.load(f)
        if userSteamID not in userlist:
            userlist[
                checkedUserSteamID
            ] = checkEedUserCharacterName  # <--- add `id` value.
        else:
            print("user exists")

    os.remove(filename)
    with open(filename, "w") as f:
        json.dump(userlist, f, indent=4)

    return userlist


def sendDiscordMessage(message):
    webhook = Webhook.from_url(
        DiscordWebHookURL,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(message)


def sendServerCommand(message):
    with Client(RCONIP, RCONPort, passwd=RCONPassword) as client:
        time.sleep(1)
        response = client.run("announce " + message)
        test = client.run("help")
    print(test, response)


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    logfile = open(logfileDir, "r")
    loglines = follow(logfile)

    sendDiscordMessage("Login Announcer Launched")
    sendServerCommand("Login Announcer Launched")

    for line in loglines:
        if debugFollow:
            print(getCurrentTime() + "-" + line)
        try:
            if "connected as" in line:
                userLine = line.split(",")
                characterNameString = userLine[2].split("'")
                characterName = characterNameString[1]

                steamIDString = userLine[0]
                userSteamIDString = steamIDString.split("'")
                userSteamID = userSteamIDString[3]

                userData = checkUser(userSteamID, characterName)

                announcement = (
                    "["
                    + getCurrentTime()
                    + "] "
                    + characterName
                    + connectedMessageAffix
                )
                print(announcement)
                if discordToggle:
                    sendDiscordMessage(announcement)
                if loginServerAnnounceToggle:
                    sendServerCommand(announcement)
            if "SteamPlatformSystem - EndAuthSession" in line:
                logoutUserLine = line.split(":")
                logoutUserSteamID = str(
                    re.sub("\D", "", logoutUserLine[1].replace(" ", ""))
                )
                announcement = (
                    "["
                    + getCurrentTime()
                    + "] "
                    + userData[logoutUserSteamID]
                    + disconnectedMessageAffix
                )
                print(announcement)
                if discordToggle:
                    sendDiscordMessage(announcement)
                if logoutServerAnnounceToggle:
                    sendServerCommand(announcement)
        except:
            print("an exception occured on line: " + line)
