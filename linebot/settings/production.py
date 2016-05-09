from linebot.settings.base import *

import os

DEBUG = False

LINE_BOT_SETTINGS = {
    'bot1': {
        'CHANNEL_ID': os.environ.get('BOT1_CHANNEL_ID'),
        'CHANNEL_SECRET': os.environ.get('BOT1_CHANNEL_SECRET'),
        'MID': os.environ.get('BOT1_MID'),
    },
}
