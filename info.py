from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
import mysql.connector
from rahasia import hehe

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    match = re.match(r'/info\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan nama SITE setelah perintah /info.')
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

    # ambil info dari site
    infoSite = []
    mycursor = mydb.cursor()
    for a in ["lokasi", "nama_pic", "jabatan_pic", "kontak_pic", "catatan"]:
        query = "SELECT %s FROM tbl_%s WHERE id = %s " % (a, jenis_aloptama, id)
        mycursor.execute(query)
        myresult = mycursor.fetchone()
        infoSite.append(myresult[0])

    # cari tanggal kunjungan , kerusakan serta rekomendasi terakhir

    infoKunjunganTerakhir = []

    mycursor = mydb.cursor()
    query = "SELECT tanggal FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % (
    jenis_aloptama, jenis_aloptama, id)
    mycursor.execute(query)
    tanggal = mycursor.fetchone()[0]

    mycursor = mydb.cursor()
    query = "SELECT kerusakan FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % (
    jenis_aloptama, jenis_aloptama, id)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    kerusakan = myresult[0]

    mycursor = mydb.cursor()
    query = "SELECT rekomendasi FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % (
    jenis_aloptama, jenis_aloptama, id)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    rekomendasi = myresult[0]

    pesan = f"""Detail info Site {kode}

Lokasi : {infoSite[0]}
PIC : {infoSite[1]}
Jabatan PIC : {infoSite[2]}
Kontak PIC : {infoSite[3]}

Kunjungan Terakhir
Tanggal : {tanggal}
Kerusakan : {kerusakan}
Rekomendasi : {rekomendasi}

Catatan Site
{infoSite[4]}
"""
    # cari file pdf laporan
    mycursor = mydb.cursor()
    query = "SELECT laporan FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % (
        jenis_aloptama, jenis_aloptama, id)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    laporan = myresult[0]
    pdf_path = f"C:/laragon/www/aloptamaDNP/kunjungan_{jenis_aloptama}/laporan/{laporan}"
    chat_id = update.effective_chat.id


    # Balas pesan ke user
    await update.message.reply_text(pesan)

    # Kirim file PDF
    await context.bot.send_document(chat_id=chat_id, document=open(pdf_path, 'rb'))