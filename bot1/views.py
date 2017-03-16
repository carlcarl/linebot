import logging


from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

logger = logging.getLogger(__name__)

line_bot_api = LineBotApi(settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_ACCESS_TOKEN'])
parser = WebhookParser(settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_SECRET'])


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

    for event in events:
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage):
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )

    return HttpResponse()
