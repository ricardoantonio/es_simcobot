from telegram.constants import PARSEMODE_HTML

def info(update, context):
    msg = ('<b>INFORMACIÓN</b>')
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode=PARSEMODE_HTML, disable_web_page_preview=True)