import os.path
import time

import schedule
from binance.spot import Spot as Client

import telebot

REQUEST_WEIGHT_LIMIT = 1200
spot_client = Client(show_limit_usage=True)


def write_symbols(symbols):
    f = open("symbols.txt", "w")
    for i in range(len(symbols)):
        if i == len(symbols) - 1:
            f.write(symbols[i]['symbol'])
        else:
            f.write(symbols[i]['symbol'] + '\n')
    f.close()


def update_symbols(symbols):
    f = open("symbols.txt", "w")
    for symbol in symbols:
        f.write(symbol + '\n')
    f.close()


def check_new_symbols(symbols):
    current_symbols = set(line.strip() for line in open('symbols.txt'))
    updated_symbols = set()
    for symbol in symbols:
        updated_symbols.add(symbol['symbol'])
    listed_symbols = updated_symbols - current_symbols  # present in updated but not in current means listed
    delisted_symbols = current_symbols - updated_symbols  # present in current but not in updated means delisted
    if len(listed_symbols) > 0:
        telebot.send_message(f'New Listed Symbols Detected! {listed_symbols}')
        update_symbols(updated_symbols)
    if len(delisted_symbols) > 0:
        telebot.send_message(f'Delisted Symbols Detected! {delisted_symbols}')
        update_symbols(updated_symbols)


def heartbeat_check():
    telebot.send_check_message("HEARTBEAT CHECK!")


def main():
    result = spot_client.exchange_info()
    symbols = result['data']['symbols']
    used_weight = result['limit_usage']['x-mbx-used-weight-1m']
    if int(used_weight) > REQUEST_WEIGHT_LIMIT - 10:
        telebot.send_message(f'Reaching request weight limit, backing off for 20 seconds...')
        time.sleep(20)
    if os.path.isfile("symbols.txt") and os.path.getsize("symbols.txt") > 0:
        check_new_symbols(symbols)
    else:
        write_symbols(symbols)


schedule.every().second.do(main)
schedule.every(8).hours.do(heartbeat_check)

while True:
    schedule.run_pending()
    time.sleep(1)
