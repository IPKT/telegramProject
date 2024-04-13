from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re

async def hardware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    f = open("userList.txt", "r")
    list = f.read()
    f.close()
    if str(update.message.from_user.id) not in list:
        await update.message.reply_text('Silahkan Login terlebi dahulu!!')
        return

    # Mendapatkan pesan dari update
    message_text = update.message.text

    # Menggunakan ekspresi reguler untuk menangkap kata kedua setelah kata pertama
    match = re.match(r'/hardware\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan nama SITE setelah perintah /hardware.')
        return

    # Mendapatkan kata kedua setelah kata pertama dari pesan
    site = match.group(1)
    txtfile = open(f"Hardware/{site}.txt","r")
    hardwareDetail = txtfile.read()


    # Balas pesan dengan nama yang diberikan
    await update.message.reply_text(hardwareDetail)