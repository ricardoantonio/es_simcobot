import logging
from common_functions.ranking import get_ranking_msg

from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN_V2


def ranking(update, context):
    logging.info('SOLICITÓ RANKING: %s en %s', update.message.from_user['first_name'], update.message.chat.type)

    if update.message.chat.type == 'private':
        msg = get_ranking_msg()
    else:
        msg = "ℹ️ <b>El ranking ahora está en los mensajes fijados.</b> Pronto este comando quedará deshabilitado."

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML)