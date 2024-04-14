import mysql.connector
from rahasia import hehe
# jenis_aloptama = "intensity"
kode = "PUTU"

host, user, password, database = hehe.koneksidb()
mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()
query = "SELECT ip FROM tbl_intensity WHERE kode = '%s' " % (kode)
mycursor.execute(query)
myresult = mycursor.fetchone()
print(myresult[0])