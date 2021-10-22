from telegram.constants import PARSEMODE_HTML

def rules(update, context):
    msg = ('<b>REGLAS</b>'
    '\n\n1-. Respetar a Todos Los Miembros'
    '\n2-. No Spam'
    '\n3-. No Compartir Contenido Porn 🔞'
    '\n4-. Apoyarse Entre Todos'
    '\n5-. Ser Educados'
    '\n6-. No Insultar'
    '\n7-. Evitar Discusiones y Peleas'
    '\n8-. Si Estás Inactivo Por Más de 30 Días Serás Eliminado de Los Grupos, Pero Podrás Regresar Más Tarde.'
    '\n9-. NOVEDAD: Todo Miembro Tendra Permitido el Uso de Enlaces. Pero Si Se Usan Mal, Seran Advertidos A La Primera, Silenciados A La Segunda y Hasta Expulsados A La Tercera!'
    '\n\n<i>Si Desobedeces las Reglas, los Administradores te  Advertirán! Y Si Continuas No Respetándolas, Podrás Ser Expulsado Del Grupo.</i>'
    )
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML, disable_web_page_preview=True)