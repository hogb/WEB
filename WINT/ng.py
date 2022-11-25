#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

import ngrok,time
import telegram
import ctypes,subprocess

import traceback,logging
from datetime import datetime
import pickle

def ng():


    #os.system('ngrok.bat')
    time.sleep(2)

    ngr = '2GuOWZTh5NENaXGtDtjjU8CllfK_5pMK1iSkPaA8SHY7am1XE'
    # construct the api client
    client = ngrok.Client(api_key=ngr,base_url='https://api.ngrok.com')
    # list all online tunnels

    to_url = list(client.tunnels.list())[0].public_url
    print(to_url)

    FROM_HELLO = '1777645275:AAF5Yb-dYd8TqZ1e4TnPqgLQnk6_yBwV0Z0'  # 헬로헬로봇
    TOTO = '562099230'
    HELLO_bot = telegram.Bot(FROM_HELLO)

    HELLO_bot.send_message(chat_id=TOTO, text=(to_url))
    # create an ip policy the allows traffic from some subnets


    with open('url_now.pickle', 'wb') as f:
        pickle.dump(to_url, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    try:
        ng()

    except:

        log_time = str(datetime.now().strftime('%Y-%m-%d %H%M%S'))

        logging.basicConfig(filename='C:/Users/Jinu/PycharmProjects/WEB/WINT/err/' + log_time + '_ng.log', level=logging.ERROR)
        logging.error(traceback.format_exc())
        print(traceback.format_exc())





