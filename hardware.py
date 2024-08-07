from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
import mysql.connector
from rahasia import hehe

async def hardware(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    match = re.match(r'/hardware\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan nama SITE setelah perintah /hardware. Contoh /hardware NBI01')
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

    # Ambil jenis hardware yang ada
    mycursor = mydb.cursor()
    query = "SELECT DISTINCT jenis_hardware FROM hardware_aloptama WHERE jenis_aloptama = '%s' AND id_aloptama = %s" % (jenis_aloptama,id)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if myresult == []:
        await update.message.reply_text(f"Detail Hardware site {kode} tidak tersedia")
        return
    jenis_hardware = []
    for x in myresult:
        jenis_hardware.append(x[0])

    # Ambil detail hardware
    laporan = f"""Detail Hardware site {kode}

"""
    for jh in jenis_hardware:
        mycursor = mydb.cursor()
        query = "SELECT jenis_hardware , merk ,tipe ,sn ,tanggal_pemasangan FROM hardware_aloptama WHERE jenis_aloptama = '%s' AND id_aloptama = %s AND jenis_hardware = '%s' ORDER BY tanggal_pemasangan DESC LIMIT 1" % (
        jenis_aloptama, id, jh)
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        laporanTambahan = f"""=={jh}==
Merk , Tipe : {myresult[0][1]} {myresult[0][2]}
SN : {myresult[0][3]}
Pemasangan : {myresult[0][4]}

"""
        laporan = laporan + laporanTambahan


    # Balas pesan ke user
    await update.message.reply_text(laporan)