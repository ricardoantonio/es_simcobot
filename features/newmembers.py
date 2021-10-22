from decouple import config
from telegram.constants import PARSEMODE_HTML


def new_member(updater, context):
    chat_id = config('LOGCHATID')

    for member in updater.message.new_chat_members:
        print('MIEMBRO:', member)
        msg = f"👤 <b>{member.full_name}</b> se ha unido al grupo."
        if member['is_bot']:
            msg += '\n️⚠️ Es probable que se trate de un bot.'
        msg += '\n¿Alguien puede verificar?'

    try:
        context.bot.send_message(chat_id=updater.effective_chat.id, text="¡Hola, {}! Bienvenid@ a <b><i>Sim Companies ES</i></b> 🇲🇽🇨🇱🇪🇸🇨🇴🇨🇺🇪🇨🇩🇴🇬🇶🇸🇻🇬🇹🇭🇳🇳🇮🇵🇦🇵🇾🇵🇪🇵🇷🇺🇾🇻🇪🇦🇷\nNo olvides presentarte mencionando cuál es tu compañía. 😄".format(member.full_name), parse_mode=PARSEMODE_HTML)
    except:
        print('No se pudo enviar el mensaje de bienvenida')

    try:
        context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=PARSEMODE_HTML)
    except:
        print('No se pudo enviar el mensaje')
