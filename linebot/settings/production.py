from linebot.settings.base import *

import os

DEBUG = False
ALLOWED_HOSTS = ['linebot.carlcarl.me']

LINE_BOT_SETTINGS = {
    'bot1': {
        'CHANNEL_ID': os.environ.get('BOT1_CHANNEL_ID'),
        'CHANNEL_SECRET': os.environ.get('BOT1_CHANNEL_SECRET'),
        'MID': os.environ.get('BOT1_MID'),
    },
}

SECRET_KEY = os.environ.get('SECRET_KEY')
