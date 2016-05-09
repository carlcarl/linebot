from django.conf import settings
from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

import json
import logging

from .utils import legal_signature
from .utils import create_msg_headers
from .utils import send_msg

logger = logging.getLogger(__name__)

@csrf_exempt
def index(request):
    logger.info(request.body)
    request_signature = request.META['HTTP_X_LINE_CHANNNELSIGNATURE']
    logger.debug(request_signature)
    channel_secret = settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_SECRET']
    if not legal_signature(request_signature, request.body, channel_secret):
        raise Http404

    json_data = json.loads(request.body.decode('utf-8'))
    channel_id = settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_ID']
    channel_mid = settings.LINE_BOT_SETTINGS['bot1']['CHANNEL_MID']
    headers = create_msg_headers(channel_id, channel_secret, channel_mid)

    request_content = json_data['result'][0]['content']
    from_mid = request_content['from']
    from_text = request_content['text']
    logger.info(from_text)

    response = send_msg(headers, [from_mid], content='haha')
    if response.status_code != 200:
        logger.error(str(response))

    return HttpResponse('haha')
