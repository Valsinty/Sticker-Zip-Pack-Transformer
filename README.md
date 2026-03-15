# Sticker Zip Pack Transformer Bot

A Python based Telegram bot that
allows you to transfer sticker packs
from other messaging apps to Telegram by:
- receiving ZIP files
- converting images to WEBP
- reformating them to Telegram specifications
- creating a new sticker pack
- uploading stickers to the newly created pack
- sharing a link to your new sticker pack

How to run it locally (with you own bot)
-
1. Enter the token of your telegram bot by one of the following ways:
   - Paste it to the "bot_token" property in the config.json file
   - Run main.py for the first time and enter the token in the terminal
2. You can further customize the pack by editing the default emoji for your stickers or the name of your pack by modifying the config.json file
3. Start the program
    - When the bot is running, sending zip files containing images create a sticker pack and return a link to it

Using the hosted bot
-
1. Create a zip file of your sticker pack
2. Send it to @ilovestickersbot on Telegram
3. The bot will generate a Telegram sticker pack and sned you the link

Example (WhatsApp)
- Send the sticker pack to a chat
- Hold the sticker pack on the chat
- Taps the three-dots menu
- Select share
- Choose Telegram
- Send it to Sticker Zip Pack Transformer