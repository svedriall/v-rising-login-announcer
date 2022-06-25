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

def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S - %d.%m.%Y")
    return current_time


def first_time_run_check():
    def where_json(file_name):
        return os.path.exists(file_name)

    if where_json("users.json"):
        pass
    else:
        data = {"DummyUserID": "DummyName"}

        with open("users.json", "w") as outfile:
            json.dump(data, outfile)


def check_user(check_steam_id, check_character_name):
    with open(file_name, "r") as f:
        user_list = json.load(f)

    if check_steam_id not in user_list:
        if check_character_name != '':
            user_list[check_steam_id] = check_character_name
        else:
            print('invalid user name, probably first login character creation.')
            user_list[check_steam_id] = "New Vampire"
    else:
        if user_list[check_steam_id] == "New Vampire":
            user_list[check_steam_id] = check_character_name
        else:
            print('user found')

    os.remove(file_name)
    with open(file_name, "w") as f:
        json.dump(user_list, f, indent=4)

    return user_list


def get_user_list():
    with open(file_name, "r") as f:
        user_list = json.load(f)
    return user_list


def send_discord_announcement(message):
    webhook = Webhook.from_url(
        discord_webhook_url,
        adapter=RequestsWebhookAdapter(),
    )
    webhook.send(message)


def send_server_command(message):
    with Client(rcon_ip, rcon_port, passwd=rcon_password) as client:
        time.sleep(1)
        response = client.run("announce " + message)
        test = client.run("help")
    print(test, response)


def follow(the_file):
    the_file.seek(0, 2)
    last_log_time = datetime.datetime.now()
    while True:
        file_line = the_file.readline()
        if not file_line:
            time.sleep(0.1)
            # calculated_time = (datetime.datetime.now() - last_log_time).total_seconds()
            # if calculated_time > 600:
            #     print('Stale log?')

            continue
        last_log_time = datetime.datetime.now()
        yield file_line


if __name__ == "__main__":
    log_file = open(logfileDir, "r")
    log_lines = follow(log_file)

    #send_discord_announcement("Login Announcer Launched")
    #send_server_command("Login Announcer Launched")

    for line in log_lines:
        if debug_follow_toggle:
            print(get_current_time() + "-" + line)
        # try:
        if "connected as" in line:
            connection_line = line.split(",")
            if debug_follow_toggle: print("connection line: " + str(connection_line))
            character_name_string = connection_line[2].split("'")
            if debug_follow_toggle: print("connection_name string: " + str(character_name_string))
            character_name = character_name_string[1]
            if debug_follow_toggle: print("character name: " + character_name)

            steam_id_line = connection_line[0]
            if debug_follow_toggle: print("steam id line: " + steam_id_line)
            user_steam_id_string = steam_id_line.split("'")
            if debug_follow_toggle: print("steam id string: " + str(user_steam_id_string))
            user_steam_id = user_steam_id_string[3]
            if debug_follow_toggle: print("user steam id: " + user_steam_id)
            if debug_follow_toggle: print("raw login line: " + line)
            user_data = check_user(user_steam_id, character_name)

            announcement = (
                "["
                + get_current_time()
                + "] "
                + character_name
                + connected_message_affix
            )
            print(announcement)
            if discord_toggle:
                send_discord_announcement(announcement)
            if login_server_announce_toggle:
                send_server_command(announcement)
        if "SteamPlatformSystem - EndAuthSession" in line:
            user_data = get_user_list()
            print(line)
            logout_user_log_line = line.split(":")
            if debug_follow_toggle: print("logout_line: " + str(logout_user_log_line))
            logout_user_steam_id = str(
                re.sub("\D", "", logout_user_log_line[1].replace(" ", ""))
            )
            if debug_follow_toggle: print("logout userSteamID: " + logout_user_steam_id)
            announcement = (
                "["
                + get_current_time()
                + "] "
                + user_data[logout_user_steam_id]
                + disconnected_message_affix
            )
            print(announcement)
            if discord_toggle:
                send_discord_announcement(announcement)
            if logoutServerAnnounceToggle:
                send_server_command(announcement)
        # except:
        #     print("an exception occured on line: " + line)
