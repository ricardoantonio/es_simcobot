import sqlite3
import os

from telegram import parsemode
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN_V2

def del_company(update, context):
    company_name = ' '.join(context.args)

    # Conexion a la DB
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, 'simcobot.db'))
    cur = conn.cursor()
    try:
        cur.execute('''DELETE FROM companies WHERE name = ?''', (company_name, ))
        msg = 'La compañia <b>{}</b> ha sido eliminada del ranking.'.format(company_name)
        conn.commit()

    except:
        msg = 'No se encontró a <b>{}</b> en la base de datos.'.format(company_name)
    conn.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML)
