import mysql.connector
from rahasia import hehe
# Koneksi ke DB
host, user, password, database = hehe.koneksidb()
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

## ambil dulu semua kode site

tabel = 'tbl_intensity'
mycursor = mydb.cursor()
query = "SELECT kode , id FROM %s ORDER BY kode" % (tabel)
mycursor.execute(query)
myresult = mycursor.fetchall()
kode=[]
print(myresult)
for a in myresult:
    kode.append(a)

print(kode)
no = 1
laporan = ""
for a in kode:
    tabel = 'tbl_kunjungan_intensity'
    mycursor = mydb.cursor()
    query = "SELECT COUNT(*) FROM %s WHERE tanggal >= '2024-01-01' AND id_intensity = %s" % (tabel,a[1])
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    b = f"{no}.{a[0]} {myresult[0]} \n"
    laporan = laporan + b
    no = no+1

print(laporan)


# SELECT * FROM `tbl_kunjungan_intensity` WHERE `tanggal` >= 2024-01-01 AND `id_intensity` = 30
# ##cari jenis aloptamanya
# jenis_aloptama = ""
# tabels = ['tbl_seismo', 'tbl_acc_noncolo', 'tbl_intensity', 'tbl_int_reis']
# for tabel in tabels:
#     mycursor = mydb.cursor()
#     query = "SELECT * FROM %s WHERE kode = '%s' " % (tabel, kode)
#     mycursor.execute(query)
#     myresult = mycursor.fetchone()
#     if myresult == None:
#         continue
#     else:
#         jenis_aloptama = tabel.split("_")[1]
#
# # Cari id aloptamanya
# mycursor = mydb.cursor()
# query = "SELECT id FROM tbl_%s WHERE kode = '%s' " % (jenis_aloptama, kode)
# mycursor.execute(query)
# myresult = mycursor.fetchone()
# id = int(myresult[0])
#
# # Ambil jenis hardware yang ada
# mycursor = mydb.cursor()
# query = "SELECT DISTINCT jenis_hardware FROM hardware_aloptama WHERE jenis_aloptama = '%s' AND id_aloptama = %s" % (jenis_aloptama,id)
# mycursor.execute(query)
# myresult = mycursor.fetchall()
# if myresult == []:
#     await update.message.reply_text(f"Detail Hardware site {kode} tidak tersedia")
#     return
# jenis_hardware = []
# for x in myresult:
#     jenis_hardware.append(x[0])
#
# # Ambil detail hardware
# laporan = f"""Detail Hardware site {kode}
#
# """
# for jh in jenis_hardware:
#     mycursor = mydb.cursor()
#     query = "SELECT jenis_hardware , merk ,tipe ,sn ,tanggal_pemasangan FROM hardware_aloptama WHERE jenis_aloptama = '%s' AND id_aloptama = %s AND jenis_hardware = '%s' ORDER BY tanggal_pemasangan DESC LIMIT 1" % (
#     jenis_aloptama, id, jh)
#     mycursor.execute(query)
#     myresult = mycursor.fetchall()
#     laporanTambahan = f"""=={jh}==
# Merk , Tipe : {myresult[0][1]} {myresult[0][2]}
# SN : {myresult[0][3]}
# Pemasangan : {myresult[0][4]}
#
# """
#     laporan = laporan + laporanTambahan
