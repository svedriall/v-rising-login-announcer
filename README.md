You should run the script from a venv created inside your "logs" folder. If your log file name is different, you should adjust the code accordingly.


Add below lines to your **ServerHostSettings.json** file to enable RCON for your server

**ServerHostSettings.json**
```json
"Rcon" : {
  "Enabled": true,
  "Password": "SecretPassword",
  "Port": 25575
}
```
You can grab the  WebhookURL of your Discord server's channel by creating an integration for it.
