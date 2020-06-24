import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_msg(event, context):
    # body に { "message": "..." } のフォーマットで Slack へ送信したいメッセージを格納する
    logger.info(event)
    body = json.loads(event['body'])
    logger.info(f"message={body['message']}")

    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=os.environ['TOPIC_ARN'],
        Message=body['message']
    )

    response_body = {
        "message": f"published message to SNS (MessageId={response['MessageId']})",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    return response
