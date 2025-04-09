







import telebot
import requests

TOKEN = '7575897337:AAFPboSmtvE0t_EaGtgXPqwrzskQ1AEyIPg'
CHAT_ID = '7009947090'
bot = telebot.TeleBot(TOKEN)

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def check_signal():
    price = get_price('BTCUSDT')
    if price > 70000:
        return "Sell Signal"
    elif price < 65000:
        return "Buy Signal"
    else:
        return "No clear signal"

@bot.message_handler(commands=['signal'])
def signal(message):
    signal = check_signal()
    bot.send_message(message.chat.id, f"BTCUSDT: {signal}")

print("Bot started...")
bot.polling()
