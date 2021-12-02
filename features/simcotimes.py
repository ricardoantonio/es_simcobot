import os
import re
import sqlite3
from urllib.request import urlopen
import urllib.error
import json
import ssl
from time import sleep
from telegram.constants import PARSEMODE_HTML

CLEAN_HTML = re.compile('<.*?>')

def get_simco_times(updater, chat_id):
    print('Buscando SimCompanies Times')

    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, '../data/simcobot.db'))
    cur = conn.cursor()
    cur.execute('''SELECT value FROM configurations WHERE parameter="sctimes_edition"''')
    edition = cur.fetchone()[0]
    conn.close()
    print(edition)

    # Conexion a la API
    service_url = 'https://www.simcompanies.com/api/v3/es/newspaper/'
    # Ignorar errores de certificado SSL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = service_url + str(edition)

    js = None

    while not js:
        try:
            uh = urlopen(url, context=ctx)
            datos = uh.read().decode()
        except urllib.error.HTTPError as err:
            if err.code == 404:
                datos = None
        try:
            js = json.loads(datos)
        except:
            js = None
        if js: break
        sleep(60)

    msg = '<b>NUEVA EDICIÓN DE SIMCOMPANIES TIMES</b>\n\n'.format(edition)
    for i, article in enumerate(js['articles']):
        text = re.sub(CLEAN_HTML, '', article['copy1']).replace('\n', ' ')
        msg += '<b>{}. {}</b>\n{}\n'.format(i+1, article['title'].replace('\n', ' '), text[:100]+'...')
    msg += '\n\nhttps://www.simcompanies.com/es/newspaper/{}/'.format(edition)

    updater.bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=PARSEMODE_HTML)

    conn = sqlite3.connect(os.path.join(dir_path, '../data/simcobot.db'))
    cur = conn.cursor()
    cur.execute('''UPDATE configurations SET value = ?''', (edition + 1,))
    conn.commit()
    conn.close()
