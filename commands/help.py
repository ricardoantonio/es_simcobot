from telegram.constants import PARSEMODE_HTML

def help(update, context):
    msg = ('<b>¡Hola! Soy SimCo Bot.</b> Esta es la lista de comandos disponibles.'
    '\n\n/ranking - Muestra el ranking, no disponible en grupos, solo en mensajes privados.'
    '\n/agregar <i>NOMBRE DE LA EMPRESA</i> - Agrega tu empresa a la lista'
    '\n/eliminar <i>NOMBRE DE LA EMPRESA</i> - Elimina tu empresa de la lista'
    '\n\n<i>En todos los casos donde se pide el <b>NOMBRE DE LA EMPRESA,</b> es necesario que la escribas <b>tal como aparece en el juego.</b> Lo mejor es copiarla de tu perfil. Recuerda dejar un espacio entre el comando y el nombre de tu empresa.</i>'
    '\n\n<b>El ranking se actualiza todos los días a las <a href="https://time.is/es/UTC">02:00 UTC</a>.</b>')
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML, disable_web_page_preview=True)