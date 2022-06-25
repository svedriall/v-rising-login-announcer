from rcon.source import Client
import time
import schedule
from datetime import datetime

rcon_ip = "YourServerIP"
rcon_port = YourRCONPort
rcon_password = "YourPassword"


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S - %d.%m.%Y")
    return current_time


rules_eng = (
    "<size=20s><color=red><b><u>\nRules:</u></b></color></size> \n"
    "<size=15><color=yellow>"
    "- 1 Castle per clan, both castles will be deleted upon complaint \n"
    "- Teaming is not allowed in any shape or form, not everything is teaming. \n"
    "- All forms of cursing and harrasment is forbidden. \n"
    "- Base blocking is forbidden. \n"
    "- All complaints should be done through discord. discord.gg/soprecious\n"
    "</color></size>"
)
rules_eng_2 = (
    "<size=15><color=yellow>"
    "\n- Do not try to resolve personal issues through global chat. \n"
    "</color></size>"
)

settings_eng = (
   "<size=20s><color=white><b><u>\nServer Settings:</u></b></color></size> \n"
   "<size=15><color=green>"
   "- 3X Loot, except blood essence\n"
   "- Buffed physical damage by 25%\n"
   "- All NPCs %25 stronger. \n"
   "- Max 5 Days to decay for castles at T4.\n"
   "- More servants and tombs for castles.\n"
   "- Smaller maximum size for castles.\n"
   "- Raid hours weekdays 22.00 - 23.00 GMT+2, weekends 21.00 - 23.00 GMT+2.\n"
   "- Siege time is 4 minutes.\n"
   "- Raid announced and shown on map. \n"
   "- Sun damage is disabled.\n"
)

settings_eng_2 = (
    "<size=15><color=green>\n"
    "</color></size>"
)

def send_rules():
    with Client(rcon_ip, rcon_port, passwd=rcon_password) as client:
        time.sleep(1)
        response = client.run("announce " + str(rules_eng))
        response = client.run("announce " + str(rules_eng_2))
    print("EN Kural sent " + get_current_time())
    print(response)
    
    
def send_settings():
    with Client(rcon_ip, rcon_port, passwd=rcon_password) as client:
        time.sleep(1)
        response = client.run("announce " + str(settings_eng))
        # response = client.run("announce " + str(settings_eng_2))
    print("EN Ayarlar sent " + get_current_time())
    print(response)


send_settings()
print( get_current_time())

schedule.every(15).minutes.do(send_settings)
schedule.every(20).minutes.do(send_rules)

print("Started scheduling announcements")

while True:
    schedule.run_pending()
    time.sleep(1)
