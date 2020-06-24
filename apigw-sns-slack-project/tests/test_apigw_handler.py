import json
import unittest
from unittest.mock import patch

import boto3
from moto import mock_sns

from message_service import apigw_handler

TOPIC_NAME = 'notify-slack-topic'


@mock_sns
class TestApigwHandler(unittest.TestCase):
    def setUp(self):
        sns_client = boto3.client('sns')
        response = sns_client.create_topic(
            Name=TOPIC_NAME
        )
        self._topic_arn = response['TopicArn']
        self.env = patch.dict('os.environ', {
            'TOPIC_ARN': response['TopicArn'],
        })

    def tearDown(self):
        sns_client = boto3.client('sns')
        sns_client.delete_topic(
            TopicArn=self._topic_arn
        )

    def test_send_msg(self):
        with self.env:
            with open('tests/apigw_event.json', encoding='utf-8', mode='r') as f:
                apigw_event = json.load(f)

            response = apigw_handler.send_msg(apigw_event, None)
            self.assertEqual(response['statusCode'], 200)
