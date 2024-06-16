from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
import mysql.connector
from rahasia import hehe

async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    f = open("userList.txt", "r")
    list = f.read()
    f.close()
    if str(update.message.from_user.id) not in list:
        await update.message.reply_text('Silahkan Login terlebi dahulu!!')
        return

    # Mendapatkan pesan dari update
    message_text = update.message.text
    fullName = update.message.from_user.full_name
    print(fullName , message_text)

    # Menggunakan ekspresi reguler untuk menangkap kata kedua setelah kata pertama
    match = re.match(r'/ip\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan nama SITE setelah perintah /ip.')
        return

    # Mendapatkan kata kedua setelah kata pertama dari pesan
    kode = match.group(1).upper()

    # Koneksi ke DB
    host, user, password, database = hehe.koneksidb()
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    ##cari jenis aloptamanya
    jenis_aloptama = ""
    tabels = ['tbl_seismo', 'tbl_acc_noncolo', 'tbl_intensity', 'tbl_int_reis']
    for tabel in tabels:
        mycursor = mydb.cursor()
        query = "SELECT * FROM %s WHERE kode = '%s' " % (tabel, kode)
        mycursor.execute(query)
        myresult = mycursor.fetchone()
        if myresult == None:
            continue
        else:
            jenis_aloptama = tabel.split("_")[1]

    # Cari id aloptamanya
    mycursor = mydb.cursor()
    query = "SELECT id FROM tbl_%s WHERE kode = '%s' " % (jenis_aloptama, kode)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    id = int(myresult[0])

    # ambil ip
    mycursor = mydb.cursor()
    query = "SELECT ip FROM tbl_%s WHERE id = %s " % (jenis_aloptama, id)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    pesan = f"""Detail IP site {kode}

{myresult[0]}
    """


    # Balas pesan ke user
    await update.message.reply_text(pesan)