from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re
from IP import IP
from hardware import hardware
from help import help
from login import login
from enkrip import enkrip
from dekrip import dekrip

app = ApplicationBuilder().token("7193995386:AAEHW6pBcZgI4EBWy2jB8MGsOYEvfsTvVqE").build()

app.add_handler(CommandHandler("ip", IP))
app.add_handler(CommandHandler("hardware", hardware))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("login", login))
app.add_handler(CommandHandler("enkrip", enkrip))
app.add_handler(CommandHandler("dekrip", dekrip))


app.run_polling()