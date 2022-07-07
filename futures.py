import logging
import telebot
import schedule, time

from binance.error import ClientError
from binance.um_futures import UMFutures

futures_client = UMFutures(show_limit_usage=True)
logging.basicConfig(filename='futures.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)


def heartbeat_check():
    telebot.send_check_message("HEARTBEAT CHECK FOR FUTURES SCRIPT!")


def main():
    try:
        res = futures_client.exchange_info()
        logging.info(f"Received response, weight usage:{res['limit_usage']}")
    except ClientError as e:
        telebot.send_message(
            f'ClientError Received! status code:{e.status_code}, error code:{e.error_code}, error message:{e.error_message}, header:{e.header}')
        logging.error(
            f'ClientError Received! status code:{e.status_code}, error code:{e.error_code}, error message:{e.error_message}, header:{e.header}')
        main()


main()
schedule.every(10).minutes.do(main)
schedule.every(4).hours.do(heartbeat_check)

while True:
    schedule.run_pending()
    time.sleep(1)
