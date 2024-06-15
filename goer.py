from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
import mysql.connector
from rahasia import hehe
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
path = "chromedriver.exe"

from selenium import webdriver

async def goer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    driver = webdriver.Chrome()
    # username = 'sanglah@wrs.id'
    # password = 'sanglah'
    username = 'putu.kembar@gmail.com'
    password = 'kembar12345'
    driver.get("https://gem.goersapp.com/")

    # driver.find_element("class", "imFarj").send_keys(username)
    try:
        cek = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "imFarj"))
        )
        # driver.find_element(By.CLASS_NAME, "kAaFY").click()
    except:
        time.sleep(100)
    driver.find_element(By.CLASS_NAME, "imFarj").send_keys(username)
    driver.find_element(By.CLASS_NAME, "BcycW").send_keys(password)
    driver.find_element(By.CLASS_NAME, "khXNhG").click()
    # driver.find_element("name", "password").send_keys(password)
    # driver.find_element(By.CLASS_NAME,"css-6ntnx5-button").click()
    # time.sleep(5)
    # driver.find_element(By.CLASS_NAME, "kAaFY").click()
    try:
        cek = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "kAaFY"))
        )
        driver.find_element(By.CLASS_NAME, "kAaFY").click()
        time.sleep(30)
    except:
        time.sleep(100)
    # haha = driver.find_element(By.CLASS_NAME,"eBBb0h").text
    hihi = driver.find_element(By.XPATH,
                               "/html/body/main/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/div[1]")
    # print(hihi.text)
    if update.message.from_user.id == 5121796183:
        pesan = f"""Halloo Ibu Koor cantik :D
Update Penjualan Tiket Musik PelipurLara
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Jumlah tiket terjual {hihi.text} 
Smangatt yaaa, jaga kesehatan 😊"""
    else:
        pesan = f"""Halloo !!!
Update Penjualan Tiket Musik PelipurLara
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Jumlah tiket terjual {hihi.text} 
Smangatt Team!!!"""




    # Balas pesan ke user
    await update.message.reply_text(pesan)