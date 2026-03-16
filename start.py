import os
import json
import subprocess

token = os.environ["BOT_TOKEN"]

with open("config.json") as f:
    config = json.load(f)

config["bot_token"] = token

with open("config.json", "w") as f:
    json.dump(config, f)

subprocess.run(["python", "main.py"])
