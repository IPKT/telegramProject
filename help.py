from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import re

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txtfile = open("help.txt","r")
    helper = txtfile.read()
    await update.message.reply_text(helper)