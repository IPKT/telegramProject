from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes , CallbackContext
import os
import re
import mysql.connector
from rahasia import hehe
from pending_notes import pending_notes  # Import variabel pending_notes
async def capture_note(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Cek apakah user memang sedang menunggu untuk menulis catatan
    if user_id in pending_notes:
        new_entry = update.message.text
        pending_notes[user_id].append(new_entry)
        await update.message.reply_text(f"Catatan berhasil ditambahkan: {new_entry}")
        # Jika user mengetikkan "selesai", simpan ke dalam file dan bersihkan catatan sementara
        if new_entry.lower() == "selesai":
            with open('catatanTeknisi.txt', 'a') as file:
                for note in pending_notes[user_id][:-1]:  # Exclude "selesai" from catatan
                    file.write(f"{note}\n")
            del pending_notes[user_id]  # Hapus user dari daftar yang menunggu

# Fungsi handler untuk command /cancel (opsional)
async def cancel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in pending_notes:
        del pending_notes[user_id]
        await update.message.reply_text("Penambahan catatan dibatalkan.")