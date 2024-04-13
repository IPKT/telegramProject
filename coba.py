import mysql.connector
from rahasia import hehe
# jenis_aloptama = "intensity"
kode = "NBDBB"

host, user, password, database = hehe.koneksidb()
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

##cari jenis aloptamanya
jenis_aloptama =""
tabels = ['tbl_seismo','tbl_acc_noncolo','tbl_intensity','tbl_int_reis']
for tabel in tabels:
    mycursor = mydb.cursor()
    query = "SELECT * FROM %s WHERE kode = '%s' " % (tabel, kode)
    mycursor.execute(query)
    myresult = mycursor.fetchone()
    if myresult == None:
        continue
    else:
        jenis_aloptama = tabel.split("_")[1]


##ambil id aloptama
mycursor = mydb.cursor()
query = "SELECT id FROM tbl_%s WHERE kode = '%s' " % (jenis_aloptama, kode)
mycursor.execute(query)
myresult = mycursor.fetchone()
id = int(myresult[0])

# Ambil jenis hardware yang ada
mycursor = mydb.cursor()
query = "SELECT DISTINCT jenis_hardware FROM hardware_aloptama WHERE jenis_aloptama = '%s' " %(jenis_aloptama)
mycursor.execute(query)
myresult = mycursor.fetchall()
jenis_hardware = []
for x in myresult:
    jenis_hardware.append(x[0])
print(jenis_hardware)
hardware = []
laporan = f"""Detail Hardware site {kode}

"""
## ambil hardware
for jh in jenis_hardware:
    mycursor = mydb.cursor()
    query =  "SELECT jenis_hardware , merk ,tipe ,sn ,tanggal_pemasangan FROM hardware_aloptama WHERE jenis_aloptama = '%s' AND id_aloptama = %s AND jenis_hardware = '%s' ORDER BY tanggal_pemasangan DESC LIMIT 1" % (jenis_aloptama, id, jh)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    laporanTambahan =  f"""{jh}
Merk / Tipe : {myresult[0][1]} / {myresult[0][2]}
sn : {myresult[0][3]}
Pemasangan : {myresult[0][4]}
    
"""
    laporan = laporan + laporanTambahan

print(laporan)

mydb.close()