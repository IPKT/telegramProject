from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
from translate import decrypt

async def dekrip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Mendapatkan pesan dari update
    message_text = update.message.text
    print(message_text)
    message_text = message_text.split(" ")

    # # Menggunakan ekspresi reguler untuk menangkap kata kedua setelah kata pertama
    # match = re.match(r'/dekrip\s+(\w+)\s+(\w+)\s+(\w+)', message_text)
    #
    # # Jika tidak ada kecocokan, kembalikan pesan default
    if len(message_text) != 4 :
        await update.message.reply_text('Mohon berikan teksTerenkripsi , password dan salt setelah perintah /dekrip.')
        return

    # Mendapatkan kata kedua setelah kata pertama dari pesan
    teksTerenkripsi = message_text[1]
    password = message_text[2]
    salt = message_text[3]
    teksTerkdeskripsi = decrypt(teksTerenkripsi, password,salt)
    await update.message.reply_text(teksTerkdeskripsi)
    # f = open("userList.txt","r")
    # list = f.read()
    # f.close()
    # if str(update.message.from_user.id) in list:
    #     print("sudah ada dalam list user id")
    #     await update.message.reply_text('Anda sudah pernah login')
    # else:
    #     print("belum ada dalam list user id")
    #     if user == "geofisika" and sandi == "sanglah12345":
    #         print("login berhasil")
    #         user_id = update.message.from_user.id
    #         username = update.message.from_user.username
    #         fullName = update.message.from_user.full_name
    #         print(username, user_id)
    #         f = open("userList.txt", "a")
    #         f.write(str(fullName))
    #         f.write(" ")
    #         f.write(str(username))
    #         f.write(" ")
    #         f.write(str(user_id))
    #         f.write("\n")
    #         f.close()
    #         balasan = f"Login Berhasil \nSelamat datang {fullName} \nIni adalah bot yang membantu anda memberikan informasi Aloptama Stasiun Geofisika Denpasar"
    #         await update.message.reply_text(balasan)
    #     # Balas pesan dengan nama yang diberikan
    # #await update.message.reply_text(hardwareDetail)