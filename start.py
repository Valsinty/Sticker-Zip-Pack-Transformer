import os
import json
import subprocess

token = os.environ.get("BOT_TOKEN")

config = {
    "bot_token": token,
    "default_emoji": "👍",
    "default_name": "new_pack"
}

with open("config.json", "w") as f:
    json.dump(config, f)

subprocess.run(["python", "main.py"])
