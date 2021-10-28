import logging
import sqlite3
import os
import datetime

from telegram.constants import PARSEMODE_HTML


def put_ranking(update, chat_id):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, '../commands/simcobot.db'))
    cur = conn.cursor()
    logging.info('CALCULANDO RANKING')
    try:
        cur.execute(
            '''SELECT name, value, growth FROM companies ORDER BY value DESC''')
        datos = cur.fetchall()

        msg = '🏆 <b>RANKING POR VALOR DE COMPAÑÍA</b> 🏆\n'
        msg += datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ' UTC\n\n'
        msg += '<i>Para aparecer en el ranking usa el comando <pre>/agregar</pre> y el nombre de tu compañía tal como aprece en el juego.</i>\n\n'

        for i, company in enumerate(datos):
            if i == 0:
                rank = '🥇'
            elif i == 1:
                rank = '🥈'
            elif i == 2:
                rank = '🥉'
            else:
                rank = str(i + 1) + '.'
            msg += '<b>{} {}</b>\n      $ {:,.2f} ({:.2%})\n'.format(
                rank, company[0], company[1], company[2] / 100)

        msg += '\n<i>Para aparecer en el ranking usa el comando <pre>/agregar</pre> y el nombre de tu compañía tal como aprece en el juego.</i>'

    except:
        msg = 'Hubo un error al generar el Top, vuelve a intentarlo.'

    try:
        cur.execute('''SELECT value FROM configurations WHERE parameter="last_ranking_id"''')
        last_ranking_id = cur.fetchone()[0]
        update.bot.unpin_chat_message(chat_id=chat_id, message_id=last_ranking_id)
    except:
        logging.info('No existe ranking fijado')

    ranking_msg_sent = update.bot.send_message(
        chat_id=chat_id, text=msg, parse_mode=PARSEMODE_HTML)
    update.bot.pinChatMessage(ranking_msg_sent['chat']['id'], ranking_msg_sent['message_id'])
    
    try:
        cur.execute('''INSERT INTO configurations (parameter, value) VALUES ("last_ranking_id", ?)''', (ranking_msg_sent['message_id'],))
    except:
        cur.execute('''UPDATE configurations SET value=? WHERE parameter="last_ranking_id"''', (ranking_msg_sent['message_id'],))

    conn.commit()
    conn.close()