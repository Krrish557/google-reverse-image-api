"""
MIT License

Copyright (c) 2023 SOME-1HING

This file uses the "google-reverse-image-api" API made by "SOME-1HING"
(https://github.com/SOME-1HING/google-reverse-image-api) under the terms of the MIT license.

This example file is written by "yash-sharma-1807"

Made only for Python Telegram Bot V12

"""

import requests
from Yourbot import dispatcher, Bot_token as Token
from telegram import *
from telegram.ext import *

url = "https://google-reverse-image-api.vercel.app/reverse"


def reverse(bot, update):
    if not update.message.reply_to_message:
        update.message.reply_text("Reply to a photo.")
    elif not update.message.reply_to_message.photo:
        update.message.reply_text("Reply to an image.")
    elif update.message.reply_to_message.photo:
        msg = update.message.reply_text("Searching.....")
        photo_id = update.message.reply_to_message.photo[-1].file_id
        get_path = requests.post(
            "https://api.telegram.org/bot{}/getFile?file_id={}".format(Token, photo_id)
        ).json()
        file_path = get_path["result"]["file_path"]
        data = {
            "imageUrl": "https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{}/{}".format(Token, file_path)
        }
        response = requests.post(url, json=data)
        result = response.json()
        if response.ok:
            bot.edit_message_text(
                chat_id=update.message.chat_id,
                message_id=msg.message_id,
                text="[{}]({})".format(
                    result["data"]["resultText"], result["data"]["similarUrl"]
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Check this out",
                                url="https://t.me/tyranteyeeee/36603",
                            )
                        ]
                    ]
                ),
            )
        else:
            update.message.reply_text("Some exception occurred")


reverse_cmd = CommandHandler("reverse", reverse)

dispatcher.add_handler(reverse_cmd)
