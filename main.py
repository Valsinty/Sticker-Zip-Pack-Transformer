import os
import json
from getpass import getpass
import requests
import time
from zip_reader import extract_static
CONFIG_FILE = 'config.json'

#Load the config file into a variable as a json object
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as config_file:
            config1 = json.load(config_file)
            return config1
    return {}

config = load_config()

def save_config(config1):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config1, config_file)

#Extract the token for the telegram bot, or ask it as an input if it is not set in the config file
if ("bot_token" in config) and (config["bot_token"]!="") and (config["bot_token"]!="YOUR_BOT_TOKEN"):
    token = config["bot_token"]
else:
    token = getpass("Enter your bot token: ")
    config["bot_token"] = token
    save_config(config)

BASE_URL = "https://api.telegram.org/bot{}/".format(token)
DOWNLOAD_BASE_URL = "https://api.telegram.org/file/bot{}/".format(token)

def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {}
    if offset:
        params["offset"] = offset
    r = requests.get(url, params=params)
    return r.json()

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    r = requests.post(url, data={"chat_id": chat_id, "text": text})
    return r.json()

def get_file_path(file_id):
    url = BASE_URL + "getFile"
    params = {"file_id": file_id}
    r = requests.get(url, params=params)
    data = r.json()
    return data["result"]["file_path"]


def download_file(file_path,save_as):
    url = DOWNLOAD_BASE_URL + file_path
    r = requests.get(url)

    print("Status:", r.status_code)
    print("Size:", len(r.content))

    with open(save_as, 'wb') as f:
        f.write(r.content)

def create_sticker_set(user_id, pack_name, title, emoji, first_sticker):
    url = BASE_URL + "createNewStickerSet"

    with open(first_sticker, 'rb') as f:
        r = requests.post(url, data={"user_id": user_id, "name":pack_name, "title":title, "emojis":emoji}, files={"png_sticker":f})
        print(r.json())

def add_sticker(user_id, pack_name, emoji, sticker_path):
    url = BASE_URL + "addStickerToSet"
    with open(sticker_path, 'rb') as f:
        r = requests.post(url, data={"user_id":user_id,"name":pack_name, "emojis":emoji}, files={"png_sticker":f})
        print(r.json())

def main(offset):

    while True:
        updates = get_updates(offset)
        for update in updates["result"]:
            message = update.get("message")
            offset = update["update_id"] + 1

            if not message:
                continue

            if "document" in message:
                document = message["document"]
                file_id = document["file_id"]
                file_name = document["file_name"]
                file_size = document["file_size"]

                user_id = message["from"]["id"]
                chat_id = message["chat"]["id"]

                print("Received file", file_name)

                if file_name.endswith(".zip"):
                    file_path = get_file_path(file_id)
                    download_file(file_path, file_name)

                    print("Zip file downloaded", file_name)
                    files = extract_static(file_name)
                    if not files:
                        send_message(chat_id, "No valid images in the zip file.")
                        continue
                    print("Extracted stickers:", files)

                    pack_name = config["default_name"]
                    emoji = config["default_emoji"]

                    stamp = str(int(time.time()))
                    pack_name = config["default_name"] + "_" + stamp + "_by_ilovestickersbot"
                    title = config["default_name"]

                    create_sticker_set(user_id, pack_name, title, emoji, files[0])
                    for sticker in files[1:]:
                        add_sticker(user_id, pack_name, emoji, sticker)

                    send_message(chat_id, f"https://t.me/addstickers/{pack_name}")

            else:
                message = update["message"]
                chat_id = message["chat"]["id"]

                send_message(chat_id, "You need to send me the zip file of your sticker pack")



        time.sleep(5)

if __name__ == "__main__":
    data = get_updates()

    if data["result"]:
        offset1 = data["result"][-1]["update_id"] + 1
    else:
        offset1 = None
    main(offset1)