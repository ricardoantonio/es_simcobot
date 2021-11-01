import logging
import sqlite3
import os
import datetime

def get_ranking_msg():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, '../data/simcobot.db'))
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
            msg += '<b>{} {}</b>\n      $ {:,d} ({:.2%})\n'.format(
                rank, company[0], company[1], company[2] / 100)

    except:
        msg = 'Hubo un error al generar el ranking, vuelve a intentarlo.'

    conn.close()

    return msg
    