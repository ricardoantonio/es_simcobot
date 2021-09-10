import logging
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from decouple import config
from commands.addcompany import add_company
from commands.delcompany import del_company
from commands.ranking import ranking

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. DEFINIR COMANDOS 
def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Pong!')

def main():
    BOT_TOKEN = config('TOKEN')
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    # 2. CREAR MANEJADORES
    ping_handler = CommandHandler('ping', ping)
    add_company_handler = CommandHandler('agregar', add_company)
    del_company_handler = CommandHandler('eliminar', del_company)
    ranking_handler = CommandHandler('ranking', ranking)

    # 3. REGISTRAR MANEJADORES
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(add_company_handler)
    dispatcher.add_handler(del_company_handler)
    dispatcher.add_handler(ranking_handler)

    # Start the bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
