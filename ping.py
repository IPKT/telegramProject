from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
import subprocess
import mysql.connector
from rahasia import hehe

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    match = re.match(r'/ping\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    if not match:
        await update.message.reply_text('Mohon berikan nama SITE setelah perintah /ping. Contoh: /ping NKBI ')
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

    # ambil list ip
    mycursor = mydb.cursor()
    query = "SELECT ip FROM tbl_%s WHERE id = %s " % (jenis_aloptama, id)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    pesan = f"""Hasil ping ke {kode}

{myresult[0]}
    """
    print(pesan)
    with open("ping_results.txt", "w") as file:
        file.write(pesan)

    with open("ping_results.txt","r") as file:
        listIP = file.readlines()
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # ambil ip
    def ping(host):
        result = subprocess.run(['ping', host], capture_output=True, text=True)

        if result.returncode == 0:
            if "time" in result.stdout:
                return True, "OK"
            else:
                return False, "RTO"
        else:
            return False, result.stderr

    success_count = 0
    failure_count = 0
    listIP_RTO = []

    # ambil ip
    for ip in listIP:
        match = re.search(pattern, ip)
        if match:
            ip_address = match.group(0).strip()
            success, output = ping(ip_address)
            if success:
                (f"Ping success = {ip}")
                (output)
                success_count += 1
            else:
                (f"Ping failed = {ip}")
                (output)
                failure_count += 1
                listIP_RTO.append(ip)

    if listIP_RTO:
        join_tanpa_ip = ",".join(listIP_RTO)
        tanpa_ip = re.sub(pattern, "", join_tanpa_ip).strip()
        (f"{tanpa_ip}")
    else:
        ("tidak ada")

    hasil1 = (f"Reply = {success_count}")
    hasil2 = (f"\nTidak Reply = {failure_count}")
    hasil3 = ("\nDaftar ip yang tidak Reply =")
    hasil4=(f"{tanpa_ip}")
    combined = hasil1 + hasil2 + hasil3 + hasil4
    print(combined)

    # Mengirim hasil kepada pengguna
    await update.message.reply_text(combined)
