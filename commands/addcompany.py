import sqlite3
from urllib.request import urlopen
import urllib.error
import json
import ssl
import os

from telegram import parsemode
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN_V2

def add_company(update, context):
    company_name = ' '.join(context.args)

    if len(company_name) == 0: 
        context.bot.send_message(chat_id=update.effective_chat.id, text='Incluye junto al comando el nombre de la compañía que deseas añadir a la lista', reply_to_message_id=update.message.message_id)
        return

    # Conexion a la DB
    dir_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(dir_path, 'simcobot.db'))
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS companies (idCompany integer primary key, name text, logo text, value integer, growth float default 0)''')

    # Conexion a la API
    service_url = 'https://www.simcompanies.com/api/v2/players-by-company/'
    # Ignorar errores de certificado SSL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    msg = 'Se ha añadido <b>{}</b> al ranking!'.format(company_name)

    url = service_url + company_name.replace(' ', '-')+ '/'
    print("recuperando datos de:", url)
    try:
        uh = urlopen(url, context=ctx)
        datos = uh.read().decode()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            datos = None  
            msg = 'No se encontró a la compañía <b>{}</b>. Copia el nombre de tu perfil.'.format(company_name)

    try:
        js = json.loads(datos)
    except:
        js = None

    if js:
        print (js['player']['id'], js['player']['company'], js['player']['logo'], js['player']['history']['value'])
        cur.execute('''INSERT OR REPLACE INTO companies(idCompany, name, logo, value) VALUES (?, ?, ?, ?)''', (js['player']['id'], js['player']['company'], js['player']['logo'], js['player']['history']['value']))
        conn.commit()
    conn.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML, reply_to_message_id=update.message.message_id)
