import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import sqlite3
import os
import logging

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

conn = sqlite3.connect(os.path.join(dir_path, 'commands/simcobot.db'))
cur = conn.cursor()

cur.execute('''SELECT idCompany FROM companies''')
players = cur.fetchall()

for player in players:
    url = service_url + str(player[0]) + '/'
    logger.debug("recuperando datos de: %s", url)
    try:
        uh = urllib.request.urlopen(url, context=ctx)
        datos = uh.read().decode()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            datos = None
            logger.warning("Error al recuperar: %s", url)

    try:
        js = json.loads(datos)
    except:
        js = None
        logger.warning("No hay datos: %s", url)

    if js:

        cur.execute(
            '''SELECT value FROM companies WHERE idCompany = ?''', (js['player']['id'],))
        last_value = cur.fetchone()[0]

        if last_value != 0:
            growth = round(
                ((js['player']['history']['value'] * 100) / last_value) - 100, 2)
        else:
            growth = 100
        
        logger.debug("Datos: %d %s %d %f", js['player']['id'], js['player']['company'], js['player']['history']['value'], growth)

        cur.execute('''UPDATE companies SET name = ?, value = ?, growth = ? WHERE idCompany = ?''',
                    (js['player']['company'], js['player']['history']['value'], growth, js['player']['id']))
        conn.commit()

conn.close()
