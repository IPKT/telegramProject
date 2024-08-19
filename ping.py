from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, CallbackContext
import emoji
import os
import re
import subprocess
import platform
import mysql.connector
from rahasia import hehe

emojiTangan= "\U0001F64F"
emojiSenyum= "\U0001F60A"

async def ping(update: Update, context: CallbackContext):
    f = open("userList.txt", "r")
    list = f.read()
    f.close()
    if str(update.message.from_user.id) not in list:
        await update.message.reply_text('Silahkan Login terlebih dahulu!!')
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
        if tabel == "tbl_intensity":
            mycursor = mydb.cursor()
            query = "SELECT * FROM %s WHERE kode = '%s' " % (tabel, kode)
            mycursor.execute(query)
            myresult = mycursor.fetchone()
            if myresult == None:
                continue
            else:
                tunggu = f"Harap tunggu.... {emojiTangan}"
                await update.message.reply_text(tunggu)
                jenis_aloptama = tabel.split("_")[1]


    #Hanya Intensity Realshake
    try:
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
        lines_to_remove = {8, 9, 10, 11}
        #content = re.sub(r"\t", "", listIP)
        filtered_lines = [line for index, line in enumerate(listIP) if index not in lines_to_remove]
        with open("ping_results.txt", "w") as file:
                file.writelines(filtered_lines)
        with open("ping_results.txt","r") as file:
            listIP = file.readlines()

        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

        # ambil ip
        def ping(host):
            # Menyesuaikan perintah ping berdasarkan sistem operasi
            if platform.system() == "Windows":
                command = ['ping', '-n', '1', host]
            else:
                command = ['ping', '-c', '1', host]

            result = subprocess.run(['ping', host], capture_output=True, text=True)

            if result.returncode == 0:
                if "time" in result.stdout:
                    return True, "OK"
                else:
                    return False, "Tidak OK"
            else:
                return False, result.stderr

        success_count = 0
        failure_count = 0

        # ambil ip
        pesanKirim = ""
        pesanKirim2= ""
        for ip in listIP:
            match = re.search(pattern, ip)
            tanpa_ip = re.sub(pattern, "", "".join(ip))
            hapus = str.maketrans('', '', ':')
            gabung = tanpa_ip.translate(hapus)
            clean_text = gabung.replace('\n', ' ')

            if match:
                ip_address = match.group(0).strip()
                success, output = ping(ip_address)
                if success:
                    (f"Ping success = {ip}")

                    hasil1=(f"{clean_text}: {output}")
                    pesanKirim = pesanKirim +"\n"+ hasil1
                    #print(hasil1)
                    # await update.message.reply_text(pesanKirim)
                    success_count += 1
                else:
                    (f"Ping failed = {ip}")
                    hasil2=(f"{clean_text}: {output}")
                    pesanKirim2 = pesanKirim2 + "\n" + hasil2
                    #print(hasil2)
                    #await update.message.reply_text(hasil2)
                    failure_count += 1
        pesanGabungan=f"Hasil tes ping Site {kode} :\n{pesanKirim}{pesanKirim2}\n\n Terimakasih....{emojiSenyum}"
        print(pesanGabungan)
        await update.message.reply_text(pesanGabungan)
        #await update.message.reply_text(pesanKirim2)

    except:
        takada = f"Mohon Maaf, hanya bisa melakukan ping ke Intensitymeter Realshake.... {emojiTangan}"
        await update.message.reply_text(takada)
        print(takada)
