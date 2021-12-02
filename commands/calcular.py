from telegram.constants import PARSEMODE_HTML


operators = ['+', '-']

def get_data(input):
    data = []
    count = 0
    for i in range(len(input)):
        if input[i] in operators:
            data.append(input[count:i].strip())
            data.append(input[i])
            count = i + 1
        if i == len(input) - 1:
            data.append(input[count:].strip())
    return data

def calculate(data):
    if len(data) != 3:
        return "Error - Solo se permiten 2 operandos"
    try:
        if '%' in data[2]:
            data[2] = data[2].replace('%', '')
            data[2] = float(data[0]) / 100 * float(data[2])
        if data[1] == '+':
            return float(data[0]) + float(data[2])
        elif data[1] == '-':
            return float(data[0]) - float(data[2])
    except:
        return "Error - Solo se permiten numeros y % en el segudno operando"


def calcular(update, context):
    datos = ''.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text='{} = <b>{}</b>'.format(datos,calculate(get_data(datos))), reply_to_message_id=update.message.message_id, parse_mode=PARSEMODE_HTML)
    