import logging
import sqlite3
import os
from common_functions.ranking import get_ranking_msg
from telegram.constants import PARSEMODE_HTML


def pin_ranking(update, chat_id):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, '../data/simcobot.db'))
    cur = conn.cursor()
    logging.info('CALCULANDO RANKING DEL DÍA')

    msg = get_ranking_msg()

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