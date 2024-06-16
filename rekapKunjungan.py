from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
import mysql.connector
from rahasia import hehe

async def rekapKunjungan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    match = re.match(r'/rekapKunjungan\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan jenis aloptama setelah perintah /rekapKunjungan. Misalnya seismo atau intensity atau acc_noncolo atau wrs atau int_reis')
        return

    # Mendapatkan kata kedua setelah kata pertama dari pesan
    jenis = match.group(1).upper()

    # Koneksi ke DB
    host, user, password, database = hehe.koneksidb()
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    ##cari jenis aloptamanya
    jenis_aloptama = jenis
    tabel = 'tbl_' + jenis_aloptama
    mycursor = mydb.cursor()
    query = "SELECT kode , id FROM %s ORDER BY kode" % (tabel)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    kode = []
    # print(myresult)
    for a in myresult:
        kode.append(a)

    # print(kode)
    tabel = 'tbl_kunjungan_' + jenis_aloptama
    mycursor = mydb.cursor()
    query = "SELECT tanggal FROM %s ORDER BY tanggal DESC LIMIT 1" % (tabel)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    # print(myresult)
    waktuUpdate = str(myresult[0])
    print(waktuUpdate)
    # mycursor.close()

    no = 1
    laporan = f"List Jumlah Kunjungan tiap site tahun 2024 \nUpdated at {waktuUpdate}\n\n"
    # laporan=""
    for a in kode:
        tabel = 'tbl_kunjungan_'+jenis_aloptama
        mycursor = mydb.cursor()
        query = "SELECT COUNT(*) FROM %s WHERE tanggal >= '2024-01-01' AND id_%s = %s" % (tabel,jenis_aloptama,a[1])
        mycursor.execute(query)
        myresult = mycursor.fetchone()
        b = f"{no}. {a[0]} {myresult[0]} \n"
        laporan = laporan + b
        no = no + 1
    # Balas pesan ke user
    print(laporan)
    await update.message.reply_text(laporan)