

import requests
import matplotlib.pyplot as plt
import io
import time
import telebot

# Telegram bot token aur chat_id
TOKEN = '7575897337:AAFPboSmtvE0t_EaGtgXPqwrzskQ1AEyIPg'
CHAT_ID = '7009947090'

bot = telebot.TeleBot(TOKEN)

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def get_banknifty_price():
    # Simulated price (live API chahiye toh bata dena)
    return 47380  # Example price

def check_btc_signal():
    price = get_price('BTCUSDT')
    if price > 70000:
        return "Sell Signal", price
    elif price < 65000:
        return "Buy Signal", price
    else:
        return "No clear signal", price

def check_banknifty_signal():
    price = get_banknifty_price()
    target = 47450
    stoploss = 47200
    if price > target:
        signal = "Sell Signal"
    elif price < stoploss:
        signal = "Buy Signal"
    else:
        signal = "Buy Signal"
    profit_potential = abs(price - target)
    return signal, price, target, stoploss, profit_potential

def plot_chart(prices, symbol):
    plt.figure(figsize=(6, 4))
    plt.plot(prices, marker='o')
    plt.title(f'{symbol} Price Chart')
    plt.xlabel('Time')
    plt.ylabel('Price')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def send_update():
    # BTC
    btc_signal, btc_price = check_btc_signal()
    btc_message = f"BTCUSDT: {btc_signal}\nCurrent Price: ${btc_price}\nNext update in: 5 min"
    bot.send_message(CHAT_ID, btc_message)

    # BankNifty
    bank_signal, bank_price, target, stoploss, profit_potential = check_banknifty_signal()
    bank_message = (
        f"BANKNIFTY: {bank_signal}\n"
        f"Current Price: ₹ {bank_price}\n"
        f"Target: ₹ {target}\n"
        f"Stoploss: ₹ {stoploss}\n"
        f"Profit Potential: ₹ {profit_potential}\n\n"
        f"Next update in: 5 min"
    )
    bot.send_message(CHAT_ID, bank_message)

    # Dummy prices for chart
    prices = [47200, 47300, bank_price, 47400, 47450]
    chart = plot_chart(prices, "BANKNIFTY")
    bot.send_photo(CHAT_ID, chart)

def main():
    bot.send_message(CHAT_ID, "Bot started and sending signals!")
    while True:
        try:
            send_update()
            time.sleep(300)  # 5 min delay
        except Exception as e:
            bot.send_message(CHAT_ID, f"Error: {e}")
            time.sleep(60)

if __name__ == '__main__':
    main()
