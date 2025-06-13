from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '7671100794:AAGAnId-R2OxrEJBSDpVzhejTfEuKwNUTrk'
OWNER_CHAT_ID = 5493055535

clients = set()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Здравей! Пиши ми съобщение и ще ти отговоря.")

def client_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    clients.add(user_id)

    if update.message.text:
        text = f"От клиент {user_id}:\n{update.message.text}"
        context.bot.send_message(chat_id=OWNER_CHAT_ID, text=text)
    elif update.message.photo:
        photo_file = update.message.photo[-1].file_id
        caption = f"От клиент {user_id}: снимка"
        context.bot.send_photo(chat_id=OWNER_CHAT_ID, photo=photo_file, caption=caption)
    elif update.message.video:
        video_file = update.message.video.file_id
        caption = f"От клиент {user_id}: видео"
        context.bot.send_video(chat_id=OWNER_CHAT_ID, video=video_file, caption=caption)

def reply_to_client(update: Update, context: CallbackContext):
    try:
        client_id = int(context.args[0])
        reply_text = ' '.join(context.args[1:])
        context.bot.send_message(chat_id=client_id, text=reply_text)
        update.message.reply_text(f"Изпратихте съобщение на {client_id}")
    except (IndexError, ValueError):
        update.message.reply_text("Използване: /reply <client_id> <съобщение>")

def send_photo(update: Update, context: CallbackContext):
    try:
        client_id = int(context.args[0])
        photo_url = context.args[1]
        context.bot.send_photo(chat_id=client_id, photo=photo_url)
        update.message.reply_text(f"Изпратена снимка на {client_id}")
    except:
        update.message.reply_text("Използване: /sendphoto <client_id> <url_на_снимката>")

def send_video(update: Update, context: CallbackContext):
    try:
        client_id = int(context.args[0])
        video_url = context.args[1]
        context.bot.send_video(chat_id=client_id, video=video_url)
        update.message.reply_text(f"Изпратено видео на {client_id}")
    except:
        update.message.reply_text("Използване: /sendvideo <client_id> <url_на_видеото>")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reply", reply_to_client))
    dp.add_handler(CommandHandler("sendphoto", send_photo))
    dp.add_handler(CommandHandler("sendvideo", send_video))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, client_message))
    dp.add_handler(MessageHandler(Filters.photo, client_message))
    dp.add_handler(MessageHandler(Filters.video, client_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
