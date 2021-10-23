from decouple import config
from telegram.constants import PARSEMODE_HTML


def new_member(updater, context):
    chat_id = config('LOGCHATID')

    for member in updater.message.new_chat_members:
        print('MIEMBRO:', member)
        msg = f"👤 <b>{member.full_name}</b> se ha unido al grupo."
        if member['is_bot']:
            msg += '\n️⚠️ Es probable que se trate de un bot.\n¿Alguien puede verificar?'
        else:
            msg += '¿Ya le dieron la bienvenida?'

    try:
        context.bot.send_message(chat_id=updater.effective_chat.id, text='¡Hola, {}! Bienvenid@ a <b><i>Sim Companies ES</i></b> 🇲🇽🇨🇱🇪🇸🇨🇴🇨🇺🇪🇨🇩🇴🇬🇶🇸🇻🇬🇹🇭🇳🇳🇮🇵🇦🇵🇾🇵🇪🇵🇷🇺🇾🇻🇪🇦🇷\n\n"Antes que nada por favor presentate con un nombre y el nombre de tu empresa, ya que unicamente miembros activos y reales pueden quedarse."\n\nDiviertanse Amig@s 😄 Recuerden Leer las /reglas y Para Más Información Pon /info'.format(member.full_name), parse_mode=PARSEMODE_HTML)
    except:
        print('No se pudo enviar el mensaje de bienvenida')

    try:
        context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=PARSEMODE_HTML)
    except:
        print('No se pudo enviar el mensaje de aviso al log')
