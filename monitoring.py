import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater, CallbackContext
import time

from bs4 import BeautifulSoup
import requests
import datetime
import pywhatkit
import mysql.connector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import timedelta , datetime
import time
path = "chromedriver.exe"

from selenium import webdriver

async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    #match = re.match(r'/monitoring\s+(\w+)', message_text)

    # Jika tidak ada kecocokan, kembalikan pesan default
    #if not match:
    #  await update.message.reply_text('Mohon berikan nama SITE setelah perintah /ping. Contoh: /ping NKBI ')
    #  return

    # Mendapatkan kata kedua setelah kata pertama dari pesan
    # site = match.group(1).upper()



    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="sanglah151197",
      database="gis_dasar"
    )
    #{myresult[0]}
    jam_pengiriman = ['08','12','16','20']

#AMBIL DATA NAMA SITE
##SEISMOMTER
    site = open("site.txt", 'r')
    siesmo = site.readline().replace("\n","")
    seismo = siesmo.split(" ")
    ##INTENSITYMETER
    intensityRealShake = site.readline().replace("\n","")
    intensityRealShake = intensityRealShake.split(" ")
    ##ACCELERO COLOCATED
    acceleroColocated = site.readline().replace("\n", "")
    acceleroColocated = acceleroColocated.split(" ")
    ##ACCELERO NONCOLOCATED
    acceleroNonColocated = site.readline().replace("\n","")
    acceleroNonColocated=acceleroNonColocated.split(" ")
    ##INTENSITYMETER REIS
    intensityReis = site.readline().replace("\n","")
    intensityReis = intensityReis.split(" ")
    site.close()

    ##inisiasikan site off
    siteOff = []


    #=========================CEK KONDISI SIESMOTER============================#
    sensoroff_seis= []
    sensoroff_seis_latency= []
    jumlah_on_seis = 0
    jumlah_off_seis = 0
    for site in seismo :
      link = "http://202.90.198.40/sismon-wrs/web/detail_slmon2/" + site
      webpage = requests.get(link)
      soup = BeautifulSoup(webpage.content, "html.parser")
      ## masukan string = 1 untuk mengecek data SHZ
      data = soup.find(string='1')
      data = data.find_parent("tr").text
      data = ' '.join(data.split())
      data1 = data.split(' ')
      kodesensor = data1[1]
      latency = data1[len(data1) - 1]
      lat = ""
      satuan = ""
      for c in latency:
        if c.isdigit():
          lat = lat + c
        else:
          satuan = satuan + c

      waktu = int(lat)
      if satuan == 's':
        status = 'ON'
        jumlah_on_seis = jumlah_on_seis + 1
      elif waktu < 10 and satuan == 'm':
        status = 'ON'
        jumlah_on_seis = jumlah_on_seis + 1
      else:
        status = 'OFF'
        jumlah_off_seis = jumlah_off_seis + 1
        sensoroff_seis_latency.append(site + " " + str(waktu) + " " + satuan)
        sensoroff_seis.append(site)
        siteOff.append(site)


    jumlah_sensor_seis= len(seismo)

    #=========================CEK KONDISI ACCELERO COLOCATED==============================#
    sensoroff_acc= []
    sensoroff_acc_latency= []
    jumlah_on_acc = 0
    jumlah_off_acc = 0
    for site in acceleroColocated :
      link = "http://202.90.198.40/sismon-wrs/web/detail_slmon2/" + site
      webpage = requests.get(link)
      soup = BeautifulSoup(webpage.content, "html.parser")
      ## masukan string = 4 untuk mengecek data HNZ
      data = soup.find(string='4')
      data = data.find_parent("tr").text
      data = ' '.join(data.split())
      data1 = data.split(' ')
      kodesensor = data1[1]
      latency = data1[len(data1) - 1]
      lat = ""
      satuan = ""
      for c in latency:
        if c.isdigit():
          lat = lat + c
        else:
          satuan = satuan + c

      waktu = int(lat)
      if satuan == 's':
        status = 'ON'
        jumlah_on_acc = jumlah_on_acc + 1

      elif waktu < 10 and satuan == 'm':
        status = 'ON'
        jumlah_on_acc = jumlah_on_acc + 1
      else:
        status = 'OFF'
        jumlah_off_acc = jumlah_off_acc + 1
        sensoroff_acc_latency.append(site + " " + str(waktu) + " " + satuan)
        sensoroff_acc.append(site)
        siteOff.append(site)

    jumlah_sensor_acc = len(acceleroColocated)

    #=======================ACCELEROMETER NONCOLO================================#
    # webpage_simora = requests.get("https://simora.bmkg.go.id/slmon/")
    # soup = BeautifulSoup(webpage_simora.content, "html.parser")
    # accelero_noncolo = ["TTBR" , "BBBR" , "DEMO" , "NEKI" , "DEBI" ,"KHBO",]
    # sensoroff_acc_noncolo= []
    # sensoroff_acc_noncolo_latency= []
    # jumlah_on_acc_noncolo = 0
    # jumlah_off_acc_noncolo = 0
    # for site in accelero_noncolo :
    #   data = soup.find(string = site)
    #   if data == None and site in ["TTBR","BBBR"]:
    #     status = 'ON'
    #     jumlah_on_acc_noncolo = jumlah_on_acc_noncolo + 1
    #     continue
    #   data = data.find_parent("tr").text
    #   data = ' '.join(data.split())
    #   data1 = data.split(' ')
    #   kodesensor = data1[1]
    #   lastdata = data1[2]  + data1[3]
    #   waktu = int(float(data1[2]))
    #   satuan = data1[3]
    #   if satuan == 's':
    #     status = 'ON'
    #     jumlah_on_acc_noncolo = jumlah_on_acc_noncolo + 1
    #
    #   elif waktu < 40 and satuan == 'm':
    #     status = 'ON'
    #     jumlah_on_acc_noncolo = jumlah_on_acc_noncolo + 1
    #   else:
    #     if site in ["TTBR","BBBR"] and satuan =='d' and waktu > 3:
    #       status = 'ON'
    #       jumlah_on_acc_noncolo = jumlah_on_acc_noncolo + 1
    #       continue
    #     status = 'OFF'
    #     jumlah_off_acc_noncolo = jumlah_off_acc_noncolo + 1
    #     sensoroff_acc_noncolo_latency.append(site + " " + data1[2] + " " + data1[3])
    #     sensoroff_acc_noncolo.append(site)
    #     siteOff.append(site)
    #
    # jumlah_sensor_acc_noncolo= len(accelero_noncolo)


    driver = webdriver.Chrome()
    driver.get("https://simora.bmkg.go.id/simora/web/login_page")
    username = 'stageof.denpasar'
    password = '12345678'

    try:
        cek = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.NAME,"login"))
        )
        driver.find_element("name", "username").send_keys(username)
        driver.find_element("name", "password").send_keys(password)
        driver.find_element("name", "login").click()
    except:
        driver.close()

    sensoroff_acc_noncolo= []
    sensoroff_acc_noncolo_latency= []
    jumlah_on_acc_noncolo = 0
    jumlah_off_acc_noncolo = 0

    driver.get("https://simora.bmkg.go.id/simora/simora_upt/status_acc2")
    select = Select(driver.find_element(By.NAME, "example_length"))
    select.select_by_value('100')


    try:
        cek2 = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,f'//td[text()="{acceleroNonColocated[1]}"]'))
        )
        for site in acceleroNonColocated:
            s = driver.find_element(By.XPATH,f'//td[text()="{site}"]')
            s1 = s.find_element(By.XPATH,"..")
            s2 = ' '.join(s1.text.split())
            s2 = s2.split(" ")[1]
            lastData = s2
            lastData = lastData.replace("T", " ")
            date_format = '%Y-%m-%d %H:%M:%S'
            lastData = datetime.strptime(lastData, date_format)
            now = datetime.now() - timedelta(hours=8)
            latency = now - lastData
            latencyInHour = round(latency.total_seconds() / 3600, 1)
            if latencyInHour > 1:
                latency = round(latency.total_seconds() / 3600, 1)
                satuan = "h"
            else:
                latency = round(latency.total_seconds() / 60, 1)
                satuan = "m"
            if satuan == "m" and latency < 40:
              status = 'ON'
              jumlah_on_acc_noncolo = jumlah_on_acc_noncolo +1
            else:
              status = 'OFF'
              jumlah_off_acc_noncolo = jumlah_off_acc_noncolo + 1
              sensoroff_acc_noncolo_latency.append(site + " " + str(latency) + " " + satuan)
              sensoroff_acc_noncolo.append(site)
              siteOff.append(site)
    except:
        print("tidak ditemukan")
    jumlah_sensor_acc_noncolo= len(acceleroNonColocated)

    #=================== CEK KONDISI INTENSITYMETER REALSHAKE =============================#
    sensoroff_int= []
    sensoroff_int_latency= []
    jumlah_on_int = 0
    jumlah_off_int = 0

    driver.get("https://simora.bmkg.go.id/simora/simora_upt/status_int")
    select = Select(driver.find_element(By.NAME, "example_length"))
    select.select_by_value('100')

    try:
        cek2 = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,f'//td[text()="{intensityRealShake[1]}"]'))
        )
        for site in intensityRealShake:
            s = driver.find_element(By.XPATH,f'//td[text()="{site}"]')
            s1 = s.find_element(By.XPATH,"..")
            s2 = ' '.join(s1.text.split())
            s2 = s2.split(" ")[1]
            lastData = s2
            lastData = lastData.replace("T", " ")
            date_format = '%Y-%m-%d %H:%M:%S'
            lastData = datetime.strptime(lastData, date_format)
            now = datetime.now() - timedelta(hours=8)
            latency = now - lastData
            latencyInHour = round(latency.total_seconds() / 3600, 1)
            if latencyInHour > 1:
                latency = round(latency.total_seconds() / 3600, 1)
                satuan = "h"
            else:
                latency = round(latency.total_seconds() / 60, 1)
                satuan = "m"
            if satuan == "m" and latency < 40:
              status = 'ON'
              jumlah_on_int = jumlah_on_int +1
            else:
              status = 'OFF'
              jumlah_off_int = jumlah_off_int + 1
              sensoroff_int_latency.append(site + " " + str(latency) + " " + satuan)
              sensoroff_int.append(site)
              siteOff.append(site)
    except:
        print("tidak ditemukan")
    jumlah_sensor_int= len(intensityRealShake)
    driver.close()

    #======================== CEK KONDISI INTENSITYMETER REIS =================================#
    sensoroff_int_reis= []
    sensoroff_int_reis_latency= []
    jumlah_on_int_reis = 0
    jumlah_off_int_reis = 0
    webpage_simora = requests.get("https://simora.bmkg.go.id/slmon/")
    soup = BeautifulSoup(webpage_simora.content, "html.parser")
    for site in intensityReis :
      data = soup.find(string = site)
      if data == None:
        status = 'ON'
        jumlah_on_int_reis = jumlah_on_int_reis + 1
        continue
      data = data.find_parent("tr").text
      data = ' '.join(data.split())
      data1 = data.split(' ')
      kodesensor = data1[1]
      lastdata = data1[2]  + data1[3]
      waktu = float(data1[2])
      satuan = data1[3]
      if satuan == 's':
        status = 'ON'
        jumlah_on_int_reis = jumlah_on_int_reis +1

      elif waktu < 40 and satuan == 'm':
        status = 'ON'
        jumlah_on_int_reis = jumlah_on_int_reis + 1
      else:
        if satuan =='d' and waktu > 2:
          status = 'ON'
          jumlah_on_int_reis = jumlah_on_int_reis + 1
          continue
        status = 'OFF'
        jumlah_off_int_reis = jumlah_off_int_reis + 1
        sensoroff_int_reis_latency.append(site + " " + data1[2] + " " + data1[3])
        sensoroff_int_reis.append(site)
        siteOff.append(site)

    jumlah_sensor_int_reis= len(intensityReis)

    ##===================== CEK KONDISI WRS ============================##
    driver = webdriver.Chrome()
    # username = 'sanglah@wrs.id'
    # password = 'sanglah'
    username = 'bawil3@wrs.id'
    password = 'bawil3'
    driver.get("http://202.90.199.203:3000/login")

    driver.find_element("name", "user").send_keys(username)
    driver.find_element("name", "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "css-6ntnx5-button").click()






    balai = open('balai.txt' , 'r')
    data_balai = balai.readlines()
    status_balai = data_balai[0].replace('\n' , '')
    modem_up_balai = int(data_balai[2].split(' ')[2].replace('\n' , ''))
    modem_down_balai = int(data_balai[3].split(' ')[2].replace('\n' , ''))
    display_up_balai = int(data_balai[4].split(' ')[2].replace('\n' , ''))
    display_down_balai = int(data_balai[5].split(' ')[2].replace('\n' , ''))

    sanglah = open('sanglah.txt' , 'r')
    data_sanglah = sanglah.readlines()
    status_sanglah = data_sanglah[0].replace('\n' , '')
    modem_up_sanglah = int(data_sanglah[2].split(' ')[2].replace('\n' , ''))
    modem_down_sanglah = int(data_sanglah[3].split(' ')[2].replace('\n' , ''))
    display_up_sanglah = int(data_sanglah[4].split(' ')[2].replace('\n' , ''))
    display_down_sanglah = int(data_sanglah[5].split(' ')[2].replace('\n' , ''))

    modem_up = modem_up_balai + modem_up_sanglah
    modem_down = modem_down_balai +modem_down_sanglah
    display_up = display_up_balai + display_up_sanglah
    display_down = display_down_balai + display_down_sanglah
    jumlah_wrs = modem_down + modem_up

    if status_sanglah == 'tidak ada perubahan' and status_balai == 'tidak ada perubahan':
        status_wrs = 'tidak ada perubahan'
    else:
        status_wrs = 'ada perubahan'

    ########################SQL##########################

    mycursor = mydb.cursor()
    sql = "UPDATE tbl_intensity SET kondisi_terkini = %s WHERE kondisi_terkini = %s"
    val = ("ON", "OFF")

    mycursor.execute(sql, val)
    sql = "UPDATE tbl_seismo SET kondisi_terkini = %s WHERE kondisi_terkini = %s"
    val = ("ON", "OFF")

    mycursor.execute(sql, val)
    sql = "UPDATE tbl_acc_noncolo SET kondisi_terkini = %s WHERE kondisi_terkini = %s"
    val = ("ON", "OFF")

    mycursor.execute(sql, val)
    sql = "UPDATE tbl_int_reis SET kondisi_terkini = %s WHERE kondisi_terkini = %s"
    val = ("ON", "OFF")

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

    for a in sensoroff_int:
        sql = "UPDATE tbl_intensity SET kondisi_terkini = %s WHERE kode = %s"
        val = ("OFF" , a)
        mycursor.execute(sql, val)
    for a in sensoroff_acc_noncolo:
        sql = "UPDATE tbl_acc_noncolo SET kondisi_terkini = %s WHERE kode = %s"
        val = ("OFF" , a)
        mycursor.execute(sql, val)
    for a in sensoroff_seis:
        sql = "UPDATE tbl_seismo SET kondisi_terkini = %s WHERE kode = %s"
        val = ("OFF" , a)
        mycursor.execute(sql, val)
    for a in sensoroff_int_reis:
        sql = "UPDATE tbl_int_reis SET kondisi_terkini = %s WHERE kode = %s"
        val = ("OFF" , a)
        mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()


    ##CETAK LAPORAN
    laporan = f"""Izin Pimpinan, Izin melaporkan status Aloptama Stageof Denpasar
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

STATUS SEISMOMETER
Jumlah Sensor : {jumlah_sensor_seis}
ON : {jumlah_on_seis}
OFF : {jumlah_off_seis} 
Sensor OFF : {sensoroff_seis_latency}

STATUS ACCELEROMETER
Jumlah Sensor : {jumlah_sensor_acc}
ON : {jumlah_on_acc}
OFF : {jumlah_off_acc} 
Sensor OFF : {sensoroff_acc_latency}

STATUS ACCELEROMETER NON COLOCATED
Jumlah Sensor : {jumlah_sensor_acc_noncolo}
ON : {jumlah_on_acc_noncolo}
OFF : {jumlah_off_acc_noncolo} 
Sensor OFF : {sensoroff_acc_noncolo_latency}

STATUS INTENSITYMETER
Jumlah Sensor : {jumlah_sensor_int}
ON : {jumlah_on_int}
OFF : {jumlah_off_int} 
Sensor OFF : {sensoroff_int_latency}

STATUS INTENSITYMETER REIS
Jumlah Sensor : {jumlah_sensor_int_reis}
ON : {jumlah_on_int_reis}
OFF : {jumlah_off_int_reis} 
Sensor OFF : {sensoroff_int_reis_latency}

STATUS WRS NG
Modem Up : {modem_up}
Modem Down : {modem_down}
Display Up : {display_up}
Display Down : {display_down} 
    """

    ## CEK SITE YANG OFF DARI DATA SEBELUMNYA
    print(laporan)
    z = open("siteOff.txt", 'r')
    siteOffYanglama2 = z.readline().replace("\n", "")
    siteOffYanglama2 = siteOffYanglama2.split(" ")
    z.close()
    siteOffYangLama = []
    for x in siteOffYanglama2:
        if x != "":
            siteOffYangLama.append(x)

    ##UPDATE SITE OFF
    siteYangOff = ""
    for a in siteOff:
        siteYangOff = siteYangOff + a + " "
    f = open("siteOff.txt", "w")
    f.write(siteYangOff)
    f.close()

    ##PROSES PENGIRIMAN LAPORAN Whatsapp
    if (siteOff == siteOffYangLama and status_wrs == 'tidak ada perubahan'):
        print("TIDAK ADA PERUBAHAN")
        f = open("status.txt", "w")
        f.write(laporan)
        f.close()
    else:
        print("ADA PERUBAHAN !!!")
        f = open("status.txt", "w")
        f.write(laporan)
        f.close()

        # {myresult[0]}
       #  pywhatkit.sendwhatmsg_to_group_instantly('L8hb3ciK8prAyXsoR0WX4S',laporan,15,True,3,)
        # await update.message.reply_text('L8hb3ciK8prAyXsoR0WX4S',laporan,15,True,3,)
        # laporan=(f"'{laporan}")
    await update.message.reply_text(laporan)
    sys.exit()
    print(laporan)

    #  jam_sekarang = datetime.now().strftime("%H")

    # try:
    #  a = jam_pengiriman.index(jam_sekarang)
    #  f = open("status.txt", "w")
    #  f.write(laporan)
    #  f.close()
    #  print("WAKTU PENGIRIMAN")
    # pywhatkit.sendwhatmsg_to_group_instantly('L8hb3ciK8prAyXsoR0WX4S',laporan,15,True,3,)
    # await update.message.reply_text('L8hb3ciK8prAyXsoR0WX4S', laporan, 15, True, 3, )
    #  await update.message.reply_text(laporan)
    # except:
    #  print("bukan jam kirim")

    # print(f"'{laporan}")