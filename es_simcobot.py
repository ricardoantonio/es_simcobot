import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from decouple import config
from commands.addcompany import add_company
from commands.delcompany import del_company
from commands.ranking import ranking
from commands.help import help
from commands.rules import rules
from commands.info import info
from commands.algo import get_algo_price
from features.simcotimes import get_simco_times
from features.ranking import pin_ranking
from features.newmembers import new_member
from commands.calcular import calcular
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 1. DEFINIR COMANDOS (Se han difinido en la carpeta commands)


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
    help_handler = CommandHandler('ayuda', help)
    reglas_handler = CommandHandler('reglas', rules)
    info_handler = CommandHandler('info', info)
    new_member_handler = MessageHandler(Filters.status_update.new_chat_members, new_member)
    calcular_handler = CommandHandler('calcular', calcular)
    algo_handler = CommandHandler('precioalgo', get_algo_price)

    # 3. REGISTRAR MANEJADORES
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(add_company_handler)
    dispatcher.add_handler(del_company_handler)
    dispatcher.add_handler(ranking_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(reglas_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(new_member_handler)
    dispatcher.add_handler(calcular_handler)
    dispatcher.add_handler(algo_handler)

    # Start the bot
    updater.start_polling()

    # Tareas programadas
    GROUP_ID = config('GROUPID')
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_simco_times, 'cron', args=[updater, GROUP_ID], day_of_week='thu', hour=16, minute=2,
                      timezone='UTC', misfire_grace_time=120)
    
    scheduler.add_job(pin_ranking, 'cron', args=[updater, GROUP_ID], hour=2, minute=5,
                      timezone='UTC', misfire_grace_time=120)
    scheduler.start()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
