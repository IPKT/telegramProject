from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
from info import info
from ip import ip
from hardware import hardware
from help import help
from login import login
from start import start
from goer import goer
from enkrip import enkrip
from dekrip import dekrip
from rahasia import hehe
from rekapKunjungan import rekapKunjungan
token = hehe.myToken()
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("ip", ip))
app.add_handler(CommandHandler("hardware", hardware))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("login", login))
app.add_handler(CommandHandler("start", start))
# app.add_handler(CommandHandler("enkrip", enkrip))
# app.add_handler(CommandHandler("dekrip", dekrip))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("goer", goer))
app.add_handler(CommandHandler("rekapKunjungan", rekapKunjungan))


app.run_polling()