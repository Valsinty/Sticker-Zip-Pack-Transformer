import os
import json
import subprocess

token = os.environ["BOT_TOKEN"]

with open("config.json", "w") as f:
    json.dump({"bot_token": token}, f)

subprocess.run(["python", "main.py"])
