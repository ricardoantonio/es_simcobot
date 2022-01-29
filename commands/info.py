from telegram.constants import PARSEMODE_HTML

def info(update, context):
    msg = ('<b>Sim Companies Comunidad en Español</b>'
    '\nChat General:'
    '\nhttps://t.me/+7e9LQzWvos9hNWFh'
    '\nCanal de Información:'
    '\n@SimCompaniesEs'
    '\n\nChat de Ventas:'
    '\n@SCCEChatDeVentas'
    '\n\nSimbloteca'
    '\n@Simbloteca')
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML, disable_web_page_preview=True)