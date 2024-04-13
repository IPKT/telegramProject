from telegram.ext import Updater, CommandHandler, CallbackContext
from rahasia import hehe

# Fungsi untuk menangani perintah /start
def start(update, context):
    update.message.reply_text('Halo! Saya adalah bot.')

def main():
    # Token bot yang Anda dapatkan dari BotFather
    TOKEN = hehe.myToken()

    # Inisialisasi Updater
    updater = Updater(TOKEN, use_context=True)

    # Dapatkan Dispatcher agar kita bisa mendaftarkan handler
    dp = updater.dispatcher

    # Daftarkan handler untuk perintah /start
    dp.add_handler(CommandHandler("start", start))

    # Mulai bot
    updater.start_polling()

    # Tunggu sampai bot dihentikan
    updater.idle()

if __name__ == '__main__':
    main()
