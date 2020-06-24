import json
import os
import unittest
from unittest.mock import patch

from message_service import sns_handler


class TestApigwHandler(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict('os.environ', {
            'SLACK_WEBHOOK_URL': 'https:/localhost/service/test',
        })

    def tearDown(self):
        None

    @patch('requests.post')
    def test_notify_slack(self, mock_requests):
        with self.env:
            with open('tests/sns_event.json', encoding='utf-8', mode='r') as f:
                sns_event = json.load(f)

            sns_handler.notify_slack(sns_event, None)

            msg = {
                'text': 'これはテストです'
            }
            encoded_msg = json.dumps(msg).encode('utf-8')
            mock_requests.assert_called_with(os.environ['SLACK_WEBHOOK_URL'], data=encoded_msg)
