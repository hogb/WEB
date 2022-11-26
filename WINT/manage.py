#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import time
import telegram
import ctypes,subprocess

import traceback,logging
from datetime import datetime
import pickle
import pandas as pd

def main():
    mt = pd.read_excel(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\CSS참고.xlsx")
    mt.to_pickle(r"C:\Users\Jinu\PycharmProjects\WEB\WINT\CSS참고.pickle")




    with open('url_now.pickle', 'rb') as f:
        to_url = pickle.load(f)

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WINT.settings')
    #os.environ.setdefault('ALLOWED_HOSTS', to_url)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    #try:
    main()
    #
    # except:
    #
    #     log_time = str(datetime.now().strftime('%Y-%m-%d %H%M%S'))
    #
    #     logging.basicConfig(filename='C:/Users/Jinu/PycharmProjects/WEB/WINT/err/' + log_time + '_manage.log', level=logging.ERROR)
    #     logging.error(traceback.format_exc())
    #     print(traceback.format_exc())





