import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import sqlite3
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

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
    print("recuperando datos de:", url)
    try:
        uh = urllib.request.urlopen(url, context=ctx)
        datos = uh.read().decode()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            datos = None  

    try:
        js = json.loads(datos)
    except:
        js = None

    if js:
        cur.execute('''UPDATE companies SET name = ?, value = ? WHERE idCompany = ?''',(js['player']['company'], js['player']['history']['value'], js['player']['id']))
        conn.commit()

conn.close()

