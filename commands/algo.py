from telegram.constants import PARSEMODE_HTML
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_algo_price(update, context):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      'id':'4030',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'a53467a7-8555-4f03-8bdc-bf04668a6a7c',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = data['data']['4030']['quote']['USD']['price']
        change1h = float(data['data']['4030']['quote']['USD']['percent_change_1h'])/100
        change24h = float(data['data']['4030']['quote']['USD']['percent_change_24h'])/100
        date = data['data']['4030']['quote']['USD']['last_updated']
        msg = '<b>ALGO</b>\n\nPrecio: <b>$ {:.4f} USD</b>\n\nCambio 1h: <b>{:.2%}</b>\nCambio 24h: <b>{:.2%}</b>\n\nÚltima actualización: {}'.format(price, change1h, change24h, date)
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_to_message_id=update.message.message_id, parse_mode=PARSEMODE_HTML)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)