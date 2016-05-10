from django.test import TestCase

from bot1.utils import legal_signature
import json


class UtilsTestCase(TestCase):
    def setUP(self):
        pass

    def test_legal_signature(self):
        signature = 'Z7WG4jbn/87P/L8Ev9q/6af9E/e96w0Jjzi4uzyErvM='
        json_data = {
            'result': [{
                'from': 'u2ddf2eb3c959e561f6c9fa2ea732e7eb8',
                'fromChannel': '1341301815',
                'to': 'u89685c7d93221ee34648637c13ebd462',
                'toChannel': '1467004949',
                'eventType': '138311609000106303',
                'id': 'ABCDEF-12345678901',
                'content': 'haha',
            }]
        }
        msg = json.dumps(json_data, sort_keys=True).encode('utf-8')
        secret = '00000000000000000000000000000000'
        self.assertTrue(legal_signature(signature, msg, secret))
