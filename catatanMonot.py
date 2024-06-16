# catatanTxt = open("C:/Users/PcMonitoring/PycharmProjects/monitoringOtomatisDNP/.venv/Lib/site-packages/catatan.txt", "r")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes , CallbackContext
import os
import re
import mysql.connector
from rahasia import hehe


# Fungsi handler untuk command /catatan
def catatan(update: Update, context: CallbackContext):
    update.message.reply_text("Silahkan isi catatan yang baru:")
    # Tambahkan user ID ke daftar catatan yang sedang ditunggu
    pending_notes[update.message.from_user.id] = []