import sqlite3
import os
import logging

from telegram import parsemode
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN_V2


def del_company(update, context):
    company_name = ' '.join(context.args)

    if len(company_name) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Incluye junto al comando el nombre de la compañía que deseas eliminar de la lista', reply_to_message_id=update.message.message_id)
        return

    logging.info("ELIMINAR COMPAÑIA: Solicitante: %s - Compañia: %s", update.message.from_user['first_name'], company_name)

    # Conexion a la DB
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, 'simcobot.db'))
    cur = conn.cursor()
    cur.execute('''SELECT name FROM companies WHERE name = ?''',
                (company_name, ))
    company = cur.fetchone()

    if not company:
        msg = 'No se encontró a <b>{}</b> en la lista. ¿Seguro que escribiste bien el nombre de la empresa?'.format(
            company_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg,
                                 parse_mode=PARSEMODE_HTML, reply_to_message_id=update.message.message_id)
        return

    try:
        cur.execute('''DELETE FROM companies WHERE name = ?''',
                    (company_name, ))
        msg = 'La compañia <b>{}</b> ha sido eliminada del ranking.'.format(
            company_name)
        conn.commit()
    except:
        msg = 'Ocurrió un error al intentar eliminar a la empresa del ranking.'.format(
            company_name)
    conn.close()

    logging.info("COMPAÑÍA ELIMINADA: %s", company_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg,
                             parse_mode=PARSEMODE_HTML, reply_to_message_id=update.message.message_id)
