import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import sqlite3
import os
import logging
import time

# Obtener la ruta absolute
dir_path = os.path.dirname(os.path.abspath(__file__))

# create logger
logger = logging.getLogger('GETCV')
logger.setLevel(logging.DEBUG)
# create console handlers and set level to debug
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
# create file handlers and set level to debug
output_file_handler = logging.FileHandler(
    os.path.join(dir_path, 'getcv.log'))
output_file_handler.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
# add formatter
stdout_handler.setFormatter(formatter)
output_file_handler.setFormatter(formatter)
# add handlers to logger
logger.addHandler(stdout_handler)
logger.addHandler(output_file_handler)

logger.info('===== Comenzando el proceo de actualización =====')

service_url = 'https://www.simcompanies.com/api/v2/players/'
# Ignorar errores de certificado SSL
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect(os.path.join(dir_path, 'data/simcobot.db'))
cur = conn.cursor()

cur.execute('''SELECT idCompany FROM companies''')
players = cur.fetchall()
total_players = len(players)

for i, player in enumerate(players):

    url = service_url + str(player[0]) + '/'
    logger.debug("%d de %d - %s", i + 1, total_players, url)

    try:
        uh = urllib.request.urlopen(url, context=ctx)
        datos = uh.read().decode()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            datos = None
            logger.warning("ERROR AL RECUPERAR: %s", url)

    try:
        js = json.loads(datos)
    except:
        js = None
        logger.warning("NO HAY DATOS: %s", url)

    if js:

        cur.execute(
            '''SELECT value FROM companies WHERE idCompany = ?''', (js['player']['id'],))
        last_value = cur.fetchone()[0]

        if last_value != 0:
            growth = round(
                ((js['player']['history']['value'] * 100) / last_value) - 100, 2)
        else:
            growth = 100
        

        cur.execute('''UPDATE companies SET name = ?, value = ?, growth = ? WHERE idCompany = ?''',
                    (js['player']['company'], js['player']['history']['value'], growth, js['player']['id']))
        conn.commit()

        logger.debug("Datos guardados: %d %s %d %f", js['player']['id'], js['player']['company'], js['player']['history']['value'], growth)
    
    time.sleep(1) # Esperamos un segundo antes de la siguiente llamada para no superar el límite de llamadas

conn.close()
