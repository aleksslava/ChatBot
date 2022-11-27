import telebot
from extensions import Crypto_Convertor, APIException
from config import keys, TOKEN



bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands= ['start', 'help'])
def start(message: telebot.types.Message):
    text = """Для конвертации валюты, необходимо отправить сообщение следующего вида:
    <имя валюты цену которой вы хотите узнать><имя валюты в которой надо узнать цену первой валюты>
    <количество первой валюты>.\nЧтобы увидеть список доступных валют, введите: /value"""
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text = '\n'.join((text, i,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException("Неверное количество параметров")
        quote, base, amount = values
        total_base = Crypto_Convertor.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()