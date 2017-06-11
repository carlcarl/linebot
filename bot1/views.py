import logging


from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import redis

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

logger = logging.getLogger(__name__)

line_bot_api = LineBotApi(settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_SECRET'])
text_actions = {}


@csrf_exempt
def index(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    request_signature = request.META['HTTP_X_LINE_SIGNATURE']

    request_body = request.body.decode('utf-8')

    try:
        events = parser.parse(request_body, request_signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    text_actions['spider'] = spider_message

    # Check message action
    for event in events:
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                action = event.message.text.split()[0]
                if action in text_actions:
                    text_actions[action](event)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='看不懂指令: {}'.format(action))
                    )

    return HttpResponse()


def spider_message(event):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    texts = event.message.text.split()
    spider_type = texts[1]
    if spider_type == 'eth':
        prop = texts[2]
        if prop == 'high':
            value = texts[3]
            t = ''
            try:
                int(value)
            except:
                t = '值不對喔: {}'.format(value)
            else:
                r.set('spider:notify:h', value)
                t = '成功!'
            finally:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=t)
                )
        elif prop == 'low':
            value = texts[3]
            t = ''
            try:
                int(value)
            except:
                t = '值不對喔: {}'.format(value)
            else:
                r.set('spider:notify:l', value)
                t = '成功!'
            finally:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=t)
                )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='看不懂這個設定: {}'.format(prop))
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='看不懂指令的類別: {}'.format(spider_type))
        )

