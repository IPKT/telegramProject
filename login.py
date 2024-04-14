from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
from rahasia import hehe

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Mendapatkan pesan dari update
    message_text = update.message.text

    # Cek apakah dia sudah login
    f = open("userList.txt", "r")
    list = f.read()
    f.close()
    if str(update.message.from_user.id) in list:
        await update.message.reply_text('Anda sudah login sebelumnya!!')
        return

    # Menggunakan ekspresi reguler untuk menangkap kata kedua setelah kata pertama
    match = re.match(r'/login\s+(\w+)\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan username dan password setelah perintah /login.')
        return

    # Mendapatkan kata kedua setelah kata pertama dari pesan
    user = match.group(1)
    sandi = match.group(2)
    u , p = hehe.userpass()
    f = open("userList.txt","r")
    list = f.read()
    f.close()
    if str(update.message.from_user.id) in list:
        print("sudah ada dalam list user id")
        await update.message.reply_text('Anda sudah pernah login!!')
    else:
        print("belum ada dalam list user id")
        if user == u and sandi == p:
            print("login berhasil")
            user_id = update.message.from_user.id
            username = update.message.from_user.username
            fullName = update.message.from_user.full_name
            print(username, user_id)
            f = open("userList.txt", "a")
            f.write(str(fullName))
            f.write(" ")
            f.write(str(username))
            f.write(" ")
            f.write(str(user_id))
            f.write("\n")
            f.close()
            balasan = f"Login Berhasil \nSelamat datang {fullName} \nIni adalah bot yang membantu anda memberikan informasi Aloptama Stasiun Geofisika Denpasar"
            await update.message.reply_text(balasan)
        else:
            await update.message.reply_text("User dan password Anda salah, silahkan hubungi Admin")
        # Balas pesan dengan nama yang diberikan
    #await update.message.reply_text(hardwareDetail)