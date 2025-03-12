from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers import *
from config import TOKEN

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FILE: [MessageHandler(filters.Document.AUDIO | filters.AUDIO, handle_file)],
            ARTIST_SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_artist_search)],
            ARTIST_SELECT: [CallbackQueryHandler(process_artist_selection)],
            ALBUM_SELECT: [CallbackQueryHandler(process_album_selection)],
            TRACK_SELECT: [CallbackQueryHandler(process_track_selection)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(CommandHandler('help', help_command))

    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Бот остановлен.")
