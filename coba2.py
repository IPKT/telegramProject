import mysql.connector
from rahasia import hehe

# Mendapatkan kata kedua setelah kata pertama dari pesan
kode = "NBI03"

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
for a in ["lokasi","nama_pic","jabatan_pic","kontak_pic","catatan"]:
    query = "SELECT %s FROM tbl_%s WHERE id = %s " % (a,jenis_aloptama, id)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    infoSite.append(myresult[0])

# cari tanggal kunjungan , kerusakan serta rekomendasi terakhir


infoKunjunganTerakhir = []

mycursor = mydb.cursor()
query = "SELECT tanggal FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % ( jenis_aloptama, jenis_aloptama, id)
mycursor.execute(query)
tanggal = mycursor.fetchone()[0]

mycursor = mydb.cursor()
query = "SELECT kerusakan FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % ( jenis_aloptama, jenis_aloptama, id)
mycursor.execute(query)
myresult = mycursor.fetchone()
kerusakan = myresult[0]

mycursor = mydb.cursor()
query = "SELECT rekomendasi FROM tbl_kunjungan_%s WHERE id_%s = %s ORDER BY tanggal DESC LIMIT 1" % ( jenis_aloptama, jenis_aloptama, id)
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

print(pesan)