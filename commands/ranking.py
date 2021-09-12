import sqlite3
import os

from telegram import parsemode
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN_V2

def ranking(update, context):
 
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, 'simcobot.db'))
    cur = conn.cursor()
    try:
        cur.execute('''SELECT name, value, growth FROM companies ORDER BY value DESC''')
        datos = cur.fetchall()

        msg = '🏆 <b>RANKING POR VALOR DE COMPAÑÍA</b> 🏆\n\n'
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
            msg += '<b>{} {}</b>\n<pre>  $ {:,.2f} ({:.2%})</pre>\n'.format(rank, company[0], company[1], company[2] / 100)

        msg += '\n<i>Para aparecer en el ranking usa el comando <pre>/agregar</pre> y el nombre de tu compañía tal como aprece en el juego.</i>'

    except:
        msg = 'Hubo un error al generar el Top, vuelve a intentarlo.'

    conn.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML)
